from flask import render_template
from flask_login import login_required, current_user
from app.main import main
from app.models.actividades import Actividad
from app.models.espacios import Espacio

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Obtener las últimas 5 actividades
    actividades = Actividad.query.order_by(Actividad.fecha_creacion.desc()).limit(5).all()
    
    # Obtener espacios disponibles
    espacios = Espacio.query.filter_by(estado='disponible').all()
    
    return render_template('dashboard.html', 
                          actividades=actividades, 
                          espacios=espacios)
