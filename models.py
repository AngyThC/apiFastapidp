from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, DECIMAL, BLOB, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = "usuarios"
    userId = Column(Integer, primary_key=True, autoincrement=True)    
    contrasenia = Column(Text, nullable=False)
    user = Column(String(50), nullable=False)

class Ubicaciones(Base):
    __tablename__ = "ubicaciones"
    ubicacionId = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=False)

class TipoMantenimiento(Base):
    __tablename__ = "tipomantenimientos"
    tipoMantenimientoId = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"
    mantenimientoId = Column(Integer, primary_key=True, autoincrement=True)
    comentario = Column(String(255), nullable=False)
    fecha = Column(DateTime, nullable=False)
    tipoId = Column(Integer)
    userId = Column(Integer)
    ubicacionId = Column(Integer)
    

class FotografiasMantenimiento(Base):
    __tablename__ = "fotografiamantenimientos"
    fotoManId = Column(Integer, primary_key=True, autoincrement=True)
    foto = Column(Text)
    fecha = Column(DateTime, nullable=False)
    mantenimientoId = Column(Integer)
    latitud = Column(Float)  # Nuevo campo
    longitud = Column(Float)  # Nuevo campo


class TipoIncidencia(Base):
    __tablename__ = "tipoincidencias"
    tipoIncidenciaId = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

class Incidencias(Base):
    __tablename__ = "incidencias"
    incidenciaId = Column(Integer, primary_key=True, autoincrement=True)
    comentario =  Column(String(255), nullable=False)
    fecha = Column(DateTime, nullable=False)
    userId = Column(Integer)
    tipoIncidenciaId = Column(Integer)
    ubicacionId = Column(Integer)
 
class FotografiasIncidencia(Base):
    __tablename__ = "fotografiaincidencias"
    fotoId = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False)
    foto = Column(Text)  # Cambiado de BLOB a Text
    incidenciaId = Column(Integer)  # Cambiado de DECIMAL(10, 5) a Integer
    latitud = Column(Float)
    longitud = Column(Float)
