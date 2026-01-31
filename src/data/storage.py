"""Database storage operations."""

import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select, delete, and_, desc
from .models import Base, Device, DataPoint, RealtimeData, HistoricalData, ProductionEvent, Alarm
from ..config.settings import DatabaseConfig
from ..utils.logger import get_logger
from ..utils.exceptions import StorageError

logger = get_logger(__name__)


class DatabaseStorage:
    """Database storage manager."""
    
    def __init__(self, config: DatabaseConfig):
        """Initialize database storage.
        
        Args:
            config: Database configuration
        """
        self.config = config
        self.engine = None
        self.session_factory = None
        
    async def initialize(self) -> None:
        """Initialize database connection and create tables."""
        try:
            # Build connection string
            if self.config.type == "sqlite":
                db_url = f"sqlite+aiosqlite:///{self.config.database}"
            elif self.config.type == "postgresql":
                db_url = (
                    f"postgresql+asyncpg://{self.config.username}:{self.config.password}"
                    f"@{self.config.host}:{self.config.port}/{self.config.database}"
                )
            else:
                raise StorageError(f"Unsupported database type: {self.config.type}")
            
            # Create engine
            self.engine = create_async_engine(
                db_url,
                pool_size=self.config.pool_size,
                max_overflow=self.config.max_overflow,
                echo=False
            )
            
            # Create session factory
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            
            # Create tables
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                
            logger.info(f"Database initialized: {db_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {str(e)}")
            raise StorageError(f"Database initialization failed: {str(e)}")
    
    async def close(self) -> None:
        """Close database connection."""
        if self.engine:
            await self.engine.dispose()
            logger.info("Database connection closed")
    
    def get_session(self) -> AsyncSession:
        """Get database session.
        
        Returns:
            Database session
        """
        if not self.session_factory:
            raise StorageError("Database not initialized")
        return self.session_factory()
    
    # Device operations
    async def create_device(self, name: str, device_type: str, connection_string: str,
                           config: Optional[Dict[str, Any]] = None) -> Device:
        """Create a new device.
        
        Args:
            name: Device name
            device_type: Type of device (opcua, modbus)
            connection_string: Connection string
            config: Optional device configuration
            
        Returns:
            Created device
        """
        async with self.get_session() as session:
            device = Device(
                name=name,
                device_type=device_type,
                connection_string=connection_string,
                config=config
            )
            session.add(device)
            await session.commit()
            await session.refresh(device)
            return device
    
    async def get_device(self, device_id: int) -> Optional[Device]:
        """Get device by ID.
        
        Args:
            device_id: Device ID
            
        Returns:
            Device or None
        """
        async with self.get_session() as session:
            result = await session.execute(select(Device).where(Device.id == device_id))
            return result.scalar_one_or_none()
    
    async def get_device_by_name(self, name: str) -> Optional[Device]:
        """Get device by name.
        
        Args:
            name: Device name
            
        Returns:
            Device or None
        """
        async with self.get_session() as session:
            result = await session.execute(select(Device).where(Device.name == name))
            return result.scalar_one_or_none()
    
    async def get_all_devices(self) -> List[Device]:
        """Get all devices.
        
        Returns:
            List of devices
        """
        async with self.get_session() as session:
            result = await session.execute(select(Device))
            return list(result.scalars().all())
    
    async def update_device_status(self, device_id: int, status: str) -> None:
        """Update device status.
        
        Args:
            device_id: Device ID
            status: New status
        """
        async with self.get_session() as session:
            result = await session.execute(select(Device).where(Device.id == device_id))
            device = result.scalar_one_or_none()
            if device:
                device.status = status
                device.last_seen = datetime.utcnow()
                await session.commit()
    
    # Data point operations
    async def create_data_point(self, device_id: int, name: str, address: str,
                                data_type: str, **kwargs: Any) -> DataPoint:
        """Create a new data point.
        
        Args:
            device_id: Device ID
            name: Data point name
            address: Data point address
            data_type: Data type
            **kwargs: Additional data point attributes
            
        Returns:
            Created data point
        """
        async with self.get_session() as session:
            data_point = DataPoint(
                device_id=device_id,
                name=name,
                address=address,
                data_type=data_type,
                **kwargs
            )
            session.add(data_point)
            await session.commit()
            await session.refresh(data_point)
            return data_point
    
    # Real-time data operations
    async def update_realtime_data(self, device_id: int, data_point_name: str,
                                   value: Any, quality: str = "good",
                                   timestamp: Optional[datetime] = None) -> None:
        """Update real-time data.
        
        Args:
            device_id: Device ID
            data_point_name: Data point name
            value: Data value
            quality: Data quality
            timestamp: Timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
            
        async with self.get_session() as session:
            # Try to get existing record
            result = await session.execute(
                select(RealtimeData).where(
                    and_(
                        RealtimeData.device_id == device_id,
                        RealtimeData.data_point_name == data_point_name
                    )
                )
            )
            realtime = result.scalar_one_or_none()
            
            if realtime:
                # Update existing
                realtime.value = str(value)
                realtime.quality = quality
                realtime.timestamp = timestamp
            else:
                # Create new
                realtime = RealtimeData(
                    device_id=device_id,
                    data_point_name=data_point_name,
                    value=str(value),
                    quality=quality,
                    timestamp=timestamp
                )
                session.add(realtime)
            
            await session.commit()
    
    async def get_realtime_data(self, device_id: Optional[int] = None) -> List[RealtimeData]:
        """Get real-time data.
        
        Args:
            device_id: Optional device ID filter
            
        Returns:
            List of real-time data
        """
        async with self.get_session() as session:
            query = select(RealtimeData)
            if device_id:
                query = query.where(RealtimeData.device_id == device_id)
            result = await session.execute(query)
            return list(result.scalars().all())
    
    # Historical data operations
    async def insert_historical_data(self, device_id: int, data_point_name: str,
                                     value: Any, quality: str = "good",
                                     timestamp: Optional[datetime] = None) -> None:
        """Insert historical data.
        
        Args:
            device_id: Device ID
            data_point_name: Data point name
            value: Data value
            quality: Data quality
            timestamp: Timestamp (defaults to now)
        """
        if timestamp is None:
            timestamp = datetime.utcnow()
            
        async with self.get_session() as session:
            historical = HistoricalData(
                device_id=device_id,
                data_point_name=data_point_name,
                value=str(value),
                quality=quality,
                timestamp=timestamp
            )
            session.add(historical)
            await session.commit()
    
    async def get_historical_data(self, device_id: int, data_point_name: str,
                                  start_time: datetime, end_time: datetime) -> List[HistoricalData]:
        """Get historical data for a time range.
        
        Args:
            device_id: Device ID
            data_point_name: Data point name
            start_time: Start time
            end_time: End time
            
        Returns:
            List of historical data
        """
        async with self.get_session() as session:
            result = await session.execute(
                select(HistoricalData).where(
                    and_(
                        HistoricalData.device_id == device_id,
                        HistoricalData.data_point_name == data_point_name,
                        HistoricalData.timestamp >= start_time,
                        HistoricalData.timestamp <= end_time
                    )
                ).order_by(HistoricalData.timestamp)
            )
            return list(result.scalars().all())
    
    async def cleanup_old_data(self, retention_days: int) -> None:
        """Clean up old historical data.
        
        Args:
            retention_days: Number of days to retain
        """
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        async with self.get_session() as session:
            await session.execute(
                delete(HistoricalData).where(HistoricalData.timestamp < cutoff_date)
            )
            await session.commit()
            logger.info(f"Cleaned up historical data older than {retention_days} days")
    
    # Alarm operations
    async def create_alarm(self, device_id: Optional[int], severity: str,
                          message: str, metadata: Optional[Dict[str, Any]] = None) -> Alarm:
        """Create a new alarm.
        
        Args:
            device_id: Optional device ID
            severity: Alarm severity
            message: Alarm message
            metadata: Optional metadata
            
        Returns:
            Created alarm
        """
        async with self.get_session() as session:
            alarm = Alarm(
                device_id=device_id,
                severity=severity,
                message=message,
                metadata=metadata
            )
            session.add(alarm)
            await session.commit()
            await session.refresh(alarm)
            return alarm
    
    async def get_active_alarms(self) -> List[Alarm]:
        """Get active (unresolved) alarms.
        
        Returns:
            List of active alarms
        """
        async with self.get_session() as session:
            result = await session.execute(
                select(Alarm).where(Alarm.resolved == False).order_by(desc(Alarm.timestamp))
            )
            return list(result.scalars().all())
