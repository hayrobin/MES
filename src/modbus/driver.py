"""Modbus TCP/IP driver with polling."""

import asyncio
from typing import Optional, Callable, Dict, Any
from datetime import datetime
from .client import ModbusClient
from ..config.settings import ModbusDeviceConfig
from ..data.acquisition import DataPoint
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ModbusDriver:
    """Modbus driver with polling capability."""
    
    def __init__(self, config: ModbusDeviceConfig, data_callback: Optional[Callable] = None):
        """Initialize Modbus driver.
        
        Args:
            config: Device configuration
            data_callback: Optional callback for data updates
        """
        self.config = config
        self.data_callback = data_callback
        self.client = ModbusClient(config)
        self.running = False
        self.poll_task: Optional[asyncio.Task] = None
        
    async def start(self) -> None:
        """Start Modbus driver."""
        self.running = True
        self.poll_task = asyncio.create_task(self._poll_loop())
        logger.info(f"Modbus driver started for {self.config.name}")
    
    async def stop(self) -> None:
        """Stop Modbus driver."""
        self.running = False
        if self.poll_task:
            self.poll_task.cancel()
            try:
                await self.poll_task
            except asyncio.CancelledError:
                pass
        await self.client.disconnect()
        logger.info(f"Modbus driver stopped for {self.config.name}")
    
    async def _poll_loop(self) -> None:
        """Main polling loop."""
        while self.running:
            try:
                # Connect if not connected
                if not self.client.connected:
                    await self.client.connect()
                
                # Poll all configured registers
                await self._poll_registers()
                
                # Wait for next poll interval
                await asyncio.sleep(self.config.polling_interval)
                
            except Exception as e:
                logger.error(f"Polling error for {self.config.name}: {str(e)}")
                self.client.connected = False
                
                # Wait before retrying
                await asyncio.sleep(self.config.reconnect_interval)
    
    async def _poll_registers(self) -> None:
        """Poll all configured registers."""
        for register_config in self.config.registers:
            try:
                value = await self._read_register(register_config)
                
                # Apply scale and offset
                if isinstance(value, (int, float)):
                    value = (value * register_config.scale) + register_config.offset
                
                # Create data point
                data_point = DataPoint(
                    device_name=self.config.name,
                    point_name=register_config.name,
                    value=value,
                    timestamp=datetime.utcnow()
                )
                
                # Call data callback if provided
                if self.data_callback:
                    await self.data_callback(data_point)
                    
            except Exception as e:
                logger.error(f"Error reading register {register_config.name}: {str(e)}")
    
    async def _read_register(self, register_config: Any) -> Any:
        """Read a single register.
        
        Args:
            register_config: Register configuration
            
        Returns:
            Register value
        """
        reg_type = register_config.register_type
        address = register_config.address
        count = register_config.count
        
        if reg_type == "coil":
            values = await self.client.read_coils(address, count)
            return values[0] if count == 1 else values
            
        elif reg_type == "discrete_input":
            values = await self.client.read_discrete_inputs(address, count)
            return values[0] if count == 1 else values
            
        elif reg_type == "holding_register":
            registers = await self.client.read_holding_registers(address, count)
            return self.client.decode_value(registers, register_config.data_type)
            
        elif reg_type == "input_register":
            registers = await self.client.read_input_registers(address, count)
            return self.client.decode_value(registers, register_config.data_type)
            
        else:
            raise ValueError(f"Unknown register type: {reg_type}")
    
    async def write_register(self, register_name: str, value: Any) -> None:
        """Write value to a register by name.
        
        Args:
            register_name: Register name
            value: Value to write
        """
        # Find register config
        register_config = None
        for reg in self.config.registers:
            if reg.name == register_name:
                register_config = reg
                break
        
        if not register_config:
            raise ValueError(f"Register not found: {register_name}")
        
        # Write value based on type
        reg_type = register_config.register_type
        address = register_config.address
        
        if reg_type == "coil":
            await self.client.write_coil(address, bool(value))
        elif reg_type == "holding_register":
            encoded = self.client.encode_value(value, register_config.data_type)
            if len(encoded) == 1:
                await self.client.write_register(address, encoded[0])
            else:
                await self.client.write_registers(address, encoded)
        else:
            raise ValueError(f"Cannot write to {reg_type}")
