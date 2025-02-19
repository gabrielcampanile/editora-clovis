from sqlalchemy import (
    create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Configuração do Banco de Dados MariaDB
engine = create_engine("mysql+pymysql://seu_usuario:sua_senha@seu_host:porta/seu_banco")

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Definição das tabelas

class Pessoa(Base):
    __tablename__ = 'pessoa'
    
    cod_pessoa = Column(Integer, primary_key=True)
    CPF = Column(String(11), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    data_nasc = Column(Date, nullable=False)
    
    revisores = relationship("Revisor", back_populates="pessoa")
    autores = relationship("Autor", back_populates="pessoa")

class Revisor(Base):
    __tablename__ = 'revisor'
    
    cod_revisor = Column(Integer, primary_key=True)
    cod_pessoa = Column(Integer, ForeignKey('pessoa.cod_pessoa'), nullable=False)
    especialidade = Column(String(100))
    salario = Column(DECIMAL(10, 2), nullable=False)
    data_contrato = Column(Date, nullable=False)
    
    pessoa = relationship("Pessoa", back_populates="revisores")
    revisoes = relationship("Revisa", back_populates="revisor")

class Autor(Base):
    __tablename__ = 'autor'
    
    cod_autor = Column(Integer, primary_key=True)
    cod_pessoa = Column(Integer, ForeignKey('pessoa.cod_pessoa'), nullable=False)

    pessoa = relationship("Pessoa", back_populates="autores")
    escreve = relationship("Escreve", back_populates="autor")

class Livro(Base):
    __tablename__ = 'livro'
    
    cod_livro = Column(Integer, primary_key=True)
    genero = Column(String(50), nullable=False)
    titulo = Column(String(200), nullable=False)

    revisoes = relationship("Revisa", back_populates="livro")
    escreve = relationship("Escreve", back_populates="livro")

class Revisa(Base):
    __tablename__ = 'revisa'
    
    cod_revisor = Column(Integer, ForeignKey('revisor.cod_revisor'), primary_key=True)
    cod_pessoa = Column(Integer, ForeignKey('pessoa.cod_pessoa'), primary_key=True)
    cod_livro = Column(Integer, ForeignKey('livro.cod_livro'), primary_key=True)
    status_revisao = Column(String(50))

    revisor = relationship("Revisor", back_populates="revisoes")
    livro = relationship("Livro", back_populates="revisoes")

class Escreve(Base):
    __tablename__ = 'escreve'
    
    cod_autor = Column(Integer, ForeignKey('autor.cod_autor'), primary_key=True)
    cod_pessoa = Column(Integer, ForeignKey('pessoa.cod_pessoa'), primary_key=True)
    cod_livro = Column(Integer, ForeignKey('livro.cod_livro'), primary_key=True)

    autor = relationship("Autor", back_populates="escreve")
    livro = relationship("Livro", back_populates="escreve")

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)
