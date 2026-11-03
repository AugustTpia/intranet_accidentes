        var map;
        var markers = [];
        var markerCounter = 1;
        var mapInitialized = false;

        function openMapModal() {
            document.getElementById('mapModal').classList.add('show');
            if (!mapInitialized) {
                setTimeout(function() {
                    initializeMap();
                    loadExistingCoordinates();
                }, 100);
                mapInitialized = true;
            } else {
                google.maps.event.trigger(map, 'resize');
                map.setCenter(new google.maps.LatLng(19.5333673, -96.9186144));
            }
        }
        
        function closeMapModal() {
            document.getElementById('mapModal').classList.remove('show');
        }
        
        function initializeMap() {
            var mapOptions = {
                center: new google.maps.LatLng(19.5333673, -96.9186144),
                zoom: 14,
                mapTypeId: "OSM",
                mapTypeControl: true,
                streetViewControl: true
            };
            
            map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
            
            map.mapTypes.set("OSM", new google.maps.ImageMapType({
                getTileUrl: function(coord, zoom) {
                    return "https://tile.openstreetmap.org/" + zoom + "/" + coord.x + "/" + coord.y + ".png";
                },
                tileSize: new google.maps.Size(256, 256),
                name: "OpenStreetMap",
                maxZoom: 18
            }));
            
            var myCoordinates = [
            ];
            
            var polyOptions = {
                path: myCoordinates,
                strokeColor: "#3e4d9a",
                strokeOpacity: 0.7,
                strokeWeight: 3,
                fillColor: "#3e4d9a",
                fillOpacity: 0.4
            };
            var it = new google.maps.Polygon(polyOptions);
            it.setMap(map);
            
            var myCoordinates2 = [
            ];
            
            var polyOptions2 = {
                path: myCoordinates2,
                strokeColor: "#fae708",
                strokeOpacity: 0.7,
                strokeWeight: 3,
                fillColor: "#fae708",
                fillOpacity: 0.3
            };
            var it2 = new google.maps.Polygon(polyOptions2);
            it2.setMap(map);
            
            google.maps.event.addListener(map, 'click', function(event) {
                addMarker(event.latLng);
            });
        }
        
        function loadExistingCoordinates() {
            var coordinatesInput = document.getElementById('coordinates');
            if (coordinatesInput.value && coordinatesInput.value.trim() !== '') {
                try {
                    var savedCoords = JSON.parse(coordinatesInput.value);
                    if (Array.isArray(savedCoords) && savedCoords.length > 0) {
                        savedCoords.forEach(function(coord) {
                            var location = new google.maps.LatLng(coord.lat, coord.lng);
                            addMarker(location, coord.id);
                        });
                        
                        if (markers.length > 0) {
                            map.setCenter(markers[0].getPosition());
                            map.setZoom(15);
                        }
                    }
                } catch (e) {
                    console.error('Error al cargar coordenadas:', e);
                }
            }
        }
        
        function addMarker(location, existingId) {
            var lat = location.lat();
            var lng = location.lng();
            var coordText = "Lat: " + lat.toFixed(6) + ", Lng: " + lng.toFixed(6);
            
            var markerId = existingId || markerCounter;
            if (!existingId) {
                markerCounter++;
            } else {
                if (markerId >= markerCounter) {
                    markerCounter = markerId + 1;
                }
            }
            
            var marker = new google.maps.Marker({
                position: location,
                map: map,
                title: coordText,
                label: String(markerId),
                animation: google.maps.Animation.DROP,
                draggable: true
            });
            
            var infowindow = new google.maps.InfoWindow({
                content: '<div style="padding: 5px;"><strong>Marcador #' + markerId + '</strong><br>' + coordText + '</div>'
            });
            
            marker.addListener('click', function() {
                infowindow.open(map, marker);
            });
            
            marker.addListener('dragend', function(event) {
                var newLat = event.latLng.lat();
                var newLng = event.latLng.lng();
                var newCoordText = "Lat: " + newLat.toFixed(6) + ", Lng: " + newLng.toFixed(6);
                marker.setTitle(newCoordText);
                infowindow.setContent('<div style="padding: 5px;"><strong>Marcador #' + marker.markerId + '</strong><br>' + newCoordText + '</div>');
                updateMarkerList();
            });
            
            marker.markerId = markerId;
            markers.push(marker);
            
            updateMarkerList();
            if (!existingId) {
                infowindow.open(map, marker);
            }
        }
        
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
            
            document.getElementById('markerCount').textContent = markers.length;
        }
        
        function deleteMarker(index) {
            markers[index].setMap(null);
            markers.splice(index, 1);
            updateMarkerList();
        }
        
        function clearAllMarkers() {
            if (confirm('¿Estás seguro de eliminar todos los marcadores?')) {
                markers.forEach(function(marker) {
                    marker.setMap(null);
                });
                markers = [];
                markerCounter = 1;
                updateMarkerList();
                document.getElementById('coordinates').value = '';
            }
        }
        
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
            alert('Coordenadas guardadas en consola:\n' + JSON.stringify(coordinates, null, 2));
            return coordinates;
        }
        
        function saveCoordinates() {
            var coordinates = [];
            markers.forEach(function(marker) {
                coordinates.push({
                    id: marker.markerId,
                    lat: marker.getPosition().lat(),
                    lng: marker.getPosition().lng()
                });
            });
            
            document.getElementById('coordinates').value = JSON.stringify(coordinates);
            
            alert('¡' + coordinates.length + ' marcador(es) guardado(s) correctamente!');
            closeMapModal();
        }
        
        window.onclick = function(event) {
            var modal = document.getElementById('mapModal');
            if (event.target == modal) {
                closeMapModal();
            }
        }