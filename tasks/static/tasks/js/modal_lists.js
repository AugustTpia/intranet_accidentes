document.addEventListener('DOMContentLoaded', function() {
            const modalOverlay = document.getElementById('modalOverlay');
            const closeModal = document.getElementById('closeModal');
            const modalOperador = document.getElementById('modalOperador');
            const modalFolios = document.getElementById('modalFolios');
            const modalPosicion = document.getElementById('modalPosicion');
            
            // Seleccionar todos los iconos con la clase icon-trigger
            const iconTriggers = document.querySelectorAll('.icon-trigger');
            
            // Agregar evento de clic a cada icono
            iconTriggers.forEach(function(icon) {
                icon.addEventListener('click', function() {
                    // Obtener datos del operador desde los atributos data
                    const operador = this.getAttribute('data-operador');
                    const folios = this.getAttribute('data-folios');
                    const posicion = this.getAttribute('data-posicion');
                    
                    // Actualizar el contenido del modal con los datos del operador
                    modalOperador.textContent = operador;
                    modalFolios.textContent = folios;
                    modalPosicion.textContent = posicion;
                    
                    // Mostrar el modal
                    modalOverlay.style.display = 'flex';
                });
            });
            
            // Cerrar modal al hacer clic en el botón de cerrar
            closeModal.addEventListener('click', function() {
                modalOverlay.style.display = 'none';
            });
            
            // Cerrar modal al hacer clic fuera del contenido
            modalOverlay.addEventListener('click', function(e) {
                if (e.target === modalOverlay) {
                    modalOverlay.style.display = 'none';
                }
            });
            
            // Funcionalidad de búsqueda con lupa para operadores
            const searchInput = document.getElementById('search-operador');
            const operadorSelect = document.getElementById('operador');
            const operadorSeleccionado = document.getElementById('operador-seleccionado');
            const posicionOperador = document.getElementById('posicion-operador');
            const foliosOperador = document.getElementById('folios-operador');
            const culpaOperador = document.getElementById('culpa-operador');
            
            // Obtener todos los operadores de la tabla para mostrar información
            const operadoresTabla = [];
            document.querySelectorAll('tbody tr').forEach(function(row) {
                const celdas = row.querySelectorAll('td');
                if (celdas.length >= 3) {
                    operadoresTabla.push({
                        posicion: celdas[0].textContent.trim(),
                        nombre: celdas[1].textContent.trim(),
                        folios: celdas[2].textContent.trim()
                    });
                }
            });
            
            // Función para filtrar operadores según la búsqueda
            function filtrarOperadores(termino) {
                const opciones = operadorSelect.querySelectorAll('option');
                let encontrados = 0;
                
                opciones.forEach(function(opcion) {
                    if (opcion.value === "") return; // Saltar la opción por defecto
                    
                    const texto = opcion.textContent.toLowerCase();
                    const terminoLower = termino.toLowerCase();
                    
                    if (texto.includes(terminoLower)) {
                        opcion.style.display = '';
                        encontrados++;
                    } else {
                        opcion.style.display = 'none';
                    }
                });
                
                // Mostrar mensaje si no hay resultados
                const noResults = operadorSelect.querySelector('.no-results-option');
                if (encontrados === 0 && termino !== '') {
                    if (!noResults) {
                        const option = document.createElement('option');
                        option.value = "";
                        option.textContent = "No se encontraron operadores";
                        option.disabled = true;
                        option.className = "no-results-option";
                        operadorSelect.appendChild(option);
                    }
                } else if (noResults) {
                    noResults.remove();
                }
            }
            
            // Evento para el campo de búsqueda
            searchInput.addEventListener('input', function() {
                filtrarOperadores(this.value);
            });
            
            // Evento para cuando se selecciona un operador
            operadorSelect.addEventListener('change', function() {
                const operador = this.value;
                operadorSeleccionado.textContent = operador || "Ninguno";
                
                // Buscar información del operador en la tabla
                if (operador) {
                    const infoOperador = operadoresTabla.find(function(op) {
                        return op.nombre === operador;
                    });
                    
                    if (infoOperador) {
                        posicionOperador.textContent = infoOperador.posicion;
                        foliosOperador.textContent = infoOperador.folios;
                        // Aquí puedes agregar la lógica para calcular la culpa
                        culpaOperador.textContent = "0 de 0"; // Placeholder
                    } else {
                        posicionOperador.textContent = "-";
                        foliosOperador.textContent = "-";
                        culpaOperador.textContent = "- de -";
                    }
                } else {
                    posicionOperador.textContent = "-";
                    foliosOperador.textContent = "-";
                    culpaOperador.textContent = "- de -";
                }
            });
            
            // Inicializar con el operador seleccionado si existe
            const operadorInicial = "{{ filtros.operador }}";
            if (operadorInicial) {
                operadorSeleccionado.textContent = operadorInicial;
                
                // Buscar información del operador en la tabla
                const infoOperador = operadoresTabla.find(function(op) {
                    return op.nombre === operadorInicial;
                });
                
                if (infoOperador) {
                    posicionOperador.textContent = infoOperador.posicion;
                    foliosOperador.textContent = infoOperador.folios;
                }
            }
        });