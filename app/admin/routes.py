from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.admin import admin
from app.models.user import User
from app.models.equipos import Equipo
from app.models.espacios import Espacio
from app.models.tipo_actividades import TipoActividad
from app.models.actividades import Actividad
from app.admin.forms import EquipoForm, EspacioForm, TipoActividadForm, ActividadForm
from app.services.api import materia_service
from datetime import datetime, timedelta
import json

# Decorador personalizado para verificar si el usuario es administrador
def admin_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Acceso denegado. Se requieren permisos de administrador.')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Ruta principal del panel de administración
@admin.route('/')
@admin_required
def index():
    return render_template('admin/index.html')

# --- CRUD para Equipos ---
@admin.route('/equipos')
@admin_required
def equipos_list():
    equipos = Equipo.query.all()
    return render_template('admin/equipos/list.html', equipos=equipos)

@admin.route('/equipos/create', methods=['GET', 'POST'])
@admin_required
def equipos_create():
    form = EquipoForm()
    if form.validate_on_submit():
        equipo = Equipo(
            nombre=form.nombre.data,
            fijo=form.fijo.data,
            estado=form.estado.data
        )
        db.session.add(equipo)
        db.session.commit()
        flash('Equipo creado exitosamente.')
        return redirect(url_for('admin.equipos_list'))
    return render_template('admin/equipos/create.html', form=form)

