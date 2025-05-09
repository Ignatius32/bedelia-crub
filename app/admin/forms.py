from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, IntegerField, TextAreaField, SubmitField, SelectMultipleField, DateField, TimeField, HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError
from datetime import date
from app.services.api import materia_service

class EquipoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 64)])
    fijo = BooleanField('Fijo')
    estado = SelectField('Estado', choices=[('activo', 'Activo'), ('inactivo', 'Inactivo')], validators=[DataRequired()])
    submit = SubmitField('Guardar')

class EspacioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 64)])
    ubicacion = StringField('Ubicación', validators=[DataRequired(), Length(1, 128)])
    aforo = IntegerField('Aforo', validators=[DataRequired(), NumberRange(min=1)])
    equipo_id = SelectField('Equipo', coerce=int, validators=[Optional()])
    estado = SelectField('Estado', choices=[
        ('disponible', 'Disponible'),
        ('mantenimiento', 'En Mantenimiento'),
        ('inactivo', 'Inactivo')
    ], validators=[DataRequired()])
    tipo_espacio = SelectField('Tipo de Espacio', choices=[
        ('aula', 'Aula'),
        ('laboratorio', 'Laboratorio'),
        ('sala', 'Sala de Conferencias'),
        ('otro', 'Otro')
    ], validators=[DataRequired()])
    submit = SubmitField('Guardar')

class TipoActividadForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(1, 64)])
    submit = SubmitField('Guardar')

class ActividadForm(FlaskForm):
    tipo_actividad_id = SelectField('Tipo de Actividad', coerce=int, validators=[DataRequired()])
    espacio_id = SelectField('Espacio', coerce=int, validators=[DataRequired()])
    dias = SelectMultipleField('Días', choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'),
        ('Miércoles', 'Miércoles'),
        ('Jueves', 'Jueves'),
        ('Viernes', 'Viernes'),
        ('Sábado', 'Sábado'),
        ('Domingo', 'Domingo')
    ], validators=[DataRequired()])
    frecuencia = SelectField('Frecuencia', choices=[
        ('semanal', 'Semanal'),
        ('quincenal', 'Quincenal'),
        ('mensual', 'Mensual'),
        ('unica', 'Única')
    ], validators=[DataRequired()])
    fecha_desde = DateField('Fecha Desde', validators=[DataRequired()])
    fecha_hasta = DateField('Fecha Hasta', validators=[DataRequired()])    
    horario_desde = TimeField('Horario Desde', validators=[DataRequired()])
    horario_hasta = TimeField('Horario Hasta', validators=[DataRequired()])
    equipamiento_extra = TextAreaField('Equipamiento Extra', validators=[Optional()])
    asignatura_id = SelectField('Asignatura', coerce=int, validators=[DataRequired()])
    asignatura_info = HiddenField('Información de la Asignatura')  # Campo oculto para almacenar la información completa
    submit = SubmitField('Guardar')
    
    def validate_fecha_hasta(self, field):
        if field.data < self.fecha_desde.data:
            raise ValidationError('La fecha de finalización debe ser posterior a la fecha de inicio.')
    
    def validate_horario_hasta(self, field):
        if field.data <= self.horario_desde.data:
            raise ValidationError('El horario de finalización debe ser posterior al horario de inicio.')
