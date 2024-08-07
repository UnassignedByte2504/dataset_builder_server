from pydantic_settings import BaseSettings
import os
import logging

class AppSettings(BaseSettings):
    """App settings class."""
    app_name: str = 'Autoamata Dataset Builder'
    app_version: str = '0.1.0'
    app_description: str = 'Autoamata Dataset Builder service'
    app_host: str = 'localhost'
    app_port: int = 8000
    log_level: str = 'INFO'
    
    class Config:
        env_prefix = 'APP_'
        env_file = '.env'
        env_file_encoding = 'utf-8'
        case_sensitive = False
        extra = 'allow'
 
 
__all__ = ['AppSettings']       