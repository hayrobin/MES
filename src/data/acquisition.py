"""Data acquisition layer - unified interface for all protocol drivers."""

import asyncio
from datetime import datetime
from typing import Any, Dict, Optional, Callable
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.exceptions import DataAcquisitionError

logger = get_logger(__name__)


@dataclass
class DataPoint:
    """Data point representation."""
    
    device_name: str
    point_name: str
    value: Any
    quality: str = "good"
    timestamp: Optional[datetime] = None
    
    def __post_init__(self) -> None:
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class DataAcquisitionManager:
    """Manager for data acquisition from multiple sources."""
    
    def __init__(self):
        """Initialize data acquisition manager."""
        self.data_callbacks: list[Callable[[DataPoint], None]] = []
        self.running = False
        
    def register_callback(self, callback: Callable[[DataPoint], None]) -> None:
        """Register a callback for data updates.
        
        Args:
            callback: Callback function that receives DataPoint
        """
        self.data_callbacks.append(callback)
        logger.debug(f"Registered data callback: {callback.__name__}")
    
    async def publish_data(self, data_point: DataPoint) -> None:
        """Publish data point to all registered callbacks.
        
        Args:
            data_point: Data point to publish
        """
        for callback in self.data_callbacks:
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data_point)
                else:
                    callback(data_point)
            except Exception as e:
                logger.error(f"Error in data callback {callback.__name__}: {str(e)}")
    
    def validate_data(self, value: Any, data_type: str) -> tuple[bool, Any]:
        """Validate and convert data value.
        
        Args:
            value: Value to validate
            data_type: Expected data type
            
        Returns:
            Tuple of (is_valid, converted_value)
        """
        try:
            if data_type == "float":
                return True, float(value)
            elif data_type == "int":
                return True, int(value)
            elif data_type == "bool":
                if isinstance(value, bool):
                    return True, value
                return True, bool(int(value))
            elif data_type == "string":
                return True, str(value)
            else:
                return True, value
        except (ValueError, TypeError) as e:
            logger.warning(f"Data validation failed for type {data_type}: {str(e)}")
            return False, None
    
    def normalize_data(self, value: Any, scale: float = 1.0, offset: float = 0.0) -> Any:
        """Normalize data value using scale and offset.
        
        Args:
            value: Value to normalize
            scale: Scale factor
            offset: Offset value
            
        Returns:
            Normalized value
        """
        try:
            if isinstance(value, (int, float)):
                return (float(value) * scale) + offset
            return value
        except Exception as e:
            logger.warning(f"Data normalization failed: {str(e)}")
            return value
    
    async def start(self) -> None:
        """Start data acquisition."""
        self.running = True
        logger.info("Data acquisition manager started")
    
    async def stop(self) -> None:
        """Stop data acquisition."""
        self.running = False
        logger.info("Data acquisition manager stopped")
