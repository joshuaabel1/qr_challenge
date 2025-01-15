
---

# QR Challenge

Este proyecto implementa un sistema de **generación y gestión de Códigos QR**, con autenticación JWT, registro de escaneos (almacenando IP/país/timestamp) y estadísticas. Usa **FastAPI** como framework y **PostgreSQL** para la base de datos.

## 1. Estructura del Proyecto

```
qr_challenge/
├── app/
│   ├── api/
│   │   ├── dependencies/
│   │   ├── routers/
│   │   └── schemas/
│   ├── core/
│   │   ├── config.py         <-- Aquí se configuran credenciales DB y JWT
│   │   └── ...
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   ├── session.py
│   │   └── __init__.py
│   ├── services/
│   └── main.py
├── docker-compose.yml        <-- Para levantar sólo PostgreSQL (db)
├── requirements.txt
├── Dockerfile (opcional, si quieres contenerizar también la API)
└── README.md (este archivo)
```

### Componentes principales

1. **`app/core/config.py`**: Define variables de entorno (como `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT`) y la configuración JWT.  
2. **`app/db/models.py`**: Tablas SQLAlchemy (`User`, `QRCode`, `Scan`).
3. **`app/api/routers/*`**: Endpoints de la API (Auth, QR, Scan, etc.).  
4. **`app/services/*`**: Lógica de negocio (auth_service, qr_service, scan_service).  
5. **`docker-compose.yml`**: Levanta **solo** la base de datos PostgreSQL en un contenedor (`db`).  

---

## 2. Configuración de la Base de Datos con Docker

Actualmente, el repositorio incluye un `docker-compose.yml` que crea un contenedor de **PostgreSQL**. Deberás asegurarte de que tus credenciales en `app/core/config.py` (o tu `.env`) coincidan con las de la DB que levantas.

### Pasos

1. **Edita** tu `.env` (o variables en `config.py`) según tu preferencia, por ejemplo:
   ```bash
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=mypassword
   POSTGRES_DB=qr_db
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```
   *(Si no tienes `.env`, ajusta directamente en `app/core/config.py`.)*

2. **Levanta** la base de datos con:
   ```bash
   docker-compose up db
   ```
   Esto inicializará un contenedor `postgres_container` que escucha en el puerto 5432 de tu host local.  

3. Verifica en logs PostgreSQL:
   ```
   db_1  | PostgreSQL init process complete; ready for start up.
   db_1  | Postgres is up and running...
   ```

---

## 3. Crear y Activar un Entorno Virtual (venv)

Para correr la **aplicación FastAPI** en tu máquina:

1. **Clona** el repositorio:
   ```bash
   git clone https://github.com/joshuaabel1/qr_challenge.git
   cd qr_challenge
   ```

2. **Crea** un entorno virtual (Python 3.10 recomendado):
   ```bash
   python -m venv env
   ```
3. **Activa** el entorno:
   - **Linux/Mac**:
     ```bash
     source env/bin/activate
     ```
   - **Windows**:
     ```bash
     env\Scripts\activate
     ```

4. **Instala** las dependencias:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 4. Configura tu Conexión a la DB (Localhost)

En **`app/core/config.py`** (o un `.env` que lea `config.py`), asegura que:

```python
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "mypassword"
POSTGRES_DB = "qr_db"
```

*(Ajusta si elegiste credenciales distintos en `docker-compose.yml`.)*

---

## 5. Levantar la API

Con el entorno virtual activo y la base de datos corriendo en Docker:

```bash
uvicorn app.main:app --reload
```
*(si `main.py` está en `app/main.py`; ajusta si está en otra ubicación)*

- Se abrirá en [http://127.0.0.1:8000](http://127.0.0.1:8000).
- Documentación de Swagger en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

## 6. Interactuando con la API

### a) Autenticación

- **`POST /auth/register`**: Registra un usuario (`{"email":"...","password":"..."}`).  
- **`POST /auth/login`**: Devuelve token JWT. Si tu endpoint usa `OAuth2PasswordRequestForm`, envía los campos `username/password` en form-data; si usa JSON `email/password`, ajusta en consecuencia.

### b) Gestión de Códigos QR

1. **`POST /qr/generate`**  
   - **Entrada**: `{"url": "...", "color": "...", "size": ...}`  
   - **Salida**: archivo `image/png` (descargable).  
2. **`PATCH /qr/update/{qr_uuid}`**  
   - Actualiza `color`, `size` o `url`.  
3. **`GET /qr/list`**  
   - Lista todos los QR del usuario autenticado.
4. **`GET /qr/{qr_uuid}`**  
   - Recupera un QR por UUID.

### c) Registro de Escaneos

- **`GET /scan/{qr_uuid}`**:  
  - Registra la IP, geolocaliza (si posible), y hace `302 Found` redirigiendo a la URL del QR.  
- **`GET /scan/stats/{qr_uuid}`**:  
  - Muestra las estadísticas de escaneos (IP, country, timestamp).

*(Estos endpoints exigen el encabezado `Authorization: Bearer <TOKEN>`.)*

---

## 8. Notas Finales

- Si **color** o `size` en el QR no se envían, el esquema `QRCreateRequest` maneja defaults (ej. `color="black"`, `size=8`).  
- Para IP geolocalización, en local verás `127.0.0.1`. En producción, configura un proxy que ponga la IP real en `X-Forwarded-For`.
- Revisa los logs y la doc [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) para pruebas de endpoints.

---
