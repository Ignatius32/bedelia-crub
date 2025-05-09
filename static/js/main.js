// main.js - Funcionalidades JavaScript para el sistema de administración universitaria

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Inicializar popovers de Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Manejar los mensajes flash con desaparición automática
    setTimeout(function() {
        $('.alert-dismissible').alert('close');
    }, 5000);
    
    // Confirmar eliminación de registros
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Está seguro que desea eliminar este registro? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
    
    // Validación de formularios de actividades para fechas y horarios
    const actividadForm = document.querySelector('#actividad-form');
    if (actividadForm) {
        actividadForm.addEventListener('submit', function(e) {
            const fechaDesde = new Date(document.querySelector('#fecha_desde').value);
            const fechaHasta = new Date(document.querySelector('#fecha_hasta').value);
            
            if (fechaHasta < fechaDesde) {
                e.preventDefault();
                alert('La fecha de finalización debe ser posterior a la fecha de inicio.');
                return false;
            }
            
            const horaDesde = document.querySelector('#horario_desde').value;
            const horaHasta = document.querySelector('#horario_hasta').value;
            
            if (horaHasta <= horaDesde) {
                e.preventDefault();
                alert('El horario de finalización debe ser posterior al horario de inicio.');
                return false;
            }
        });
    }
    
    // Filtros para tablas de datos
    const filterInput = document.querySelector('.table-filter');
    if (filterInput) {
        filterInput.addEventListener('keyup', function() {
            const value = this.value.toLowerCase();
            const table = document.querySelector('.table-filterable');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(function(row) {
                const text = row.textContent.toLowerCase();
                row.style.display = text.indexOf(value) > -1 ? '' : 'none';
            });
        });
    }
});
