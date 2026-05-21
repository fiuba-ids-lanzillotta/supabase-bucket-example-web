# Supabase Bucket Example - Web

> **Aviso:** este proyecto es **codigo de ejemplo** con fines didacticos. Puede contener errores, simplificaciones o decisiones de diseno discutibles. Si se usa como base para un trabajo practico u otro entregable, **debe adaptarse a las buenas practicas y consignas especificas de la materia/catedra** (estilo de codigo, manejo de errores, validaciones, tests, estructura, etc.).

## Motivacion

Este proyecto es el **frontend** del ejemplo practico de como integrar [Supabase Storage](https://supabase.com/docs/guides/storage) para **subir imagenes a un bucket**.

Proporciona un formulario de registro de mascotas con subida de foto (drag & drop), un carousel para navegar las mascotas disponibles, y una pagina de detalle. La imagen se envia al backend (`supabase-bucket-example-api`) que se encarga de subirla al bucket de Supabase.

El objetivo es mostrar como un frontend puede delegar la subida de archivos a una API, manteniendo la separacion de responsabilidades.

## Arquitectura

```
  Browser
     |
     v
  Flask Web (este proyecto, puerto 5001)
     |
     |  requests.get/post (HTTP)
     v
  Flask API (supabase-bucket-example-api, puerto 5000)
     |
     |--- Imagen ---> Supabase Storage
     |--- Datos  ---> MySQL
```

## Estructura del proyecto

```
supabase-bucket-example-web/
├── app.py                          # Entry point Flask (puerto 5001)
├── requirements.txt                # Dependencias Python
├── bucket_example_web/
│   ├── constants.py                # URL de la API backend
│   ├── routes/
│   │   └── mascotas.py             # Rutas: home, detalle, nueva mascota
│   └── services/
│       └── mascotas.py             # Cliente HTTP para consumir la API
├── templates/
│   ├── base.html                   # Template base (header, footer, nav)
│   ├── home.html                   # Carousel de mascotas disponibles
│   ├── detalle.html                # Pagina de detalle de una mascota
│   └── nueva_mascota.html          # Formulario de registro con subida de imagen
└── static/
    ├── css/
    │   └── styles.css              # Estilos responsive
    └── img/
        └── placeholder.svg         # Imagen fallback
```

## Requisitos previos

- Python 3.10+
- La API (`supabase-bucket-example-api`) corriendo en el puerto 5000

## Instalacion y ejecucion

El proyecto incluye scripts de setup que crean el entorno virtual, instalan las dependencias y levantan la aplicacion automaticamente.

Asegurate de que la API este corriendo primero, luego:

**Con virtualenv:**

```bash
# Windows
setup_virtualenv.bat

# Linux / macOS
chmod +x setup_virtualenv.sh
./setup_virtualenv.sh
```

**Con pipenv:**

```bash
# Windows
setup_pipenv.bat

# Linux / macOS
chmod +x setup_pipenv.sh
./setup_pipenv.sh
```

Una vez iniciada, la web estara disponible en `http://localhost:5001/mascotas`

## Paginas

| Ruta                 | Descripcion                                      |
|----------------------|--------------------------------------------------|
| `/mascotas`          | Home con carousel de mascotas disponibles         |
| `/mascota/<id>`      | Detalle de una mascota                            |
| `/mascotas/nueva`    | Formulario para registrar una mascota con foto    |

## Flujo del formulario

1. El usuario completa los datos y selecciona una imagen (drag & drop o click)
2. El frontend valida los campos localmente
3. Si es valido, envia todo al backend via `multipart/form-data`
4. La API sube la imagen al bucket de Supabase y guarda los datos en MySQL
5. Si todo sale bien, redirige al home con la nueva mascota visible

## Glosario de terminos

- **API REST**: estilo de arquitectura para servicios web que expone recursos via HTTP (GET, POST, PUT, DELETE) usando, en general, JSON como formato de intercambio.
- **Endpoint**: ruta concreta de la API (por ejemplo `POST /mascotas`) que responde a un metodo HTTP y realiza una accion sobre un recurso.
- **Body**: contenido (payload) de una request o response. En el formulario de alta de mascota se envia como `multipart/form-data`.
- **JSON**: formato de texto para representar datos estructurados (objetos y arrays). Es el formato usado para las respuestas de la API.
- **Flask**: micro framework web de Python. En este ejemplo se usa tanto en el frontend (este proyecto) como en la API backend.
- **Frontend**: aplicacion que renderiza las paginas HTML del lado del servidor y consume la API. En este proyecto corre en el puerto 5001.
- **Backend / API**: servicio HTTP REST (`supabase-bucket-example-api`) que expone los endpoints de mascotas y se encarga de subir las imagenes a Supabase. Corre en el puerto 5000.
- **Blueprint (Flask)**: mecanismo de Flask para agrupar rutas relacionadas en modulos (por ejemplo `routes/mascotas.py`).
- **Service**: capa con la logica de invocacion a la API (cliente HTTP). Vive en `services/` y es invocada desde las routes.
- **SSR (Server-Side Rendering)**: renderizado del HTML en el servidor (con Jinja2) antes de enviarlo al navegador. Es el enfoque usado en este frontend.
- **SPA (Single Page Application)**: alternativa al SSR donde el frontend corre como JavaScript en el navegador y consume la API directamente. **No** es lo que hace este proyecto.
- **Jinja2**: motor de templates que usa Flask para generar HTML dinamico (los archivos `.html` en `templates/`).
- **Template base (`base.html`)**: plantilla con la estructura comun (header, footer, flash) de la que heredan las demas paginas.
- **Flash message**: mensaje temporal de una sola lectura que Flask muestra al usuario tras una accion (exito o error).
- **`requests`**: libreria de Python que el frontend usa para hacer llamadas HTTP a la API.
- **`multipart/form-data`**: codificacion HTTP estandar para enviar formularios que contienen archivos. Se usa para subir la foto de la mascota al backend.
- **Drag & drop**: interaccion del navegador que permite arrastrar un archivo desde el sistema operativo y soltarlo en un elemento HTML para subirlo. Se implementa en `static/js/upload.js`.
- **Carousel**: componente UI que muestra una lista de items navegables (en este caso, mascotas disponibles).
- **Imagen fallback (`placeholder.svg`)**: imagen generica que se muestra cuando la mascota no tiene foto o la URL falla.
- **Supabase**: plataforma backend-as-a-service que combina PostgreSQL, autenticacion, Storage (buckets) y otros servicios. En este ejemplo se usa solo PostgreSQL + Storage.
- **Bucket (Supabase Storage)**: contenedor de archivos publico o privado donde se almacenan las imagenes subidas por la API.
- **Entorno virtual**: directorio aislado con la version de Python y las dependencias del proyecto, para no mezclarlas con las del sistema.
- **virtualenv / `venv`**: herramienta estandar de Python para crear entornos virtuales. Las dependencias se declaran en `requirements.txt` y se instalan con `pip install -r requirements.txt`. En este proyecto lo levantan los scripts `setup_virtualenv.sh` / `setup_virtualenv.bat`.
- **pipenv**: herramienta alternativa que combina la gestion del entorno virtual con la de dependencias en un solo flujo. Usa `Pipfile` (declaracion) y `Pipfile.lock` (versiones exactas resueltas) en vez de `requirements.txt`. En este proyecto lo levantan los scripts `setup_pipenv.sh` / `setup_pipenv.bat`.
- **`pip`**: gestor de paquetes de Python. Instala librerias desde PyPI dentro del entorno activo.
