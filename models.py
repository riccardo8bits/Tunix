# importar bibliotecas
import integer
from sqlalchemy import Column, Integer, String, create_engine
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
    url_img = Column(String(255), nullable=True)

    def __repr__(self):
        return (f"<Musica(id={self.id}, nome='{self.nome}', artista='{self.artista}', "
                f"album='{self.album}', ano_lancamento='{self.ano_lancamento}'), url_img='{self.url_img}'>")

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



# cria a tabela se ainda não existir
if __name__ == "__main__":
    Base.metadata.create_all(engine)