@admin.route('/equipos/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def equipos_edit(id):
    equipo = Equipo.query.get_or_404(id)
    form = EquipoForm(obj=equipo)
    if form.validate_on_submit():
        equipo.nombre = form.nombre.data
        equipo.fijo = form.fijo.data
        equipo.estado = form.estado.data
        db.session.commit()
        flash('Equipo actualizado exitosamente.')
        return redirect(url_for('admin.equipos_list'))
    return render_template('admin/equipos/edit.html', form=form, equipo=equipo)

@admin.route('/equipos/delete/<int:id>', methods=['POST'])
@admin_required
def equipos_delete(id):
    equipo = Equipo.query.get_or_404(id)
    db.session.delete(equipo)
    db.session.commit()
    flash('Equipo eliminado exitosamente.')
    return redirect(url_for('admin.equipos_list'))

# --- CRUD para Espacios ---
@admin.route('/espacios')
@admin_required
def espacios_list():
    espacios = Espacio.query.all()
    return render_template('admin/espacios/list.html', espacios=espacios)

@admin.route('/espacios/create', methods=['GET', 'POST'])
@admin_required
def espacios_create():
    form = EspacioForm()
    # Cargar opciones de equipos
    form.equipo_id.choices = [(e.id, e.nombre) for e in Equipo.query.filter_by(estado='activo').all()]
    form.equipo_id.choices.insert(0, (0, 'Sin equipo asignado'))
    
    if form.validate_on_submit():
        espacio = Espacio(
            nombre=form.nombre.data,
            ubicacion=form.ubicacion.data,
            aforo=form.aforo.data,
            equipo_id=form.equipo_id.data if form.equipo_id.data != 0 else None,
            estado=form.estado.data,
            tipo_espacio=form.tipo_espacio.data
        )
        db.session.add(espacio)
        db.session.commit()
        flash('Espacio creado exitosamente.')
        return redirect(url_for('admin.espacios_list'))
    return render_template('admin/espacios/create.html', form=form)

@admin.route('/espacios/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def espacios_edit(id):
    espacio = Espacio.query.get_or_404(id)
    form = EspacioForm(obj=espacio)
    # Cargar opciones de equipos
    form.equipo_id.choices = [(e.id, e.nombre) for e in Equipo.query.filter_by(estado='activo').all()]
    form.equipo_id.choices.insert(0, (0, 'Sin equipo asignado'))
    
    if form.validate_on_submit():
        espacio.nombre = form.nombre.data
        espacio.ubicacion = form.ubicacion.data
        espacio.aforo = form.aforo.data
        espacio.equipo_id = form.equipo_id.data if form.equipo_id.data != 0 else None
        espacio.estado = form.estado.data
        espacio.tipo_espacio = form.tipo_espacio.data
        db.session.commit()
        flash('Espacio actualizado exitosamente.')
        return redirect(url_for('admin.espacios_list'))
    return render_template('admin/espacios/edit.html', form=form, espacio=espacio)

@admin.route('/espacios/delete/<int:id>', methods=['POST'])
@admin_required
def espacios_delete(id):
    espacio = Espacio.query.get_or_404(id)
    db.session.delete(espacio)
    db.session.commit()
    flash('Espacio eliminado exitosamente.')
    return redirect(url_for('admin.espacios_list'))

# --- CRUD para Tipos de Actividades ---
@admin.route('/tipo-actividades')
@admin_required
def tipo_actividades_list():
    tipos = TipoActividad.query.all()
    return render_template('admin/tipo_actividades/list.html', tipos=tipos)

@admin.route('/tipo-actividades/create', methods=['GET', 'POST'])
@admin_required
def tipo_actividades_create():
    form = TipoActividadForm()
    if form.validate_on_submit():
        tipo = TipoActividad(nombre=form.nombre.data)
        db.session.add(tipo)
        db.session.commit()
        flash('Tipo de actividad creado exitosamente.')
        return redirect(url_for('admin.tipo_actividades_list'))
    return render_template('admin/tipo_actividades/create.html', form=form)

@admin.route('/tipo-actividades/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def tipo_actividades_edit(id):
    tipo = TipoActividad.query.get_or_404(id)
    form = TipoActividadForm(obj=tipo)
    if form.validate_on_submit():
        tipo.nombre = form.nombre.data
        db.session.commit()
        flash('Tipo de actividad actualizado exitosamente.')
        return redirect(url_for('admin.tipo_actividades_list'))
    return render_template('admin/tipo_actividades/edit.html', form=form, tipo=tipo)

@admin.route('/tipo-actividades/delete/<int:id>', methods=['POST'])
@admin_required
def tipo_actividades_delete(id):
    tipo = TipoActividad.query.get_or_404(id)
    db.session.delete(tipo)
    db.session.commit()
    flash('Tipo de actividad eliminado exitosamente.')
    return redirect(url_for('admin.tipo_actividades_list'))

# --- CRUD para Actividades ---
@admin.route('/actividades')
@admin_required
def actividades_list():
    actividades = Actividad.query.all()
    return render_template('admin/actividades/list.html', actividades=actividades)

@admin.route('/actividades/create', methods=['GET', 'POST'])
@admin_required
def actividades_create():
    form = ActividadForm()
    # Cargar opciones para el formulario
    form.tipo_actividad_id.choices = [(t.id, t.nombre) for t in TipoActividad.query.all()]
    form.espacio_id.choices = [(e.id, f"{e.nombre} - {e.ubicacion}") for e in Espacio.query.filter_by(estado='disponible').all()]
    
    # En lugar de precargar todas las materias, dejaremos que se carguen dinámicamente desde JavaScript
    try:
        # Obtenemos solo las primeras 20 materias para mostrar en el select inicial
        materias = materia_service.get_materias()[:20]
        form.asignatura_id.choices = [(m['id_materia'], f"{m['nombre_materia']} - {m['nombre_carrera']}") for m in materias]
        form.asignatura_id.choices.insert(0, (0, 'Seleccione una asignatura'))
    except Exception as e:
        flash(f'Error al cargar las asignaturas: {str(e)}', 'danger')
        form.asignatura_id.choices = [(0, 'Error al cargar asignaturas')]
    
    if form.validate_on_submit():
        # Obtener la información completa de la materia seleccionada (opcional)
        materia_id = form.asignatura_id.data if form.asignatura_id.data else None
        materia_info = None
        materia_nombre = None
        if materia_id and materia_id > 0:
            try:
                materia = materia_service.get_materia_by_id(materia_id)
                if materia:
                    materia_info = json.dumps(materia)
                    materia_nombre = materia['nombre_materia']
            except Exception as e:
                flash(f'Error al obtener información de la asignatura: {str(e)}', 'warning')
        
        actividad = Actividad(
            tipo_actividad_id=form.tipo_actividad_id.data,
            espacio_id=form.espacio_id.data,
            dias=','.join(form.dias.data),
            frecuencia=form.frecuencia.data,
            fecha_desde=form.fecha_desde.data,
            fecha_hasta=form.fecha_hasta.data,
            horario_desde=form.horario_desde.data,
            horario_hasta=form.horario_hasta.data,
            equipamiento_extra=form.equipamiento_extra.data,
            asignatura=materia_nombre,
            asignatura_id=materia_id if materia_id and materia_id > 0 else None,
            asignatura_info=materia_info
        )
        db.session.add(actividad)
        db.session.commit()
        flash('Actividad creada exitosamente.')
        return redirect(url_for('admin.actividades_list'))
    return render_template('admin/actividades/create.html', form=form)

@admin.route('/actividades/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def actividades_edit(id):
    actividad = Actividad.query.get_or_404(id)
    form = ActividadForm(obj=actividad)
    
    # Cargar opciones para el formulario
    form.tipo_actividad_id.choices = [(t.id, t.nombre) for t in TipoActividad.query.all()]
    form.espacio_id.choices = [(e.id, f"{e.nombre} - {e.ubicacion}") for e in 
                               Espacio.query.filter(
                                   (Espacio.estado=='disponible') | (Espacio.id==actividad.espacio_id)
                               ).all()]
    
    # Si el formulario ya tiene datos previos de días, convertirlos a lista
    if request.method == 'GET' and actividad.dias:
        form.dias.data = actividad.dias.split(',')
    
    # Cargar opciones de asignaturas
    try:
        # Obtenemos solo las primeras 20 materias para mostrar en el select inicial
        materias = materia_service.get_materias()[:20]
        form.asignatura_id.choices = [(m['id_materia'], f"{m['nombre_materia']} - {m['nombre_carrera']}") for m in materias]
        form.asignatura_id.choices.insert(0, (0, 'Seleccione una asignatura'))
        
        # Si la actividad ya tiene una asignatura_id, asegurarse de que esté en las opciones
        if actividad.asignatura_id and actividad.asignatura_id > 0:
            materia_actual = materia_service.get_materia_by_id(actividad.asignatura_id)
            if materia_actual:
                existing_ids = [id for id, _ in form.asignatura_id.choices]
                if actividad.asignatura_id not in existing_ids:
                    form.asignatura_id.choices.append((
                        materia_actual['id_materia'], 
                        f"{materia_actual['nombre_materia']} - {materia_actual['nombre_carrera']}"
                    ))
                form.asignatura_id.data = actividad.asignatura_id
    except Exception as e:
        flash(f'Error al cargar las asignaturas: {str(e)}', 'danger')
        form.asignatura_id.choices = [(0, 'Error al cargar asignaturas')]
        if actividad.asignatura_id:
            form.asignatura_id.choices.append((actividad.asignatura_id, actividad.asignatura))
            form.asignatura_id.data = actividad.asignatura_id
    
    if form.validate_on_submit():
        # Obtener la información completa de la materia seleccionada (opcional)
        materia_id = form.asignatura_id.data if form.asignatura_id.data else None
        materia_info = None
        materia_nombre = actividad.asignatura  # Valor predeterminado
        if materia_id and materia_id > 0:
            try:
                materia = materia_service.get_materia_by_id(materia_id)
                if materia:
                    materia_info = json.dumps(materia)
                    materia_nombre = materia['nombre_materia']
            except Exception as e:
                flash(f'Error al obtener información de la asignatura: {str(e)}', 'warning')
        
        actividad.tipo_actividad_id = form.tipo_actividad_id.data
        actividad.espacio_id = form.espacio_id.data
        actividad.dias = ','.join(form.dias.data)
        actividad.frecuencia = form.frecuencia.data
        actividad.fecha_desde = form.fecha_desde.data
        actividad.fecha_hasta = form.fecha_hasta.data
        actividad.horario_desde = form.horario_desde.data
        actividad.horario_hasta = form.horario_hasta.data
        actividad.equipamiento_extra = form.equipamiento_extra.data
        actividad.asignatura = materia_nombre
        actividad.asignatura_id = materia_id if materia_id and materia_id > 0 else None
        if materia_info:
            actividad.asignatura_info = materia_info
        else:
            actividad.asignatura_info = None
        db.session.commit()
        flash('Actividad actualizada exitosamente.')
        return redirect(url_for('admin.actividades_list'))
    return render_template('admin/actividades/edit.html', form=form, actividad=actividad)

@admin.route('/actividades/delete/<int:id>', methods=['POST'])
@admin_required
def actividades_delete(id):
    actividad = Actividad.query.get_or_404(id)
    db.session.delete(actividad)
    db.session.commit()
    flash('Actividad eliminada exitosamente.')
    return redirect(url_for('admin.actividades_list'))

# --- API para búsqueda de materias ---
@admin.route('/api/materias/search')
@admin_required
def search_materias():
    """Endpoint para búsqueda de materias desde la interfaz de administración"""
    query = request.args.get('q', '')
    if not query or len(query) < 3:
        return jsonify([])
    
    try:
        materias = materia_service.search_materias(query)
        return jsonify([{
            'id': m['id_materia'],
            'text': f"{m['nombre_materia']} - {m['nombre_carrera']}",
            'data': m
        } for m in materias])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Para mostrar las actividades por día en un calendario
@admin.route('/calendario')
@login_required
def calendario():
    # Obtener mes y año para el calendario (parámetros de URL opcionales)
    mes = request.args.get('mes', datetime.now().month, type=int)
    anio = request.args.get('anio', datetime.now().year, type=int)
    
    # Validar mes y año
    if mes < 1 or mes > 12:
        mes = datetime.now().month
    if anio < 2000 or anio > 2100:
        anio = datetime.now().year
    
    # Obtener el primer y último día del mes
    primer_dia = datetime(anio, mes, 1)
    
    # Determinar el último día del mes
    if mes == 12:
        ultimo_dia = datetime(anio + 1, 1, 1)
    else:
        ultimo_dia = datetime(anio, mes + 1, 1)
    
    # Obtener todas las actividades para el mes seleccionado
    actividades = Actividad.query.filter(
        (Actividad.fecha_desde < ultimo_dia) & 
        (Actividad.fecha_hasta >= primer_dia)
    ).all()
    
    # Organizar actividades por día
    calendario_datos = {}
    
    # Inicializar cada día del mes en el diccionario
    dias_en_mes = (ultimo_dia - primer_dia).days
    for dia in range(1, dias_en_mes + 1):
        fecha = datetime(anio, mes, dia)
        calendario_datos[dia] = {
            'fecha': fecha,
            'actividades': []
        }
    
    # Asignar actividades a los días correspondientes
    for actividad in actividades:
        # Para cada actividad, determinar los días del mes en que ocurre
        dias_semana_actividad = actividad.dias.split(',')
          # Calcular el rango de fechas relevante para el mes actual
        fecha_inicio = max(actividad.fecha_desde, primer_dia.date())
        fecha_fin = min(actividad.fecha_hasta, (ultimo_dia - timedelta(days=1)).date())
          # Para cada día en el rango, verificar si la actividad ocurre ese día
        dias_corrientes = (fecha_fin - fecha_inicio).days + 1
        for i in range(dias_corrientes):
            fecha_actual = fecha_inicio + timedelta(days=i)
            
            # Verificar si la actividad ocurre en este día de la semana
            nombre_dia = fecha_actual.strftime('%A')  # Obtener nombre del día en inglés
            # Mapeo de días en inglés a español
            mapeo_dias = {
                'Monday': 'Lunes',
                'Tuesday': 'Martes',
                'Wednesday': 'Miércoles',
                'Thursday': 'Jueves',
                'Friday': 'Viernes',
                'Saturday': 'Sábado',
                'Sunday': 'Domingo'
            }
            nombre_dia_es = mapeo_dias.get(nombre_dia)
            
            # Si la actividad ocurre en este día de la semana
            if nombre_dia_es in dias_semana_actividad:
                # Si la fecha está dentro del mes actual
                if fecha_actual.month == mes and fecha_actual.year == anio:
                    # Agregar la actividad a ese día en el calendario
                    if fecha_actual.day in calendario_datos:
                        calendario_datos[fecha_actual.day]['actividades'].append(actividad)
    
    # Determinar nombres de mes y controles de navegación
    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
             'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    nombre_mes = meses[mes - 1]
    
    # Calcular mes anterior y siguiente
    mes_anterior = mes - 1 if mes > 1 else 12
    anio_anterior = anio if mes > 1 else anio - 1
    
    mes_siguiente = mes + 1 if mes < 12 else 1
    anio_siguiente = anio if mes < 12 else anio + 1
    
    return render_template(
        'admin/calendario.html',
        calendario_datos=calendario_datos,
        anio=anio,
        mes=mes,
        nombre_mes=nombre_mes,
        mes_anterior=mes_anterior,
        anio_anterior=anio_anterior,
        mes_siguiente=mes_siguiente,
        anio_siguiente=anio_siguiente
    )
