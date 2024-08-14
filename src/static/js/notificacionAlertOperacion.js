
// Solicitar permiso para mostrar notificaciones
function solicitarPermiso() {
    if (Notification.permission !== "granted") {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                console.log("Permiso concedido para mostrar notificaciones.");
            }
        });
    }
}

// Mostrar una notificación
function mostrarNotificacion() {
    if (Notification.permission === "granted") {
        const notificacion = new Notification("¡Operacion nueva!", {
            body: "¡Debe operar nuevamente!",
            icon: "/static/img/icono.png" // Ruta de la imagen del icono
        });

        // Puedes añadir un evento click para que algo suceda cuando se hace clic en la notificación
        notificacion.onclick = function(event) {
            window.focus(); // Lleva al usuario a la ventana que generó la notificación
            event.target.close(); // Cierra la notificación
            // Aquí puedes agregar el código que quieres que se ejecute al hacer clic en la notificación
        };
    }
}
