"""OPC UA Server implementation."""

import asyncio
from typing import Dict, Any, Optional
from asyncua import Server, ua
from asyncua.common.node import Node
from ..config.settings import OPCUAServerConfig
from ..utils.logger import get_logger
from ..utils.exceptions import OPCUAException

logger = get_logger(__name__)


class OPCUAServer:
    """OPC UA Server implementation."""
    
    def __init__(self, config: OPCUAServerConfig):
        """Initialize OPC UA server.
        
        Args:
            config: Server configuration
        """
        self.config = config
        self.server: Optional[Server] = None
        self.namespace_idx: Optional[int] = None
        self.nodes: Dict[str, Node] = {}
        self.running = False
        
    async def start(self) -> None:
        """Start OPC UA server."""
        try:
            # Create server
            self.server = Server()
            await self.server.init()
            
            # Set endpoint
            self.server.set_endpoint(self.config.endpoint)
            self.server.set_server_name(self.config.server_name)
            
            # Register namespace
            self.namespace_idx = await self.server.register_namespace(self.config.namespace)
            
            # Set security if enabled
            if self.config.security_enabled:
                # Security configuration would go here
                logger.warning("OPC UA security not fully implemented yet")
            
            # Create nodes from configuration
            await self._create_nodes()
            
            # Start server
            async with self.server:
                self.running = True
                logger.info(f"OPC UA server started at {self.config.endpoint}")
                
                # Keep server running
                while self.running:
                    await asyncio.sleep(1)
                    
        except Exception as e:
            logger.error(f"OPC UA server error: {str(e)}")
            raise OPCUAException(f"Failed to start OPC UA server: {str(e)}")
    
    async def stop(self) -> None:
        """Stop OPC UA server."""
        self.running = False
        logger.info("OPC UA server stopped")
    
    async def _create_nodes(self) -> None:
        """Create nodes from configuration."""
        if not self.server or self.namespace_idx is None:
            return
            
        # Get objects node
        objects = self.server.get_objects_node()
        
        # Create folder for our nodes
        folder = await objects.add_folder(self.namespace_idx, "Factory")
        
        for node_config in self.config.nodes:
            try:
                # Map data type string to UA type
                ua_type = self._get_ua_datatype(node_config.data_type)
                
                # Create variable node
                node = await folder.add_variable(
                    self.namespace_idx,
                    node_config.browse_name,
                    node_config.initial_value if node_config.initial_value is not None else 0,
                    varianttype=ua_type
                )
                
                # Set properties
                await node.set_writable(node_config.writable)
                if node_config.description:
                    await node.set_attribute(
                        ua.AttributeIds.Description,
                        ua.DataValue(ua.LocalizedText(node_config.description))
                    )
                
                # Store node reference
                self.nodes[node_config.node_id] = node
                
                logger.debug(f"Created OPC UA node: {node_config.browse_name}")
                
            except Exception as e:
                logger.error(f"Failed to create node {node_config.browse_name}: {str(e)}")
    
    def _get_ua_datatype(self, type_str: str) -> ua.VariantType:
        """Map data type string to OPC UA variant type.
        
        Args:
            type_str: Data type string
            
        Returns:
            OPC UA variant type
        """
        type_map = {
            "bool": ua.VariantType.Boolean,
            "int": ua.VariantType.Int32,
            "float": ua.VariantType.Float,
            "double": ua.VariantType.Double,
            "string": ua.VariantType.String,
        }
        return type_map.get(type_str.lower(), ua.VariantType.Variant)
    
    async def write_value(self, node_id: str, value: Any) -> None:
        """Write value to a node.
        
        Args:
            node_id: Node ID
            value: Value to write
        """
        if node_id not in self.nodes:
            raise OPCUAException(f"Node not found: {node_id}")
        
        try:
            node = self.nodes[node_id]
            await node.set_value(value)
            logger.debug(f"Wrote value to node {node_id}: {value}")
        except Exception as e:
            raise OPCUAException(f"Failed to write to node {node_id}: {str(e)}")
    
    async def read_value(self, node_id: str) -> Any:
        """Read value from a node.
        
        Args:
            node_id: Node ID
            
        Returns:
            Node value
        """
        if node_id not in self.nodes:
            raise OPCUAException(f"Node not found: {node_id}")
        
        try:
            node = self.nodes[node_id]
            value = await node.get_value()
            return value
        except Exception as e:
            raise OPCUAException(f"Failed to read from node {node_id}: {str(e)}")
