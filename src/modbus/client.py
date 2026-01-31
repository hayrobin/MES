"""Modbus TCP/IP client implementation."""

import asyncio
import struct
from typing import List, Optional, Any
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.exceptions import ModbusException
from ..config.settings import ModbusDeviceConfig, ModbusRegisterConfig
from ..utils.logger import get_logger
from ..utils.exceptions import ModbusConnectionError, ModbusReadError, ModbusWriteError

logger = get_logger(__name__)


class ModbusClient:
    """Modbus TCP client for a single device."""
    
    def __init__(self, config: ModbusDeviceConfig):
        """Initialize Modbus client.
        
        Args:
            config: Device configuration
        """
        self.config = config
        self.client: Optional[AsyncModbusTcpClient] = None
        self.connected = False
        
    async def connect(self) -> None:
        """Connect to Modbus device."""
        try:
            self.client = AsyncModbusTcpClient(
                host=self.config.host,
                port=self.config.port,
                timeout=self.config.timeout
            )
            
            result = await self.client.connect()
            if result:
                self.connected = True
                logger.info(f"Connected to Modbus device: {self.config.name} ({self.config.host}:{self.config.port})")
            else:
                raise ModbusConnectionError(f"Failed to connect to {self.config.name}")
                
        except Exception as e:
            self.connected = False
            logger.error(f"Modbus connection error for {self.config.name}: {str(e)}")
            raise ModbusConnectionError(f"Connection failed: {str(e)}")
    
    async def disconnect(self) -> None:
        """Disconnect from Modbus device."""
        if self.client:
            self.client.close()
            self.connected = False
            logger.info(f"Disconnected from Modbus device: {self.config.name}")
    
    async def read_coils(self, address: int, count: int = 1) -> List[bool]:
        """Read coils (FC1).
        
        Args:
            address: Starting address
            count: Number of coils to read
            
        Returns:
            List of coil values
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.read_coils(address, count, slave=self.config.unit_id)
            if result.isError():
                raise ModbusReadError(f"Error reading coils: {result}")
            return result.bits[:count]
        except Exception as e:
            logger.error(f"Read coils error: {str(e)}")
            raise ModbusReadError(f"Failed to read coils: {str(e)}")
    
    async def read_discrete_inputs(self, address: int, count: int = 1) -> List[bool]:
        """Read discrete inputs (FC2).
        
        Args:
            address: Starting address
            count: Number of inputs to read
            
        Returns:
            List of input values
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.read_discrete_inputs(address, count, slave=self.config.unit_id)
            if result.isError():
                raise ModbusReadError(f"Error reading discrete inputs: {result}")
            return result.bits[:count]
        except Exception as e:
            logger.error(f"Read discrete inputs error: {str(e)}")
            raise ModbusReadError(f"Failed to read discrete inputs: {str(e)}")
    
    async def read_holding_registers(self, address: int, count: int = 1) -> List[int]:
        """Read holding registers (FC3).
        
        Args:
            address: Starting address
            count: Number of registers to read
            
        Returns:
            List of register values
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.read_holding_registers(address, count, slave=self.config.unit_id)
            if result.isError():
                raise ModbusReadError(f"Error reading holding registers: {result}")
            return result.registers
        except Exception as e:
            logger.error(f"Read holding registers error: {str(e)}")
            raise ModbusReadError(f"Failed to read holding registers: {str(e)}")
    
    async def read_input_registers(self, address: int, count: int = 1) -> List[int]:
        """Read input registers (FC4).
        
        Args:
            address: Starting address
            count: Number of registers to read
            
        Returns:
            List of register values
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.read_input_registers(address, count, slave=self.config.unit_id)
            if result.isError():
                raise ModbusReadError(f"Error reading input registers: {result}")
            return result.registers
        except Exception as e:
            logger.error(f"Read input registers error: {str(e)}")
            raise ModbusReadError(f"Failed to read input registers: {str(e)}")
    
    async def write_coil(self, address: int, value: bool) -> None:
        """Write single coil (FC5).
        
        Args:
            address: Coil address
            value: Value to write
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.write_coil(address, value, slave=self.config.unit_id)
            if result.isError():
                raise ModbusWriteError(f"Error writing coil: {result}")
            logger.debug(f"Wrote coil {address} = {value}")
        except Exception as e:
            logger.error(f"Write coil error: {str(e)}")
            raise ModbusWriteError(f"Failed to write coil: {str(e)}")
    
    async def write_register(self, address: int, value: int) -> None:
        """Write single register (FC6).
        
        Args:
            address: Register address
            value: Value to write
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.write_register(address, value, slave=self.config.unit_id)
            if result.isError():
                raise ModbusWriteError(f"Error writing register: {result}")
            logger.debug(f"Wrote register {address} = {value}")
        except Exception as e:
            logger.error(f"Write register error: {str(e)}")
            raise ModbusWriteError(f"Failed to write register: {str(e)}")
    
    async def write_coils(self, address: int, values: List[bool]) -> None:
        """Write multiple coils (FC15).
        
        Args:
            address: Starting address
            values: List of values to write
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.write_coils(address, values, slave=self.config.unit_id)
            if result.isError():
                raise ModbusWriteError(f"Error writing coils: {result}")
            logger.debug(f"Wrote {len(values)} coils starting at {address}")
        except Exception as e:
            logger.error(f"Write coils error: {str(e)}")
            raise ModbusWriteError(f"Failed to write coils: {str(e)}")
    
    async def write_registers(self, address: int, values: List[int]) -> None:
        """Write multiple registers (FC16).
        
        Args:
            address: Starting address
            values: List of values to write
        """
        if not self.connected or not self.client:
            raise ModbusConnectionError("Not connected to device")
        
        try:
            result = await self.client.write_registers(address, values, slave=self.config.unit_id)
            if result.isError():
                raise ModbusWriteError(f"Error writing registers: {result}")
            logger.debug(f"Wrote {len(values)} registers starting at {address}")
        except Exception as e:
            logger.error(f"Write registers error: {str(e)}")
            raise ModbusWriteError(f"Failed to write registers: {str(e)}")
    
    def decode_value(self, registers: List[int], data_type: str) -> Any:
        """Decode register values to specific data type.
        
        Args:
            registers: List of register values
            data_type: Data type to decode to
            
        Returns:
            Decoded value
        """
        if data_type == "uint16":
            return registers[0]
        elif data_type == "int16":
            return struct.unpack('>h', struct.pack('>H', registers[0]))[0]
        elif data_type == "uint32":
            return (registers[0] << 16) | registers[1]
        elif data_type == "int32":
            value = (registers[0] << 16) | registers[1]
            return struct.unpack('>i', struct.pack('>I', value))[0]
        elif data_type == "float32":
            bytes_data = struct.pack('>HH', registers[0], registers[1])
            return struct.unpack('>f', bytes_data)[0]
        else:
            return registers[0]
    
    def encode_value(self, value: Any, data_type: str) -> List[int]:
        """Encode value to register format.
        
        Args:
            value: Value to encode
            data_type: Data type
            
        Returns:
            List of register values
        """
        if data_type == "uint16":
            return [int(value) & 0xFFFF]
        elif data_type == "int16":
            return [struct.unpack('>H', struct.pack('>h', int(value)))[0]]
        elif data_type == "uint32":
            val = int(value)
            return [(val >> 16) & 0xFFFF, val & 0xFFFF]
        elif data_type == "int32":
            bytes_data = struct.pack('>i', int(value))
            return list(struct.unpack('>HH', bytes_data))
        elif data_type == "float32":
            bytes_data = struct.pack('>f', float(value))
            return list(struct.unpack('>HH', bytes_data))
        else:
            return [int(value) & 0xFFFF]
