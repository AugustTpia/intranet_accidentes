// Script para formatear el monto
document.getElementById('costo_finiquito').addEventListener('input', function(e){
            let input = e.target.value.replace(/[^0-9.]/g, '');
            let parts = input.split('.');
            let integerPart = parts[0];
            let decimalPart = parts.length > 1 ? '.' + parts[1] : '';
            integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
            e.target.value = integerPart + decimalPart;
        });

        document.querySelector('form').addEventListener('submit', function(e){
            let montoInput = document.getElementById('costo_finiquito');
            let cleanValue = montoInput.value.replace(/,/g, '');
            montoInput.value = cleanValue;
        });

        // Script para preview de imágenes
        function previewImage(input, number) {
            const preview = document.getElementById(`preview-${number}`);
            const file = input.files[0];
            const reader = new FileReader();
            
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
                document.querySelector(`#image-box-${number} i`).style.display = 'none';
                document.querySelector(`#image-box-${number} span`).style.display = 'none';
            }
            
            if (file) {
                reader.readAsDataURL(file);
            }
        }
        
        function removeImage(number) {
            const input = document.getElementById(`imagen${number}`);
            const preview = document.getElementById(`preview-${number}`);
            const box = document.getElementById(`image-box-${number}`);
            
            input.value = '';
            preview.src = '';
            preview.style.display = 'none';
            box.querySelector('i').style.display = 'block';
            box.querySelector('span').style.display = 'block';
        }
        
        // Mostrar botón de eliminar al pasar el mouse
        document.querySelectorAll('.image-upload-box').forEach(box => {
            box.addEventListener('mouseenter', function() {
                const preview = this.querySelector('.preview-image');
                if (preview.style.display === 'block') {
                    this.querySelector('.remove-image-btn').style.opacity = '1';
                }
            });
            
            box.addEventListener('mouseleave', function() {
                this.querySelector('.remove-image-btn').style.opacity = '0';
            });
        });