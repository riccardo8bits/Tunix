# importar bibliotecas
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# criar conexão com base de dados SQLite (simples e local)
# você pode trocar depois por MySQL se quiser
engine = create_engine('sqlite:///musicas.db', echo=True)

# configurar sessão local
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

    def __repr__(self):
        return (f"<Musica(id={self.id}, nome='{self.nome}', artista='{self.artista}', "
                f"album='{self.album}', ano_lancamento='{self.ano_lancamento}')>")

# criar tabelas (só executa se rodar esse arquivo diretamente)
if __name__ == "__main__":
    Base.metadata.create_all(engine)
