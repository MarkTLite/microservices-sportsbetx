"""Config for securing sensitive information"""
import os

class Config:
    DEBUG = False
    DEVELOPMENT = False
    DATABASE = 'postgresql'
    SECRET_KEY = os.getenv("SECRET_KEY", "default-key")

class ProductionConfig(Config):
    pass

class StagingConfig(Config):
    DEBUG = True

class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True