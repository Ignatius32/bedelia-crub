from app import db
from datetime import datetime
import json

class Actividad(db.Model):
    __tablename__ = 'actividades'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo_actividad_id = db.Column(db.Integer, db.ForeignKey('tipo_actividades.id'), nullable=False)
    espacio_id = db.Column(db.Integer, db.ForeignKey('espacios.id'), nullable=False)
    dias = db.Column(db.String(64), nullable=False)  # Por ejemplo: "Lunes,Miércoles,Viernes"
    frecuencia = db.Column(db.String(20), nullable=False)  # Por ejemplo: "semanal", "quincenal"
    fecha_desde = db.Column(db.Date, nullable=False)
    fecha_hasta = db.Column(db.Date, nullable=False)
    horario_desde = db.Column(db.Time, nullable=False)
    horario_hasta = db.Column(db.Time, nullable=False)
    equipamiento_extra = db.Column(db.Text)
    asignatura = db.Column(db.String(100), nullable=True)  # Nombre de la asignatura (opcional)
    asignatura_id = db.Column(db.Integer, nullable=True)
    asignatura_info = db.Column(db.Text, nullable=True) # Almacena la información completa de la asignatura en formato JSON (opcional)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
      # Relaciones
    tipo_actividad = db.relationship('TipoActividad')
    espacio = db.relationship('Espacio')
    @property
    def carrera(self):
        """Obtiene el nombre de la carrera de la asignatura"""
        if self.asignatura_info:
            try:
                info = json.loads(self.asignatura_info)
                return info.get('nombre_carrera', '')
            except:
                return ''
        return ''
    
    @property
    def materia_detalles(self):
        """Obtiene detalles formateados de la materia"""
        if self.asignatura_info:
            try:
                info = json.loads(self.asignatura_info)
                return {
                    'nombre': info.get('nombre_materia', ''),
                    'carrera': info.get('nombre_carrera', ''),
                    'plan': info.get('plan_guarani', ''),
                    'departamento': info.get('depto', ''),
                    'ano_plan': info.get('ano_plan', ''),
                    'horas': info.get('horas_totales', '')
                }
            except:
                return {}
        return {}
    
    def __repr__(self):
        return f'<Actividad {self.id}: {self.asignatura}>'
