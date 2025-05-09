from app import db

class Espacio(db.Model):
    __tablename__ = 'espacios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    ubicacion = db.Column(db.String(128), nullable=False)
    aforo = db.Column(db.Integer, nullable=False)
    equipo_id = db.Column(db.Integer, db.ForeignKey('equipos.id'))
    estado = db.Column(db.String(20), default='disponible')
    tipo_espacio = db.Column(db.String(50), nullable=False)
    
    # Relación con actividades (un espacio puede tener varias actividades)
    actividades = db.relationship('Actividad', lazy='dynamic')
    
    def __repr__(self):
        return f'<Espacio {self.nombre}>'
