from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Mantener sesión iniciada')
    submit = SubmitField('Iniciar sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[
        DataRequired(), Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
              'El nombre de usuario debe contener solo letras, números, puntos o guiones bajos')
    ])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(), EqualTo('password2', message='Las contraseñas deben coincidir.')
    ])
    password2 = PasswordField('Confirmar contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')
    
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Este nombre de usuario ya está en uso.')
    
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Este correo electrónico ya está registrado.')
