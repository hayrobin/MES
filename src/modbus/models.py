"""Modbus data models."""

from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ModbusRegister:
    """Modbus register representation."""
    
    name: str
    register_type: str  # coil, discrete_input, holding_register, input_register
    address: int
    value: Any = None
    data_type: str = "uint16"
    timestamp: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
