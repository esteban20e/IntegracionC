// Cerrar el menú desplegable al ser seleccionado
function cerrarMenuSeleccionado() {
  $(document).ready(function() {
      $(".navbar-nav a").click(function() {
          var isSubmenu = $(this).next(".dropdown-menu").length > 0;

          // Solo cierra el menú si el enlace no tiene un submenú
          if (!isSubmenu) {
              $(".navbar-collapse").collapse('hide');
          }
      });
  });
}


document.addEventListener("DOMContentLoaded", function() {
    // Obtener todos los enlaces que tienen el atributo data-target
    const links = document.querySelectorAll('[data-target]');
    
    

    // Agregar un evento de clic a cada enlace
    links.forEach((link) => {
      link.addEventListener('click', (event) => {
        event.preventDefault(); // Evitar el comportamiento predeterminado del enlace
  
        const target = link.dataset.target; // Obtener el valor del atributo data-target
  
        // Crear un elemento <div> para cargar el contenido del modal
        const modalContainer = document.createElement('div');
        modalContainer.classList.add('modal-container');
  
        // Cargar el contenido del modal desde el archivo modal.html
        fetch('static/modUpImage.html')
          .then((response) => response.text())
          .then((html) => {
            modalContainer.innerHTML = html;
            const modal = modalContainer.querySelector('.modal');
            if (modal) {
              modal.style.display = 'block';
            } else {
              console.error('El elemento modal no fue encontrado.');
            }
            
          })
          .catch((error) => {
            console.error('Error al cargar el contenido del modal:', error);
          });
      });
    });
  });
  