from flask import Blueprint, render_template, request, redirect, url_for
from ..services.mascotas import (
    obtener_mascotas_disponibles,
    obtener_mascota_por_id,
    crear_mascota,
)
from ..constants import ESPECIES_VALIDAS, SEXOS_VALIDOS, MAX_FILE_SIZE_MB

mascotas_bp = Blueprint('mascotas', __name__)


@mascotas_bp.route('/mascotas')
def index():
    """Pagina principal con el carrousel de mascotas en adopcion."""
    mascotas = obtener_mascotas_disponibles()

    return render_template('home.html', mascotas=mascotas)


@mascotas_bp.route('/mascota/<int:id>')
def detalle_mascota(id):
    """Pagina de detalle de una mascota."""
    mascota = obtener_mascota_por_id(id)
    
    return render_template('detalle.html', mascota=mascota)


@mascotas_bp.route('/mascotas/nueva', methods=['GET', 'POST'])
def nueva_mascota():
    """Formulario para registrar una nueva mascota."""
    if request.method == 'GET':
        return render_template(
            'nueva_mascota.html',
            especies=sorted(ESPECIES_VALIDAS),
            sexos=sorted(SEXOS_VALIDOS),
        )

    # --- Procesar el POST ---
    errores = []

    nombre        = request.form.get('nombre', '').strip()
    especie       = request.form.get('especie', '').strip()
    raza          = request.form.get('raza', '').strip()
    edad_meses    = request.form.get('edad_meses', '').strip()
    sexo          = request.form.get('sexo', '').strip()
    descripcion   = request.form.get('descripcion', '').strip()
    fecha_ingreso = request.form.get('fecha_ingreso', '').strip()
    archivo       = request.files.get('imagen')

    # Validaciones basicas en el frontend antes de enviar al backend
    if not nombre:
        errores.append('El nombre es obligatorio.')
    if especie.lower() not in ESPECIES_VALIDAS:
        errores.append('La especie seleccionada no es valida.')
    if not raza:
        errores.append('La raza es obligatoria.')
    if not edad_meses:
        errores.append('La edad en meses es obligatoria.')
    else:
        try:
            edad_val = int(edad_meses)
            if edad_val < 0:
                errores.append('La edad en meses debe ser mayor o igual a 0.')
        except ValueError:
            errores.append('La edad en meses debe ser un numero entero.')
    if sexo.lower() not in SEXOS_VALIDOS:
        errores.append('El sexo seleccionado no es valido.')
    if not descripcion:
        errores.append('La descripcion es obligatoria.')
    if not fecha_ingreso:
        errores.append('La fecha de ingreso es obligatoria.')
    if not archivo or not archivo.filename:
        errores.append('Debes seleccionar una imagen.')

    if errores:
        return render_template(
            'nueva_mascota.html',
            especies=sorted(ESPECIES_VALIDAS),
            sexos=sorted(SEXOS_VALIDOS),
            errores=errores,
            form=request.form,
        )

    # Enviar datos + imagen al backend (la API se encarga de subir al bucket)
    form_data = {
        'nombre':        nombre,
        'especie':       especie,
        'raza':          raza,
        'edad_meses':    edad_meses,
        'sexo':          sexo,
        'descripcion':   descripcion,
        'fecha_ingreso': fecha_ingreso,
    }

    resultado = crear_mascota(form_data, archivo)

    if 'errores' in resultado:
        return render_template(
            'nueva_mascota.html',
            especies=sorted(ESPECIES_VALIDAS),
            sexos=sorted(SEXOS_VALIDOS),
            errores=resultado['errores'],
            form=request.form,
        )

    return redirect(url_for('mascotas.index'))
