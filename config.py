"""Configuration file for the application."""

import os

from dotenv import load_dotenv

basedir = os.path.join(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Base configuration for the application."""

    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get("JWT_ACCESS_TOKEN_EXPIRES") or 3600
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "NOTSECURE"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "insecure"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
        or "sqlite:///dndbehind-dev.db"


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-secret-key"
