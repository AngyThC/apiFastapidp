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

class TipoIncidenciaCreate(BaseModel):
    nombreIncidencia: str

class IncidenciaCreate(BaseModel):
    idTipoIncidencia: int
    comentario: str
    fecha: str
    usuarioId: int

class FotografiaIncidenciaCreate(BaseModel):
    foto: bytes
    fecha: str
    idUbicacion: int
    idIncidencia: int