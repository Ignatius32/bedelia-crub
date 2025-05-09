from app import db

class Equipo(db.Model):
    __tablename__ = 'equipos'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    fijo = db.Column(db.Boolean, default=False)
    estado = db.Column(db.String(20), default='activo')
    
    # Relación con espacios (un equipo puede estar en varios espacios)
    espacios = db.relationship('Espacio', backref='equipo_asignado', lazy='dynamic')
    
    def __repr__(self):
        return f'<Equipo {self.nombre}>'
