from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    user: str
    contrasenia: str

class UbicacionCreate(BaseModel):
    nombreUbicacion: str
    descripcion: str
    latitud: float
    longitud: float

class TipoMantenimientoCreate(BaseModel):
    nombreMantenimiento: str

class MantenimientoCreate(BaseModel):
    comentario: str
    fecha: str
    tipoId: int
    userId: int
    ubicacionId: int

class FotografiaMantenimientoCreate(BaseModel):
    foto: bytes
    fecha: str
    idMantenimiento: int
    latitud: float  # Nuevo campo
    longitud: float  # Nuevo campo

class TipoIncidenciaCreate(BaseModel):
    nombreIncidencia: str

class IncidenciaCreate(BaseModel):
    comentario: str
    fecha: str
    userId: int
    tipoIncidenciaId: int
    ubicacionId: int

class FotografiaIncidenciaCreate(BaseModel):
    foto: str  # Cambiado de bytes a str
    fecha: str  # Puedes cambiar fecha a datetime para que FastAPI lo parse automáticamente
    incidenciaId: int
    latitud: float
    longitud: float