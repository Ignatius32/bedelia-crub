# Instrucciones para aplicar las migraciones y actualizar la base de datos

Para aplicar las migraciones a la base de datos y actualizar su estructura con los nuevos campos para la integración de asignaturas, siga los siguientes pasos:

1. Asegúrese de estar en el directorio raíz del proyecto

2. Ejecute el siguiente comando para aplicar las migraciones:
   ```
   flask db upgrade
   ```

Si encuentra algún error durante la migración, puede ser necesario crear una migración desde cero:

1. Elimine el archivo de migración creado:
   ```
   rm -f migrations/versions/001_add_asignatura_fields.py
   ```

2. Genere una nueva migración:
   ```
   flask db migrate -m "add_asignatura_fields"
   ```

3. Revise el archivo de migración generado y luego aplíquelo:
   ```
   flask db upgrade
   ```

## Notas importantes

- La integración agrega dos nuevos campos a la tabla de actividades:
  - `asignatura_id`: ID de la asignatura en el sistema externo
  - `asignatura_info`: Información completa de la asignatura en formato JSON

- Los datos de las asignaturas se obtienen en tiempo real desde la API externa:
  `https://huayca.crub.uncoma.edu.ar/catedras/1.0/rest/materias`

- Si experimenta problemas de conexión con la API, la aplicación seguirá funcionando pero con funcionalidad limitada para la selección de asignaturas.

## Requisitos adicionales

Esta integración requiere las siguientes dependencias adicionales:
- requests
- select2 (ya incluido en los templates)

Puede instalarlas con:
```
pip install requests
```
