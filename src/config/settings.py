"""Configuration models using Pydantic."""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class OPCUANodeConfig(BaseModel):
    """Configuration for an OPC UA node."""
    
    node_id: str
    browse_name: str
    display_name: str
    data_type: str
    initial_value: Any = None
    writable: bool = False
    description: str = ""


class OPCUAServerConfig(BaseModel):
    """Configuration for OPC UA server."""
    
    endpoint: str = "opc.tcp://0.0.0.0:4840/freeopcua/server/"
    server_name: str = "Factory MES OPC UA Server"
    namespace: str = "http://factory.mes"
    nodes: List[OPCUANodeConfig] = Field(default_factory=list)
    security_enabled: bool = False
    certificate_path: Optional[str] = None
    private_key_path: Optional[str] = None


class OPCUASubscriptionConfig(BaseModel):
    """Configuration for OPC UA subscription."""
    
    node_id: str
    publishing_interval: int = 1000  # milliseconds


class OPCUAClientConfig(BaseModel):
    """Configuration for OPC UA client connection."""
    
    name: str
    endpoint: str
    namespace_index: int = 2
    subscriptions: List[OPCUASubscriptionConfig] = Field(default_factory=list)
    reconnect_interval: int = 5  # seconds
    timeout: int = 10  # seconds
    security_enabled: bool = False


class ModbusRegisterConfig(BaseModel):
    """Configuration for a Modbus register."""
    
    name: str
    register_type: str  # coil, discrete_input, holding_register, input_register
    address: int
    count: int = 1
    data_type: str = "uint16"  # uint16, int16, uint32, int32, float32
    scale: float = 1.0
    offset: float = 0.0
    unit: str = ""


class ModbusDeviceConfig(BaseModel):
    """Configuration for a Modbus TCP device."""
    
    name: str
    host: str
    port: int = 502
    unit_id: int = 1
    registers: List[ModbusRegisterConfig] = Field(default_factory=list)
    polling_interval: int = 1  # seconds
    timeout: int = 5  # seconds
    reconnect_interval: int = 5  # seconds


class DatabaseConfig(BaseModel):
    """Database configuration."""
    
    type: str = "sqlite"  # sqlite or postgresql
    host: Optional[str] = None
    port: Optional[int] = None
    database: str = "mes.db"
    username: Optional[str] = None
    password: Optional[str] = None
    pool_size: int = 5
    max_overflow: int = 10


class APIConfig(BaseModel):
    """API server configuration."""
    
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    workers: int = 1
    log_level: str = "info"


class MESSettings(BaseSettings):
    """Main MES configuration settings."""
    
    # Application
    app_name: str = "Factory MES"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Logging
    log_level: str = "INFO"
    json_logging: bool = False
    
    # Database
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    
    # API
    api: APIConfig = Field(default_factory=APIConfig)
    
    # Configuration file paths
    opcua_server_config: str = "config/opcua_server.yaml"
    opcua_clients_config: str = "config/opcua_clients.yaml"
    modbus_devices_config: str = "config/modbus_devices.yaml"
    
    # Data retention
    historical_data_retention_days: int = 30
    
    model_config = {
        "env_prefix": "MES_",
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }
