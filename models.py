# importar bibliotecas
import integer
from sqlalchemy import Column, Integer, String, create_engine, Text
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine('mysql+pymysql://root:senaisp@localhost:3306/registro_site', echo=False)

# configurar seções locais
local_session = sessionmaker(bind=engine)
Base = declarative_base()

# modelo Musica

class Musica(Base):
    __tablename__ = 'musica'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    artista = Column(String(60), nullable=False)
    album = Column(String(60))
    ano_lancamento = Column(String(60))
    letras = Column(Text, nullable=False)
    url_img = Column(String(255), nullable=True)

    def __repr__(self):
        return (f"<Musica(id={self.id}, nome='{self.nome}', artista='{self.artista}', "
                f"album='{self.album}', ano_lancamento='{self.ano_lancamento}', letras='{self.letras}', url_img='{self.url_img}'>")

class Artista(Base):
    __tablename__ = 'artista'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    sobrenome = Column(String(60), nullable=False)
    data_nascimento = Column(String(60), nullable=False)
    url_img = Column(String(255), nullable=True)

    def __repr__(self):
        return (f"<Artista(id={self.id}, nome='{self.nome}', sobrenome='{self.sobrenome}', "
                f"data_nascimento='{self.data_nascimento}'), url_img='{self.url_img}'>")


class Albuns(Base):
    __tablename__ = 'albuns'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    artista = Column(String(60), nullable=False)
    ano_lancamento = Column(String(60), nullable=False)
    nome_musica = Column(String(60), nullable=False)
    url_img = Column(String(255), nullable=True)

    def __repr__(self):
        return (f"<albuns(id={self.id}, nome='{self.nome}', artista='{self.artista}', "
                f"ano_lancamento='{self.ano_lancamento}'), nome_musica='{self.nome_musica}'>, url_img='{self.url_img}'>")

class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(60), nullable=False)
    email = Column(String(120), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)

    def __repr__(self):
        return (
            f"<Usuario(id={self.id}, nome='{self.nome}', "
            f"email='{self.email}', senha='{self.senha}')>"
        )

class Avaliacao(Base):
    __tablename__ = 'avaliacao'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    id_musica = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"<Avaliacao(id={self.id}, id_usuario='{self.id_usuario}', id_musica='{self.id_musica}')>")

    # cria a tabela se ainda não existir
    if __name__ == "__main__":
        Base.metadata.create_all(engine)