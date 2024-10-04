from fastapi import FastAPI, HTTPException, Request, Depends
from sqlalchemy.orm import sessionmaker
from models import Base, Usuarios, Ubicaciones, TipoMantenimiento, Mantenimiento, FotografiasMantenimiento, TipoIncidencia, Incidencias, FotografiasIncidencia
from schemas import UsuarioCreate, UbicacionCreate, TipoMantenimientoCreate, MantenimientoCreate, FotografiaMantenimientoCreate, TipoIncidenciaCreate, IncidenciaCreate, FotografiaIncidenciaCreate
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
import base64
from fastapi import  UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

app = FastAPI()

#LOGIN

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()

# Aquí está tu código para manejar las imágenes...
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica los dominios que deseas permitir
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/mantenimientodm"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password

    user = db.query(Usuarios).filter(Usuarios.user == username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    if not verify_password(password, user.contrasenia):
        raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

    return {"message": "Inicio de sesión exitoso", "userId": user.userId}

# CODIGO DE IMAGENES =================================================================

# Rutas para Usuarios
@app.get("/usuarios/")
def read_usuarios():
    usuariosa = db.query(Usuarios).all()
    return usuariosa

@app.post("/usuarios/create")
def create_usuario(usuario: UsuarioCreate):
    hashed_password = get_password_hash(usuario.contrasenia)
    db_usuario = Usuarios(user=usuario.user, contrasenia=hashed_password)
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
@app.get("/fotografiasmantenimiento/{mantenimientoId}")
def read_fotografiasmantenimiento(mantenimiento_Id: int):
    # Código para obtener fotografías...
    fotografias = db.query(FotografiasMantenimiento).filter_by(mantenimientoId=mantenimiento_Id).all()
    if not fotografias:
        raise HTTPException(status_code=404, detail="No se encontraron fotografías para este mantenimiento.")

    # Formatear la respuesta
    response = []
    for fotografia in fotografias:
        print(f"Fotografía ID: {fotografia.idFotografia}, Base64: {fotografia.foto[:30]}...")  # Log para verificar
        response.append({
            "fotoManId": fotografia.fotoManId,
            "fecha": fotografia.fecha,
            "foto": fotografia.foto,  # Verifica que esto contenga los datos en base64
            "mantenimientoId": fotografia.mantenimientoId
        })
    
    return response


def agregar_padding_base64(foto_base64: str):
    return foto_base64 + '=' * (-len(foto_base64) % 4)

@app.post("/fotografiasmantenimiento/create")
async def crear_fotografia(request: Request):
    datos = await request.json()
    foto = datos.get("foto")
    fecha = datos.get("fecha")
    mantenimientoId = datos.get("mantenimientoId")
    latitud = datos.get("latitud")
    longitud = datos.get("longitud")

    # Validar que el id de mantenimiento no sea None
    if mantenimientoId is None:
        raise HTTPException(status_code=400, detail="mantenimientoId es requerido")

    # Mostrar los datos recibidos en la terminal
    print("Datos recibidos desde Android Studio:")
    print(f"Foto (base64): {foto[:30]}...")  # Solo los primeros 30 caracteres
    print(f"Fecha: {fecha}")
    print(f"ID Mantenimiento: {mantenimientoId}")
    print(f"Latitud: {latitud}")
    print(f"Longitud: {longitud}")

    # Guardar la imagen en el servidor si es necesario
    if foto:
        foto = agregar_padding_base64(foto)
        with open("imagen_recibida.png", "wb") as img_file:
            img_file.write(base64.b64decode(foto))

    # Guardar la fotografía en la base de datos
    nueva_fotografia = FotografiasMantenimiento(
        foto=foto,
        fecha=fecha,
        mantenimientoId=mantenimientoId,
        latitud=latitud,
        longitud=longitud
    )
    db.add(nueva_fotografia)
    db.commit()
    db.refresh(nueva_fotografia)

    return {"mensaje": "Fotografía guardada correctamente", "idFotografia": nueva_fotografia.fotoManId}


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

@app.get("/fotografiasincidencia/{incidenciaId}")
def read_fotografiasincidencia(incidenciaId: int):
    fotografias = db.query(FotografiasIncidencia).filter_by(incidenciaId=incidenciaId).all()
    if not fotografias:
        raise HTTPException(status_code=404, detail="No se encontraron fotografías para esta incidencia.")
    
    response = []
    for fotografia in fotografias:
        print(f"Fotografía ID: {fotografia.fotoId}, Base64: {fotografia.foto[:30]}...")  # Log para verificar
        response.append({
            "fotoId": fotografia.fotoId,
            "fecha": fotografia.fecha,
            "foto": fotografia.foto,
            "incidenciaId": fotografia.incidenciaId,
            "latitud": fotografia.latitud,
            "longitud": fotografia.longitud
        })
    
    return response

@app.post("/fotografiasincidencia/create")
def create_fotografiaincidencia(fotografiaincidencia: FotografiaIncidenciaCreate):
    # Validar que el id de incidencia no sea None
    if fotografiaincidencia.incidenciaId is None:
        raise HTTPException(status_code=400, detail="incidenciaId es requerido")

    # Mostrar los datos recibidos en la terminal
    print("Datos recibidos desde Android Studio:")
    print(f"Foto (base64): {fotografiaincidencia.foto[:30]}...")
    print(f"Fecha: {fotografiaincidencia.fecha}")
    print(f"ID Incidencia: {fotografiaincidencia.incidenciaId}")
    print(f"Latitud: {fotografiaincidencia.latitud}")
    print(f"Longitud: {fotografiaincidencia.longitud}")

    # Guardar la imagen en el servidor si es necesario
    if fotografiaincidencia.foto:
        foto = agregar_padding_base64(fotografiaincidencia.foto)
        with open("imagen_incidencia_recibida.png", "wb") as img_file:
            img_file.write(base64.b64decode(foto))

    # Guardar la fotografía en la base de datos
    nueva_fotografia = FotografiasIncidencia(
        foto=fotografiaincidencia.foto,
        fecha=fotografiaincidencia.fecha,
        incidenciaId=fotografiaincidencia.incidenciaId,
        latitud=fotografiaincidencia.latitud,
        longitud=fotografiaincidencia.longitud
    )
    db.add(nueva_fotografia)
    db.commit()
    db.refresh(nueva_fotografia)

    return {"mensaje": "Fotografía de incidencia guardada correctamente", "idFotografia": nueva_fotografia.fotoId}