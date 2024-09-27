from fastapi import FastAPI, HTTPException, Request
from sqlalchemy.orm import sessionmaker
from models import Base, Usuarios, Ubicaciones, TipoMantenimiento, Mantenimiento, FotografiasMantenimiento, TipoIncidencia, Incidencias, FotografiasIncidencia
from schemas import UsuarioCreate, UbicacionCreate, TipoMantenimientoCreate, MantenimientoCreate, FotografiaMantenimientoCreate, TipoIncidenciaCreate, IncidenciaCreate, FotografiaIncidenciaCreate
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica los dominios que deseas permitir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/mantenimientos"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Rutas para Usuarios
@app.get("/usuarios/")
def read_usuarios():
    usuariosa = db.query(Usuarios).all()
    return usuariosa

@app.post("/usuarios/create")
def create_usuario(usuario: UsuarioCreate):
    db_usuario = Usuarios(**usuario.dict())
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

# Rutas para Ubicaciones
@app.get("/ubicaciones/")
def read_ubicaciones():
    ubicaciones = db.query(Ubicaciones).all()
    return ubicaciones

@app.post("/ubicaciones/create")
def create_ubicacion(ubicacion: UbicacionCreate):
    db_ubicacion = Ubicaciones(**ubicacion.dict())
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

# Rutas para TipoMantenimiento
@app.get("/tipomantenimiento/")
def read_tipomantenimiento():
    tipomantenimiento = db.query(TipoMantenimiento).all()
    return tipomantenimiento

@app.post("/tipomantenimiento/create")
def create_tipomantenimiento(tipomantenimiento: TipoMantenimientoCreate):
    db_tipomantenimiento = TipoMantenimiento(**tipomantenimiento.dict())
    db.add(db_tipomantenimiento)
    db.commit()
    db.refresh(db_tipomantenimiento)
    return db_tipomantenimiento

# Rutas para Mantenimiento
@app.get("/mantenimiento/")
def read_mantenimiento():
    mantenimiento = db.query(Mantenimiento).all()
    return mantenimiento

@app.post("/mantenimiento/create")
def create_mantenimiento(mantenimiento: MantenimientoCreate):
    db_mantenimiento = Mantenimiento(**mantenimiento.dict())
    db.add(db_mantenimiento)
    db.commit()
    db.refresh(db_mantenimiento)
    return db_mantenimiento

# Rutas para FotografiasMantenimiento
@app.get("/fotografiasmantenimiento/{id_mantenimiento}")
def read_fotografiasmantenimiento(id_mantenimiento: int):
    # Código para obtener fotografías...
    fotografias = db.query(FotografiasMantenimiento).filter_by(idMantenimiento=id_mantenimiento).all()
    if not fotografias:
        raise HTTPException(status_code=404, detail="No se encontraron fotografías para este mantenimiento.")

    # Formatear la respuesta
    response = []
    for fotografia in fotografias:
        print(f"Fotografía ID: {fotografia.idFotografia}, Base64: {fotografia.foto[:30]}...")  # Log para verificar
        response.append({
            "idFotografia": fotografia.idFotografia,
            "fecha": fotografia.fecha,
            "foto": fotografia.foto,  # Verifica que esto contenga los datos en base64
            "idMantenimiento": fotografia.idMantenimiento
        })
    
    return response



@app.post("/fotografiasmantenimiento/create")
async def crear_fotografia(request: Request):
    datos = await request.json()
    foto = datos.get("foto")
    fecha = datos.get("fecha")
    id_mantenimiento = datos.get("idMantenimiento")

    # Verifica que se recibieron los datos
    print(f"Foto (base64): {foto[:30]}...")  # Muestra solo los primeros 30 caracteres para no llenar los logs
    print(f"Fecha: {fecha}")
    print(f"ID Mantenimiento: {id_mantenimiento}")

    # Puedes guardar la imagen si es necesario
    if foto:
        with open("imagen_recibida.png", "wb") as img_file:
            img_file.write(base64.b64decode(foto))

    return {"mensaje": "Datos recibidos"}

# Rutas para TipoIncidencia
@app.get("/tipoincidencia/")
def read_tipoincidencia():
    tipoincidencia = db.query(TipoIncidencia).all()
    return tipoincidencia

@app.post("/tipoincidencia/create")
def create_tipoincidencia(tipoincidencia: TipoIncidenciaCreate):
    db_tipoincidencia = TipoIncidencia(**tipoincidencia.dict())
    db.add(db_tipoincidencia)
    db.commit()
    db.refresh(db_tipoincidencia)
    return db_tipoincidencia

# Rutas para Incidencias
@app.get("/incidencias/")
def read_incidencias():
    incidencias = db.query(Incidencias).all()
    return incidencias

@app.post("/incidencias/create")
def create_incidencia(incidencia: IncidenciaCreate):
    db_incidencia = Incidencias(**incidencia.dict())
    db.add(db_incidencia)
    db.commit()
    db.refresh(db_incidencia)
    return db_incidencia

@app.get("/fotografiasincidencia/{id_incidencia}")
def read_fotografiasincidencia(id_incidencia: int):
    try:
        fotografias = db.query(FotografiasIncidencia).filter_by(idIncidencia=id_incidencia).all()
        if not fotografias:
            raise HTTPException(status_code=404, detail="No se encontraron fotografías para esta incidencia.")
        
        response = []
        for fotografia in fotografias:
            response.append({
                "idFotografiaInciden": fotografia.idFotografiaInciden,
                "fecha": fotografia.fecha,
                "foto": fotografia.foto,
                "idIncidencia": fotografia.idIncidencia
            })
        
        return response
    except Exception as e:
        # Registro del error
        print(f"Error al obtener fotografías: {str(e)}")
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@app.post("/fotografiasincidencia/create")
def create_fotografiaincidencia(fotografiaincidencia: FotografiaIncidenciaCreate):
    db_fotografiaincidencia = FotografiasIncidencia(**fotografiaincidencia.dict())
    db.add(db_fotografiaincidencia)
    db.commit()
    db.refresh(db_fotografiaincidencia)
    return db_fotografiaincidencia