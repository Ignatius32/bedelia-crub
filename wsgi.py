from app import create_app, db
from app.models.user import User
from app.models.equipos import Equipo
from app.models.espacios import Espacio
from app.models.tipo_actividades import TipoActividad
from app.models.actividades import Actividad

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Equipo': Equipo, 
        'Espacio': Espacio, 
        'TipoActividad': TipoActividad, 
        'Actividad': Actividad
    }
