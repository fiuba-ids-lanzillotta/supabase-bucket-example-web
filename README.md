# Supabase Bucket Example - Web

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
