var mapaVisualizacion;
        var marcadoresVisualizacion = [];
        
        function abrirMapaModal(reporteIndex) {
            // Obtener el contenedor del reporte
            var reporteElement = document.querySelectorAll('.reporte')[reporteIndex];
            var coordenadasData = reporteElement.querySelector('.reporte-coordenadas-data');
            
            if (!coordenadasData) {
                alert('No hay coordenadas para mostrar');
                return;
            }
            
            var coordenadas = JSON.parse(coordenadasData.dataset.coordenadas);
            var folio = coordenadasData.dataset.folio;
            
            // Actualizar título del modal
            document.getElementById('mapaModalTitle').textContent = 'Ubicación del Incidente - Folio: ' + folio;
            
            // Mostrar modal
            document.getElementById('mapaModal').classList.add('show');
            
            // Inicializar mapa si no existe o reiniciar
            setTimeout(function() {
                if (mapaVisualizacion) {
                    mapaVisualizacion.remove();
                }
                inicializarMapaVisualizacion();
                mostrarCoordenadasEnMapa(coordenadas);
            }, 100);
        }
        
        function cerrarMapaModal() {
            document.getElementById('mapaModal').classList.remove('show');
            // Opcionalmente limpiar el mapa al cerrar
            if (mapaVisualizacion) {
                marcadoresVisualizacion.forEach(function(marker) {
                    mapaVisualizacion.removeLayer(marker);
                });
                marcadoresVisualizacion = [];
            }
        }
        
        function inicializarMapaVisualizacion() {
            // Crear mapa centrado en Xalapa, Veracruz
            mapaVisualizacion = L.map('mapaViewCanvas').setView([19.5333673, -96.9186144], 14);
            
            // Añadir capa de OpenStreetMap
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                maxZoom: 19
            }).addTo(mapaVisualizacion);
        }
        
        function mostrarCoordenadasEnMapa(coordenadas) {
            // Limpiar marcadores anteriores
            marcadoresVisualizacion.forEach(function(marker) {
                mapaVisualizacion.removeLayer(marker);
            });
            marcadoresVisualizacion = [];
            
            if (!coordenadas || coordenadas.length === 0) {
                return;
            }
            
            // Array para calcular los límites
            var bounds = [];
            
            // Agregar marcadores
            coordenadas.forEach(function(coord) {
                var coordText = "Lat: " + coord.lat.toFixed(6) + ", Lng: " + coord.lng.toFixed(6);
                
                // Crear icono personalizado con número
                var customIcon = L.divIcon({
                    html: '<div class="custom-marker">' + coord.id + '</div>',
                    className: '',
                    iconSize: [35, 35],
                    iconAnchor: [17, 17]
                });
                
                // Crear marcador
                var marker = L.marker([coord.lat, coord.lng], {
                    icon: customIcon
                }).addTo(mapaVisualizacion);
                
                // Añadir popup
                marker.bindPopup(
                    '<div style="padding: 5px;"><strong>Marcador #' + coord.id + '</strong><br>' + 
                    coordText + '</div>'
                );
                
                marcadoresVisualizacion.push(marker);
                bounds.push([coord.lat, coord.lng]);
            });
            
            // Ajustar el mapa a los marcadores
            if (bounds.length === 1) {
                mapaVisualizacion.setView(bounds[0], 16);
            } else if (bounds.length > 1) {
                mapaVisualizacion.fitBounds(bounds, {
                    padding: [50, 50]
                });
            }
        }
        
        // Cerrar modal al hacer clic fuera
        window.onclick = function(event) {
            var modal = document.getElementById('mapaModal');
            if (event.target == modal) {
                cerrarMapaModal();
            }
        }