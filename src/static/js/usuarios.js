
  
  
  
  // Función para editar un usuario existente
  function editarUsuario(event) {
    event.preventDefault();
    var form = event.target;
    var id = form.id.value;   
    var email = form.email.value;
    var password = form.password.value;
    var rol = form.rol.value;
    fetch('/usuarios/' + id, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nombre: nombre,
        email: email,
        password: password,
        rol: rol
      })
    })
    .then(function(response) {
      if (response.ok) {
        return response.json();
      }
      throw new Error('Error al editar usuario');
    })
    .then(function(usuario) {
      var usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
      for (var i = 0; i < usuarios.length; i++) {
        if (usuarios[i].id === usuario.id) {
          usuarios[i] = usuario;
          break;
        }
      }
      localStorage.setItem('usuarios', JSON.stringify(usuarios));
      mostrarUsuarios(usuarios);
      $('#editarUsuarioModal').modal('hide');
      alert('Usuario editado correctamente');
    })
    .catch(function(error) {
      console.error(error);
      alert('Error al editar usuario');
    });
  }
  
  // Función para eliminar un usuario existente
  function eliminarUsuario(event) {
    event.preventDefault();
    var form = event.target;
    var id = form.id.value;
    fetch('/usuarios/' + id, {
      method: 'DELETE'
    })
    .then(function(response) {
      if (response.ok) {
        return response.json();
      }
      throw new Error('Error al eliminar usuario');
    })
    .then(function(usuario) {
      var usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
      for (var i = 0; i < usuarios.length; i++) {
        if (usuarios[i].id === usuario.id) {
          usuarios.splice(i, 1);
          break;
        }
      }
      localStorage.setItem('usuarios', JSON.stringify(usuarios));
      mostrarUsuarios(usuarios);
      $('#eliminarUsuarioModal').modal('hide');
      alert('Usuario eliminado correctamente');
    })
    .catch(function(error) {
      console.error(error);
      alert('Error al eliminar usuario');
    });
  }
  
  // Función para inicializar la página
  function inicializarPagina() {
    // Mostrar la lista de usuarios
    var usuarios = JSON.parse(localStorage.getItem('usuarios')) || [];
    mostrarUsuarios(usuarios);
  
    // Agregar un nuevo usuario
    var agregarUsuarioForm = document.querySelector('#agregarUsuarioForm');
    agregarUsuarioForm.addEventListener('submit', agregarUsuario);
  
    // Editar un usuario existente
    var editarUsuarioForm = document.querySelector('#editarUsuarioForm');
    editarUsuarioForm.addEventListener('submit', editarUsuario);
  
    // Eliminar un usuario existente
    var eliminarUsuarioForm = document.querySelector('#eliminarUsuarioForm');
    eliminarUsuarioForm.addEventListener('submit', eliminarUsuario);
  }
  
  // Inicializar la página cuando se carga
  document.addEventListener('DOMContentLoaded', inicializarPagina);