import inspect
import sqlalchemy
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import relationship
from sqlalchemy import Column, inspect, create_engine
from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    cpf = Column(String)
    endereco = Column(String)

    address = relationship(
        "Address", back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, cpf={self.cpf}, endereco={self.endereco})"


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(String)
    num = Column(Integer)
    id_cliente = Column(Integer, ForeignKey('user_account.id'), nullable=False)
    saldo = Column(Float)

    user = relationship("User", back_populates='address')

    def __repr__(self):
        return f"Address(id={self.id}, tipo={self.tipo}, agencia={self.agencia}, num={self.num}, saldo={self.saldo})"


print(User.__tablename__)

engine = create_engine("sqlite://")

Base.metadata.create_all(engine)

inspect_engine = inspect(engine)
print(inspect_engine.has_table("user_account"))
print(inspect_engine.get_table_names())

Session = sessionmaker(bind=engine)

with Session() as session:
    Aldecir = User(
        name='Aldecir',
        cpf='101.101.010-00',
        endereco='Rua das Flores',
        address=[Address(agencia='01', saldo='500')]
    )

    session.add_all([Aldecir])

    session.commit()

Session = sessionmaker(bind=engine)
session = Session()

users = session.query(User).all()
for user in users:
    print(
        f"ID: {user.id}, Nome: {user.name}, CPF: {user.cpf}, Endereço: {user.endereco}")
    for address in user.address:
        print(f"  Agência: {address.agencia}, Saldo: {address.saldo}")

session.close()
