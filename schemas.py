from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    password: str

class UbicacionCreate(BaseModel):
    nombreUbicacion: str
    descripcion: str
    latitud: float
    longitud: float

class TipoMantenimientoCreate(BaseModel):
    nombreMantenimiento: str

class MantenimientoCreate(BaseModel):
    idTipoMantenimiento: int
    idUbicacion: int
    comentario: str
    fecha: str
    usuarioId: int

class FotografiaMantenimientoCreate(BaseModel):
    foto: bytes
    fecha: str
    idMantenimiento: int
    latitud: float  # Nuevo campo
    longitud: float  # Nuevo campo

class TipoIncidenciaCreate(BaseModel):
    nombreIncidencia: str

class IncidenciaCreate(BaseModel):
    idTipoIncidencia: int
    comentario: str
    fecha: str
    usuarioId: int

class FotografiaIncidenciaCreate(BaseModel):
    foto: str  # Cambiado de bytes a str
    fecha: str  # Puedes cambiar fecha a datetime para que FastAPI lo parse automáticamente
    incidenciaId: int
    latitud: float
    longitud: float