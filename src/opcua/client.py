"""OPC UA Client implementation."""

import asyncio
from typing import Dict, Any, Optional, Callable, List
from asyncua import Client
from asyncua.common.node import Node
from asyncua.common.subscription import Subscription
from ..config.settings import OPCUAClientConfig
from ..data.acquisition import DataPoint
from ..utils.logger import get_logger
from ..utils.exceptions import OPCUAConnectionError, OPCUAReadError, OPCUAWriteError

logger = get_logger(__name__)


class OPCUAClient:
    """OPC UA Client implementation."""
    
    def __init__(self, config: OPCUAClientConfig, data_callback: Optional[Callable] = None):
        """Initialize OPC UA client.
        
        Args:
            config: Client configuration
            data_callback: Optional callback for data updates
        """
        self.config = config
        self.data_callback = data_callback
        self.client: Optional[Client] = None
        self.subscription: Optional[Subscription] = None
        self.connected = False
        self.running = False
        
    async def connect(self) -> None:
        """Connect to OPC UA server."""
        try:
            self.client = Client(url=self.config.endpoint, timeout=self.config.timeout)
            
            if self.config.security_enabled:
                # Security configuration would go here
                logger.warning("OPC UA client security not fully implemented yet")
            
            await self.client.connect()
            self.connected = True
            logger.info(f"Connected to OPC UA server: {self.config.name} ({self.config.endpoint})")
            
        except Exception as e:
            self.connected = False
            logger.error(f"Failed to connect to OPC UA server {self.config.name}: {str(e)}")
            raise OPCUAConnectionError(f"Connection failed: {str(e)}")
    
    async def disconnect(self) -> None:
        """Disconnect from OPC UA server."""
        if self.subscription:
            try:
                await self.subscription.delete()
            except Exception as e:
                logger.warning(f"Error deleting subscription: {str(e)}")
        
        if self.client and self.connected:
            try:
                await self.client.disconnect()
                self.connected = False
                logger.info(f"Disconnected from OPC UA server: {self.config.name}")
            except Exception as e:
                logger.error(f"Error disconnecting: {str(e)}")
    
    async def browse(self, node_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Browse OPC UA address space.
        
        Args:
            node_id: Optional starting node ID (defaults to Objects folder)
            
        Returns:
            List of node information dictionaries
        """
        if not self.connected or not self.client:
            raise OPCUAConnectionError("Not connected to server")
        
        try:
            # Get starting node
            if node_id:
                node = self.client.get_node(node_id)
            else:
                node = self.client.nodes.objects
            
            # Browse children
            children = await node.get_children()
            
            nodes_info = []
            for child in children:
                try:
                    browse_name = await child.read_browse_name()
                    display_name = await child.read_display_name()
                    node_class = await child.read_node_class()
                    
                    nodes_info.append({
                        "node_id": child.nodeid.to_string(),
                        "browse_name": browse_name.Name,
                        "display_name": display_name.Text,
                        "node_class": node_class.name
                    })
                except Exception as e:
                    logger.warning(f"Error reading node info: {str(e)}")
                    
            return nodes_info
            
        except Exception as e:
            logger.error(f"Browse error: {str(e)}")
            raise OPCUAReadError(f"Failed to browse: {str(e)}")
    
    async def read_node(self, node_id: str) -> Any:
        """Read value from a node.
        
        Args:
            node_id: Node ID to read
            
        Returns:
            Node value
        """
        if not self.connected or not self.client:
            raise OPCUAConnectionError("Not connected to server")
        
        try:
            node = self.client.get_node(node_id)
            value = await node.get_value()
            return value
        except Exception as e:
            logger.error(f"Read error for node {node_id}: {str(e)}")
            raise OPCUAReadError(f"Failed to read node {node_id}: {str(e)}")
    
    async def write_node(self, node_id: str, value: Any) -> None:
        """Write value to a node.
        
        Args:
            node_id: Node ID to write
            value: Value to write
        """
        if not self.connected or not self.client:
            raise OPCUAConnectionError("Not connected to server")
        
        try:
            node = self.client.get_node(node_id)
            await node.set_value(value)
            logger.debug(f"Wrote value to node {node_id}: {value}")
        except Exception as e:
            logger.error(f"Write error for node {node_id}: {str(e)}")
            raise OPCUAWriteError(f"Failed to write to node {node_id}: {str(e)}")
    
    async def batch_read(self, node_ids: List[str]) -> Dict[str, Any]:
        """Read multiple nodes at once.
        
        Args:
            node_ids: List of node IDs to read
            
        Returns:
            Dictionary mapping node IDs to values
        """
        if not self.connected or not self.client:
            raise OPCUAConnectionError("Not connected to server")
        
        results = {}
        for node_id in node_ids:
            try:
                value = await self.read_node(node_id)
                results[node_id] = value
            except Exception as e:
                logger.warning(f"Failed to read node {node_id}: {str(e)}")
                results[node_id] = None
        
        return results
    
    async def subscribe_to_nodes(self) -> None:
        """Subscribe to configured nodes for data changes."""
        if not self.connected or not self.client:
            raise OPCUAConnectionError("Not connected to server")
        
        if not self.config.subscriptions:
            logger.debug(f"No subscriptions configured for {self.config.name}")
            return
        
        try:
            # Create subscription
            self.subscription = await self.client.create_subscription(500, self)
            
            # Subscribe to each configured node
            for sub_config in self.config.subscriptions:
                try:
                    node = self.client.get_node(sub_config.node_id)
                    await self.subscription.subscribe_data_change(node)
                    logger.debug(f"Subscribed to node: {sub_config.node_id}")
                except Exception as e:
                    logger.error(f"Failed to subscribe to {sub_config.node_id}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Subscription error: {str(e)}")
            raise OPCUAConnectionError(f"Failed to create subscriptions: {str(e)}")
    
    def datachange_notification(self, node: Node, val: Any, data: Any) -> None:
        """Handle data change notifications.
        
        Args:
            node: Node that changed
            val: New value
            data: Additional data
        """
        try:
            node_id = node.nodeid.to_string()
            
            # Create data point
            data_point = DataPoint(
                device_name=self.config.name,
                point_name=node_id,
                value=val
            )
            
            # Call data callback if provided
            if self.data_callback:
                asyncio.create_task(self.data_callback(data_point))
                
            logger.debug(f"Data change notification: {node_id} = {val}")
            
        except Exception as e:
            logger.error(f"Error handling data change: {str(e)}")
    
    async def run(self) -> None:
        """Run client with automatic reconnection."""
        self.running = True
        
        while self.running:
            try:
                # Connect if not connected
                if not self.connected:
                    await self.connect()
                    await self.subscribe_to_nodes()
                
                # Keep connection alive
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Client {self.config.name} error: {str(e)}")
                self.connected = False
                
                # Wait before reconnecting
                logger.info(f"Reconnecting in {self.config.reconnect_interval} seconds...")
                await asyncio.sleep(self.config.reconnect_interval)
    
    async def stop(self) -> None:
        """Stop client."""
        self.running = False
        await self.disconnect()
