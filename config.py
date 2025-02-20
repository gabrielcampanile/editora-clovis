import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+pymysql://root:senha@localhost/editora')
    SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-desenvolvimento')