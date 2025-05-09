"""
Script para crear la base de datos inicial y un usuario administrador.
"""
import os
import json
from datetime import datetime, timedelta
from app import create_app, db
from app.models.user import User
from app.models.equipos import Equipo
from app.models.espacios import Espacio
from app.models.tipo_actividades import TipoActividad
from app.models.actividades import Actividad
from werkzeug.security import generate_password_hash

app = create_app()

def init_db():
    with app.app_context():
        # Borrar la base de datos si existe
        if os.path.exists('instance/app.db'):
            os.remove('instance/app.db')
            print("Base de datos anterior eliminada.")
        
        # Crear todas las tablas
        db.create_all()
        
        # Crear usuario administrador
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('adminpassword')
        db.session.add(admin)
        
        # Crear usuario estándar
        user = User(username='user', email='user@example.com')
        user.set_password('userpassword')
        db.session.add(user)
        
        # Crear algunos tipos de actividades
        tipos = [
            TipoActividad(nombre='Clase Teórica'),
            TipoActividad(nombre='Clase Práctica'),
            TipoActividad(nombre='Laboratorio'),
            TipoActividad(nombre='Seminario'),
            TipoActividad(nombre='Examen')
        ]
        db.session.add_all(tipos)
        
        # Crear algunos equipos
        equipos = [
            Equipo(nombre='Proyector Multimedia', fijo=False, estado='activo'),
            Equipo(nombre='Computadoras de Escritorio', fijo=True, estado='activo'),
            Equipo(nombre='Equipo de Sonido', fijo=False, estado='activo'),
            Equipo(nombre='Smart TV 55"', fijo=True, estado='activo')
        ]
        db.session.add_all(equipos)
        
        # Guardar cambios para obtener IDs
        db.session.commit()
        
        # Crear algunos espacios
        espacios = [
            Espacio(nombre='Aula 101', ubicacion='Edificio Central, 1er Piso', aforo=40, 
                    equipo_id=1, estado='disponible', tipo_espacio='aula'),
            Espacio(nombre='Laboratorio 1', ubicacion='Edificio de Ciencias, Planta Baja', aforo=25, 
                    equipo_id=2, estado='disponible', tipo_espacio='laboratorio'),
            Espacio(nombre='Sala de Conferencias', ubicacion='Edificio Administrativo, 2do Piso', aforo=100, 
                    equipo_id=3, estado='disponible', tipo_espacio='sala')
        ]
        db.session.add_all(espacios)
          # Guardar cambios para obtener IDs
        db.session.commit()
        
        # Ejemplo de datos de asignaturas (similar a lo que devolvería la API)
        ejemplo_asignaturas = [
            {
                "id_materia": 328,
                "nombre_carrera": "PROFESORADO EN CIENCIAS BIOLÓGICAS",
                "nombre_materia": "ECOLOGIA DE PAISAJES (OPTATIVA)",
                "ano_plan": 4,
                "periodo_plan": "2CUAT",
                "horas_totales": "160",
                "horas_semanales": "10",
                "depto_principal": "ECOLOGÍA",
                "depto": "ECOLOGÍA",
                "area": "ECOLOGÍA",
                "orientacion": "SIN ORIENTACIÓN",
                "contenidos_minimos": "NC",
                "correlativas_para_cursar": "ECOLOGIA GENERAL aprobada",
                "correlativas_para_aprobar": "ECOLOGIA GENERAL aprobada",
                "competencias": "",
                "optativa": "SI",
                "trayecto": "N/C",
                "cod_carrera": "PBIB",
                "plan_guarani": "0750",
                "version_guarani": "1820",
                "plan_mocovi": "0750/1820",
                "plan_ordenanzas": "0750/12, 0086/14 - 0307/19 - Res. CD-GAB 1205/21",
                "cod_guarani": "PB112",
                "observaciones": ""
            },
            {
                "id_materia": 329,
                "nombre_carrera": "LICENCIATURA EN CIENCIAS BIOLÓGICAS",
                "nombre_materia": "BIOLOGÍA MOLECULAR",
                "ano_plan": 3,
                "periodo_plan": "1CUAT",
                "horas_totales": "120",
                "horas_semanales": "8",
                "depto_principal": "BIOLOGÍA MOLECULAR",
                "depto": "BIOLOGÍA MOLECULAR",
                "area": "BIOLOGÍA MOLECULAR",
                "orientacion": "SIN ORIENTACIÓN",
                "contenidos_minimos": "NC",
                "correlativas_para_cursar": "GENÉTICA aprobada",
                "correlativas_para_aprobar": "GENÉTICA aprobada",
                "competencias": "",
                "optativa": "NO",
                "trayecto": "N/C",
                "cod_carrera": "LBIO",
                "plan_guarani": "0752",
                "version_guarani": "1840",
                "plan_mocovi": "0752/1840",
                "plan_ordenanzas": "0752/14, 0088/16 - 0310/19",
                "cod_guarani": "LB210",
                "observaciones": ""
            }
        ]
        
        # Crear algunas actividades con la información de asignatura
        now = datetime.now()
        actividades = [
            Actividad(
                tipo_actividad_id=1,  # Clase Teórica
                espacio_id=1,  # Aula 101
                dias="Lunes,Miércoles",
                frecuencia="semanal",
                fecha_desde=now.date(),
                fecha_hasta=(now + timedelta(days=90)).date(),
                horario_desde=datetime.strptime("10:00", "%H:%M").time(),
                horario_hasta=datetime.strptime("12:00", "%H:%M").time(),
                equipamiento_extra="Proyector y pizarra digital",
                asignatura=ejemplo_asignaturas[0]["nombre_materia"],
                asignatura_id=ejemplo_asignaturas[0]["id_materia"],
                asignatura_info=json.dumps(ejemplo_asignaturas[0])
            ),
            Actividad(
                tipo_actividad_id=2,  # Clase Práctica
                espacio_id=2,  # Laboratorio 1
                dias="Martes,Jueves",
                frecuencia="semanal",
                fecha_desde=now.date(),
                fecha_hasta=(now + timedelta(days=90)).date(),
                horario_desde=datetime.strptime("14:00", "%H:%M").time(),
                horario_hasta=datetime.strptime("16:00", "%H:%M").time(),
                equipamiento_extra="Equipamiento de laboratorio especializado",
                asignatura=ejemplo_asignaturas[1]["nombre_materia"],
                asignatura_id=ejemplo_asignaturas[1]["id_materia"],
                asignatura_info=json.dumps(ejemplo_asignaturas[1])
            )
        ]
        db.session.add_all(actividades)
        
        # Guardar todos los cambios
        db.session.commit()
        
        print('Base de datos inicializada con datos de ejemplo.')

if __name__ == '__main__':
    init_db()
