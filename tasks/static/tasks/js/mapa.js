var map;
        var markers = []; // Array para guardar todos los marcadores
        var markerCounter = 1; // Contador para numerar marcadores
        
        function initialize() {
        
        var mapOptions = {
            center: new google.maps.LatLng(19.5333673,-96.9186144),
            zoom: 14,
            mapTypeId: "OSM",
            mapTypeControl: true,
            streetViewControl: true
        }
        
        map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
        
        map.mapTypes.set("OSM", new google.maps.ImageMapType({
            getTileUrl: function(coord, zoom) {
                return "https://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
            },
            tileSize: new google.maps.Size(256, 256),
            name: "OpenStreetMap",
            maxZoom: 18
        }));
                    
        /* Area Azul coordenadas en formato JS*/
        var myCoordinates = [
            new google.maps.LatLng(19.5353861,-96.9207000),
            new google.maps.LatLng(19.5360194,-96.9206757),
            new google.maps.LatLng(19.5354551,-96.9206329)
        ];
        
        var polyOptions = {
            path: myCoordinates,
            strokeColor: "#3e4d9a",
            strokeOpacity: 0.7,
            strokeWeight: 3,
            fillColor: "#3e4d9a",
            fillOpacity: 0.4
        }
        var it = new google.maps.Polygon(polyOptions);
        it.setMap(map); 
        
        /* Area Amarilla */
        var myCoordinates2 = [
            new google.maps.LatLng(19.523474,-96.9196584),
            new google.maps.LatLng(19.5196142,-96.9249654),
            new google.maps.LatLng(19.523474,-96.9396584)
        ];

        var polyOptions2 = {
            path: myCoordinates2,
            strokeColor: "#fae708",
            strokeOpacity: 0.7,
            strokeWeight: 3,
            fillColor: "#fae708",
            fillOpacity: 0.3
        }
        var it2 = new google.maps.Polygon(polyOptions2);
        it2.setMap(map);
        
        // Agregar marcadores originales
        //var image1 = '{% static "tasks/img/icon.png" %}';
        //addPredefinedMarker(19.5360852, -96.9200778, 'First Point', image1);
        //addPredefinedMarker(19.3543346, -96.9612145, 'Second Point', image1);
        
        // Evento de clic en el mapa para agregar marcadores
        google.maps.event.addListener(map, 'click', function(event) {
            addMarker(event.latLng);
        });
        
        }
        
        // Función para agregar marcadores predefinidos
        function addPredefinedMarker(lat, lng, title, icon) {
            var position = new google.maps.LatLng(lat, lng);
            var marker = new google.maps.Marker({
                position: position,
                map: map,
                title: title,
                icon: icon,
                isPredefined: true
            });
        }
        
        // Función para agregar nuevos marcadores al hacer clic
        function addMarker(location) {
            var lat = location.lat();
            var lng = location.lng();
            var coordText = "Lat: " + lat.toFixed(6) + ", Lng: " + lng.toFixed(6);
            
            var marker = new google.maps.Marker({
                position: location,
                map: map,
                title: coordText,
                label: String(markerCounter),
                animation: google.maps.Animation.DROP,
                draggable: true // Permitir arrastrar el marcador
            });
            
            // InfoWindow para mostrar las coordenadas
            var infowindow = new google.maps.InfoWindow({
                content: '<div style="padding: 5px;"><strong>Marcador #' + markerCounter + '</strong><br>' + coordText + '</div>'
            });
            
            // Mostrar info al hacer clic en el marcador
            marker.addListener('click', function() {
                infowindow.open(map, marker);
            });
            
            // Actualizar coordenadas al arrastrar
            marker.addListener('dragend', function(event) {
                var newLat = event.latLng.lat();
                var newLng = event.latLng.lng();
                var newCoordText = "Lat: " + newLat.toFixed(6) + ", Lng: " + newLng.toFixed(6);
                marker.setTitle(newCoordText);
                infowindow.setContent('<div style="padding: 5px;"><strong>Marcador #' + marker.markerId + '</strong><br>' + newCoordText + '</div>');
                updateMarkerList();
            });
            
            // Guardar el marcador con su ID
            marker.markerId = markerCounter;
            markers.push(marker);
            markerCounter++;
            
            // Actualizar la lista de marcadores
            updateMarkerList();
            
            // Mostrar el info automáticamente
            infowindow.open(map, marker);
        }
        
        // Función para actualizar la lista de marcadores en el panel
        function updateMarkerList() {
            var listContainer = document.getElementById('markerList');
            listContainer.innerHTML = '';
            
            markers.forEach(function(marker, index) {
                var lat = marker.getPosition().lat().toFixed(6);
                var lng = marker.getPosition().lng().toFixed(6);
                
                var item = document.createElement('div');
                item.className = 'marker-item';
                item.innerHTML = '<div><strong>#' + marker.markerId + '</strong><br>' +
                                'Lat: ' + lat + '<br>Lng: ' + lng + '</div>' +
                                '<button class="delete-btn" onclick="deleteMarker(' + index + ')">Eliminar</button>';
                
                // Al hacer clic en el item, centrar el mapa en ese marcador
                item.style.cursor = 'pointer';
                item.addEventListener('click', function(e) {
                    if (!e.target.classList.contains('delete-btn')) {
                        map.setCenter(marker.getPosition());
                        map.setZoom(16);
                        google.maps.event.trigger(marker, 'click');
                    }
                });
                
                listContainer.appendChild(item);
            });
            
            // Actualizar contador
            document.getElementById('markerCount').textContent = markers.length;
        }
        
        // Función para eliminar un marcador específico
        function deleteMarker(index) {
            markers[index].setMap(null);
            markers.splice(index, 1);
            updateMarkerList();
        }
        
        // Función para limpiar todos los marcadores
        function clearAllMarkers() {
            if (confirm('¿Estás seguro de eliminar todos los marcadores?')) {
                markers.forEach(function(marker) {
                    marker.setMap(null);
                });
                markers = [];
                markerCounter = 1;
                updateMarkerList();
            }
        }
        
        // Función para obtener todas las coordenadas (útil para guardar en BD)
        function getAllCoordinates() {
            var coordinates = [];
            markers.forEach(function(marker) {
                coordinates.push({
                    id: marker.markerId,
                    lat: marker.getPosition().lat(),
                    lng: marker.getPosition().lng()
                });
            });
            console.log('Coordenadas actuales:', coordinates);
            alert('Coordenadas en consola (F12 para ver):\n' + JSON.stringify(coordinates, null, 2));
            return coordinates;
        }

        google.maps.event.addDomListener(window, 'load', initialize);