import os

from dotenv import load_dotenv

basedir = os.path.join(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "insecure"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") \
        or "sqlite:///dndbehind-dev.db"
