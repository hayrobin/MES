"""OPC UA data models."""

from typing import Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OPCUANode:
    """OPC UA node representation."""
    
    node_id: str
    browse_name: str
    display_name: str
    value: Any = None
    data_type: str = "Variant"
    timestamp: Optional[datetime] = None
    quality: str = "good"
    
    def __post_init__(self) -> None:
        """Set timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()
