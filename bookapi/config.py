import os
class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://tarun:tarun@localhost:5432/bookdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config): # TestConfig inherits from the base Config
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' # Still use in-memory SQLite for tests
    TESTING = True # Essential for Flask testing features
    SQLALCHEMY_TRACK_MODIFICATIONS = False