"""Custom exceptions for the MES system."""


class MESException(Exception):
    """Base exception for all MES errors."""
    pass


class OPCUAException(MESException):
    """Exception for OPC UA related errors."""
    pass


class OPCUAConnectionError(OPCUAException):
    """Exception for OPC UA connection errors."""
    pass


class OPCUAReadError(OPCUAException):
    """Exception for OPC UA read errors."""
    pass


class OPCUAWriteError(OPCUAException):
    """Exception for OPC UA write errors."""
    pass


class ModbusException(MESException):
    """Exception for Modbus related errors."""
    pass


class ModbusConnectionError(ModbusException):
    """Exception for Modbus connection errors."""
    pass


class ModbusReadError(ModbusException):
    """Exception for Modbus read errors."""
    pass


class ModbusWriteError(ModbusException):
    """Exception for Modbus write errors."""
    pass


class ConfigurationError(MESException):
    """Exception for configuration errors."""
    pass


class DataAcquisitionError(MESException):
    """Exception for data acquisition errors."""
    pass


class StorageError(MESException):
    """Exception for storage errors."""
    pass
