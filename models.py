from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, DECIMAL, BLOB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = "usuarios"
    usuarioID = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(255), nullable=False)

class Ubicaciones(Base):
    __tablename__ = "ubicaciones"
    idUbicacion = Column(Integer, primary_key=True, autoincrement=True)
    nombreUbicacion = Column(String(100), nullable=False)
    descripcion = Column(Text)
    latitud = Column(DECIMAL(10, 8))
    longitud = Column(DECIMAL(11, 8))

class TipoMantenimiento(Base):
    __tablename__ = "tipomantenimiento"
    idTipoMantenimiento = Column(Integer, primary_key=True, autoincrement=True)
    nombreMantenimiento = Column(String(100), nullable=False)

class Mantenimiento(Base):
    __tablename__ = "mantenimiento"
    idMantenimiento = Column(Integer, primary_key=True, autoincrement=True)
    idTipoMantenimiento = Column(Integer)
    idUbicacion = Column(Integer)
    comentario = Column(Text)
    fecha = Column(DateTime, nullable=False)
    usuarioId = Column(Integer)

class FotografiasMantenimiento(Base):
    __tablename__ = "fotografiasmantenimiento"
    idFotografia = Column(Integer, primary_key=True, autoincrement=True)
    foto = Column(BLOB)
    fecha = Column(DateTime, nullable=False)
    idMantenimiento = Column(Integer)

class TipoIncidencia(Base):
    __tablename__ = "tipoincidencia"
    idTipoIncidencia = Column(Integer, primary_key=True, autoincrement=True)
    nombreIncidencia = Column(String(100), nullable=False)

class Incidencias(Base):
    __tablename__ = "incidencias"
    idIncidencia = Column(Integer, primary_key=True, autoincrement=True)
    idTipoIncidencia = Column(Integer)
    comentario = Column(Text)
    fecha = Column(DateTime, nullable=False)
    usuarioId = Column(Integer)

class FotografiasIncidencia(Base):
    __tablename__ = "fotografiasincidencia"
    idFotografiaInciden = Column(Integer, primary_key=True, autoincrement=True)
    foto = Column(BLOB)
    fecha = Column(DateTime, nullable=False)
    idUbicacion = Column(Integer)
    idIncidencia = Column(Integer)