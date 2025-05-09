# Sistema de Administración Universitaria

## Descripción
Sistema web para la gestión integral de recursos académicos universitarios, incluyendo espacios, equipamiento, actividades académicas y calendario de eventos.

## Características Principales
- **Gestión de Espacios**: Administración de aulas, laboratorios y otros espacios físicos universitarios.
- **Gestión de Equipamiento**: Control de equipos disponibles para actividades académicas.
- **Administración de Actividades**: Creación y gestión de diferentes tipos de actividades académicas.
- **Calendario Interactivo**: Visualización de actividades programadas en formato calendario.
- **Panel de Administración**: Interfaz para administradores con acciones rápidas y reportes.

## Tecnologías
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Base de Datos**: SQLite (para desarrollo)
- **Bibliotecas**: Font Awesome, SQLAlchemy (ORM)

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación
1. Clonar el repositorio:
   ```
   git clone <url-del-repositorio>
   cd bedelia
   ```

2. Crear y activar entorno virtual:
   ```
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```

4. Configurar variables de entorno:
   Crear un archivo `.env` con las siguientes variables:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=clave-secreta-unica
   DATABASE_URL=sqlite:///instance/app.db
   ```

5. Inicializar la base de datos:
   ```
   python init_db.py
   ```

6. Ejecutar migraciones:
   ```
   flask db upgrade
   ```

7. Iniciar la aplicación:
   ```
   flask run
   ```

## Estructura del Proyecto
- **/app**: Contiene la aplicación principal
  - **/admin**: Rutas y formularios del panel de administración
  - **/api**: Endpoints de la API REST
  - **/auth**: Autenticación y gestión de usuarios
  - **/main**: Rutas principales
  - **/models**: Modelos de datos (ORM)
  - **/services**: Servicios y lógica de negocio
- **/static**: Archivos estáticos (CSS, JS, imágenes)
- **/templates**: Plantillas HTML
- **/migrations**: Migraciones de la base de datos

## Uso del Sistema

### Acceso al Sistema
1. Acceder a la URL principal
2. Iniciar sesión con credenciales de usuario o administrador
3. Navegar al panel según los permisos correspondientes

### Módulos Principales
- **Panel de Control**: Resumen de actividades recientes y espacios disponibles
- **Calendario**: Visualización mensual de actividades programadas
- **Gestión de Espacios**: Creación y administración de espacios físicos
- **Gestión de Equipamiento**: Registro y control de equipos disponibles
- **Gestión de Actividades**: Programación de clases, exámenes y eventos
- **Tipos de Actividades**: Categorización de diferentes tipos de eventos académicos

## Equipo de Desarrollo
- [Tu Nombre] - Desarrollador principal

## Licencia
Este proyecto está licenciado bajo [especificar licencia]
