// Ruta al archivo con la galería de imágenes
var galeriaURL = '/MostrarImages/';

$.ajax({
    type: 'POST',
    url: '/MostrarImages/',
    dataType: 'html',
    data: { 'access_token': access_token },
    success: function (data) {
        // Insertar el contenido de la galería en la ubicación deseada
        $('.ubicacion-imagenes').html(data);
    },
    error: function () {
        console.error('Error al cargar la galería de imágenes.');
    }
});
