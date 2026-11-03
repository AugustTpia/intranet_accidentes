// Variables para paginación
        const reportsPerPage = 10;
        let currentPage = 1;
        let totalPages = 1;
        let allReports = document.querySelectorAll('.reporte');
        let originalReports = Array.from(allReports); // Guardamos una copia de todos los reportes originales
        
        // Variables para el modal
        const modal = document.getElementById("myModal");
        const modalImg = document.getElementById("modalImage");
        const closeBtn = document.querySelector(".close");

        // Asignar páginas dinámicamente
        function assignPages() {
            allReports.forEach((report, index) => {
                const pageNumber = Math.floor(index / reportsPerPage) + 1;
                report.setAttribute('data-page', pageNumber);
            });
            totalPages = Math.ceil(allReports.length / reportsPerPage);
        }

        // Mostrar página específica
        function showPage(page) {
            // Ocultar todos los reportes
            allReports.forEach(report => {
                report.classList.remove('active');
            });
            
            // Mostrar reportes de la página actual
            const startIndex = (page - 1) * reportsPerPage;
            const endIndex = startIndex + reportsPerPage;
            
            for (let i = startIndex; i < endIndex && i < allReports.length; i++) {
                allReports[i].classList.add('active');
            }
            
            // Actualizar botones activos
            const pageBtns = document.querySelectorAll('.page-btn');
            pageBtns.forEach((btn, index) => {
                btn.classList.remove('active');
                if (btn.textContent == page) {
                    btn.classList.add('active');
                }
            });
            
            // Scroll hacia arriba
            window.scrollTo({top: 0, behavior: 'smooth'});
        }

        // Inicializar paginación
        function initPagination() {
            assignPages();
            const paginationContainer = document.getElementById('paginationContainer');
            paginationContainer.innerHTML = '';
            
            if (totalPages > 1) {
                const prevBtn = document.createElement('button');
                prevBtn.className = 'page-btn';
                prevBtn.innerHTML = '<i class="fas fa-chevron-left"></i>';
                prevBtn.addEventListener('click', () => {
                    if (currentPage > 1) {
                        currentPage--;
                        showPage(currentPage);
                    }
                });
                paginationContainer.appendChild(prevBtn);
            }
            
            for (let i = 1; i <= totalPages; i++) {
                const pageBtn = document.createElement('button');
                pageBtn.className = 'page-btn';
                if (i === 1) pageBtn.classList.add('active');
                pageBtn.textContent = i;
                pageBtn.addEventListener('click', () => {
                    currentPage = i;
                    showPage(currentPage);
                });
                paginationContainer.appendChild(pageBtn);
            }
            
            if (totalPages > 1) {
                const nextBtn = document.createElement('button');
                nextBtn.className = 'page-btn';
                nextBtn.innerHTML = '<i class="fas fa-chevron-right"></i>';
                nextBtn.addEventListener('click', () => {
                    if (currentPage < totalPages) {
                        currentPage++;
                        showPage(currentPage);
                    }
                });
                paginationContainer.appendChild(nextBtn);
            }
            
            showPage(1);
        }

        // Función para abrir el modal
        function openModal(imageUrl) {
            modal.style.display = "flex";
            setTimeout(() => {
                modal.classList.add("show");
                modalImg.src = imageUrl;
            }, 10);
            
            // Resetear el evento onclick cada vez
            modal.onclick = function(e) {
                if (e.target === modal) {
                    closeModal();
                }
            }
        }

        // Función para cerrar el modal
        function closeModal() {
            modal.classList.remove("show");
            setTimeout(() => {
                modal.style.display = "none";
                modalImg.src = ""; // Limpiar la imagen
            }, 300);
        }

        // Configurar lazy loading de imágenes
        function setupLazyLoading() {
            const lazyImageObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const thumbnail = entry.target;
                        const img = thumbnail.querySelector('img');
                        const spinner = thumbnail.querySelector('.imagen-loading');
                        
                        if (img) {
                            img.onload = function() {
                                spinner.style.display = 'none';
                                img.style.display = 'block';
                            };
                            img.style.display = 'block';
                        }
                    }
                });
            });
            
            document.querySelectorAll('.imagen-thumbnail').forEach(thumbnail => {
                lazyImageObserver.observe(thumbnail);
            });
        }

        // Inicializar todo al cargar la página
        document.addEventListener("DOMContentLoaded", function() {
            initPagination();
            setupLazyLoading();
            
            // Manejar tecla Escape
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Escape' && modal.classList.contains("show")) {
                    closeModal();
                }
            });
            
            // Manejar búsqueda con debouncing
            let searchTimeout;
            document.getElementById("searchInput").addEventListener("input", function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    const searchTerm = this.value.toLowerCase();
                    
                    // Restaurar todos los reportes originales primero
                    allReports = Array.from(originalReports);
                    
                    if (searchTerm.trim() === "") {
                        // Si la búsqueda está vacía, mostrar todos los reportes
                        allReports.forEach(report => {
                            report.style.display = "block";
                        });
                    } else {
                        // Filtrar reportes
                        allReports.forEach(report => {
                            const shouldDisplay = report.textContent.toLowerCase().includes(searchTerm);
                            report.style.display = shouldDisplay ? "block" : "none";
                        });
                        
                        // Actualizar la lista de reportes visibles
                        allReports = Array.from(document.querySelectorAll('.reporte:not([style*="display: none"])'));
                    }
                    
                    // Actualizar la paginación
                    currentPage = 1;
                    initPagination();
                }, 300);
            });
        });