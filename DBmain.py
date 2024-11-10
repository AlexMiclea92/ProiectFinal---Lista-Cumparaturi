from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base
import pymysql

hostname = "127.0.0.1"
username = "root"
password = ""
port = 3306
database = "lista_cumparaturi"

conex = pymysql.connect(host=hostname, user=username, password=password, port=port)
cursor = conex.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database};")
cursor.close()
conex.close()

DATABASE_URI = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database}'
engine = create_engine(DATABASE_URI)

Base = declarative_base()

class Produs(Base):
    __tablename__ = 'Produs'
    id = Column(Integer, primary_key=True)
    nume = Column(String(150), nullable=False)
    cumparat = Column(Boolean, nullable=False, default=False)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def populate_list():
    produse = [
        {'nume': 'Cartofi'},
        {'nume': 'Ceapa'},
        {'nume': 'Usturoi'},
        {'nume': 'Ardei gras'},
        {'nume': 'Ardei iute'},
        {'nume': 'Rosii'},
        {'nume': 'Castraveti'},
        {'nume': 'Marar'},
        {'nume': 'Conopida'},
        {'nume': 'Morcov'}
    ]
    for produs in produse:
        produs_existent = session.query(Produs).filter_by(nume = produs['nume']).first()
        if not produs_existent:
            produs = Produs(nume= produs['nume'])
            session.add(produs)

    session.commit()
    print('Lista de cumparaturi a fost populata cu success!')

populate_list()