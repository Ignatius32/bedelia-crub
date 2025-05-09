from app import db

class TipoActividad(db.Model):
    __tablename__ = 'tipo_actividades'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False, unique=True)
    
    # Relación con actividades (un tipo de actividad puede tener varias actividades)
    actividades = db.relationship('Actividad', backref='tipo', lazy='dynamic')
    
    def __repr__(self):
        return f'<TipoActividad {self.nombre}>'
