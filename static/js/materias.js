/**
 * JavaScript para manejar la selección de asignaturas desde la API externa
 */
document.addEventListener('DOMContentLoaded', function() {
    // Elemento select para asignaturas
    const asignaturaSelect = document.getElementById('asignatura_id');
    // Campo oculto para almacenar la información completa de la asignatura
    const asignaturaInfoField = document.getElementById('asignatura_info');
    
    if (asignaturaSelect) {
        // Inicializar Select2 para búsqueda y selección de asignaturas
        $(asignaturaSelect).select2({
            placeholder: 'Buscar asignatura...',
            minimumInputLength: 3,
            ajax: {
                url: '/admin/api/materias/search',
                dataType: 'json',
                delay: 400,
                data: function(params) {
                    return {
                        q: params.term
                    };
                },
                processResults: function(data) {
                    return {
                        results: data
                    };
                },
                cache: true
            },
            templateResult: formatMateria,
            templateSelection: formatMateriaSelection
        });

        // Cuando se selecciona una asignatura, guardar su información completa en el campo oculto
        $(asignaturaSelect).on('select2:select', function(e) {
            const data = e.params.data;
            if (data && data.data) {
                asignaturaInfoField.value = JSON.stringify(data.data);
            }
        });
    }
});

/**
 * Formatea una materia para mostrarla en el dropdown de resultados
 */
function formatMateria(materia) {
    if (materia.loading) return materia.text;
    if (!materia.data) return materia.text;
    
    const data = materia.data;
    let markup = `<div class="select2-result-materia">
        <strong>${data.nombre_materia}</strong>
        <div><small>Carrera: ${data.nombre_carrera}</small></div>
        <div><small>Plan: ${data.plan_guarani} | Año plan: ${data.ano_plan}</small></div>
    </div>`;
    
    return markup;
}

/**
 * Formatea una materia una vez seleccionada
 */
function formatMateriaSelection(materia) {
    return materia.text || materia.nombre_materia;
}
