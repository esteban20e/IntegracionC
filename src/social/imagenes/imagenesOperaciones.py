import os
from flask import Flask,jsonify, request, render_template, Blueprint,current_app, url_for
from utils.db import db
from models.modelMedia.image import Image
from models.usuario import Usuario
import jwt
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError

# Configuración del Blueprint para el registro de usuarios
imagenesOperaciones = Blueprint("imagenesOperaciones", __name__)

@imagenesOperaciones.route('/subirImagen/')
def subirImagen():
    return render_template("media/principalMedia/subirImage.html")

@imagenesOperaciones.route('/subirVideo/')
def subirVideo():
    return render_template("media/principalMedia/subirVideo.html")

@imagenesOperaciones.route('/mostrarGaleria/')
def mostrarGaleria():
    return render_template("media/principalMedia/mostrarGaleria.html")

@imagenesOperaciones.route('/cargarVideo', methods=['POST'])
def cargarVideo():
    #try:
        # Verificar si el campo 'selectedColor' está en la solicitud
        if 'selectedColor' not in request.form:
            return jsonify({'error': 'No se proporcionó el campo de selectedColor'}), 400

        selectedColor = request.form['selectedColor']

        # Verificar si el campo 'video' está en la solicitud
        if 'video' not in request.files:
            return jsonify({'error': 'No se proporcionó el campo de video'}), 400

        video = request.files['video']

        # Verificar si los campos necesarios están presentes en la solicitud
        required_fields = ['nombreArchivo', 'descriptionVideo', 'randomNumber']
        for field in required_fields:
            if field not in request.form:
                return jsonify({'error': f'No se proporcionó el campo de {field}'}), 400

        nombre_archivo = request.form['nombreArchivo']
        description_video = request.form['descriptionVideo']
        random_number = int(request.form['randomNumber'])
  # Verificar si el token de acceso está presente en el encabezado 'Authorization'
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token de acceso no proporcionado'}), 401

        authorization_header = request.headers['Authorization']
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Formato de token de acceso no válido'}), 401

        access_token = parts[1]
        

        # Guardar el video en la carpeta src/static/uploads
        new_path = os.path.join('static', 'uploads', video.filename)
        video.save(new_path)

        if access_token:
            app = current_app._get_current_object()                    
            userid = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
          

        # Crear una nueva instancia de la clase Image y agregarla a la base de datos
        nueva_imagen = Image(
            user_id=userid,
            title=nombre_archivo,
            description=description_video,
            colorDescription=selectedColor,
            filepath=new_path,
            randomNumber=random_number
        )

        db.session.add(nueva_imagen)
        db.session.commit()

        # Realizar alguna acción adicional si es necesario, como mostrar las imágenes
     

        return jsonify({'mensaje': 'Video cargado con éxito', 'nombreArchivo': nombre_archivo})

    #except Exception as e:
       # return jsonify({'error': str(e)}), 500
    
    
@imagenesOperaciones.route('/cargarImagen', methods=['POST'])
def cargarImagen():
  try:
      
        if 'selectedColor' not in request.form:
            return jsonify({'error': 'No se proporcionó el campo de selectedColor'}), 400

        selectedColor = request.form['selectedColor']
        # Verificar si el campo 'imagen' está en la solicitud
        if 'imagen' not in request.files:
            return jsonify({'error': 'No se proporcionó el campo de imagen'}), 400

        imagen = request.files['imagen']

        # Verificar si el campo 'nombreArchivo' está en la solicitud
        if 'nombreArchivo' not in request.form:
            return jsonify({'error': 'No se proporcionó el campo de nombreArchivo'}), 400

        nombre_archivo = request.form['nombreArchivo']
        
        if 'descriptionImagen' not in request.form:
            return jsonify({'error': 'No se proporcionó el campo de descriptionImagen'}), 400

        descriptionImagen = request.form['descriptionImagen']
        
        randomNumber_ = request.form['randomNumber']
        numeroAleatoreo = int(randomNumber_)
        # Verificar si el token de acceso está presente en el encabezado 'Authorization'
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Token de acceso no proporcionado'}), 401

        authorization_header = request.headers['Authorization']
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Formato de token de acceso no válido'}), 401

        access_token = parts[1]
       
        # Guardar la imagen en la carpeta src/static/uploads
      
        new_path = os.path.join( 'static', 'uploads', imagen.filename)
       # Guardar la imagen en la carpeta src/static/uploads
       # print(f"Ruta completa del archivo: {new_path}")
        imagen.save(new_path)
        # Resto de tu lógica para manejar la imagen, el nombre del archivo y el access_token
        # Aquí puedes acceder a 'imagen' (objeto FileStorage), 'nombre_archivo' y 'access_token'
        #aqui carga la los datos en la base de datos
        if access_token:
            app = current_app._get_current_object()                    
            userid = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            nueva_imagen = Image(
                user_id=userid,
                title=nombre_archivo,
                description=descriptionImagen,
                colorDescription=selectedColor,
                filepath=new_path,
                randomNumber=numeroAleatoreo
            )
            db.session.add(nueva_imagen)
            db.session.commit()
          
       # MostrarImages()
        return jsonify({'mensaje': 'Imagen cargada con éxito', 'nombreArchivo': nombre_archivo})
  except Exception as e:
        return jsonify({'error': str(e)}), 500

@imagenesOperaciones.route('/MostrarImages/', methods=['POST'])
def mostrar_imagenes():
    access_token = request.form.get('access_token')
     
   # Obtener la ruta completa de la carpeta 'static/uploads'
    uploads_folder = os.path.join(current_app.root_path, 'static', 'uploads')

    # Obtener todas las imágenes en la carpeta 'static/uploads'
    image_files = [file for file in os.listdir(uploads_folder) if file.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Crear las rutas completas de las imágenes sin codificación de caracteres
    image_paths = [os.path.join('uploads', filename).replace(os.sep, '/') for filename in image_files]
   
    
    if access_token:
        app = current_app._get_current_object()                    
        userid = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            
       
        # Obtener todas las imágenes cuyas rutas coincidan con las rutas en db_image_paths
        
        usuarios = Usuario.query.all()
        imagenes = Image.query.all()
        
        
       # Filtrar solo las imágenes (puedes ajustar esto según tus necesidades)
        imagenes_filtradas = [img for img in imagenes if es_formato_imagen(img.filepath)]
        
        # Procesar y asignar los paths solo a las imágenes filtradas
        for img in imagenes_filtradas:
            img.image_paths = img.filepath.replace('static\\', '').replace('\\', '/')
  # Buscar el usuario correspondiente
            usuario_correspondiente = next((usuario for usuario in usuarios if usuario.id == img.user_id), None)

            # Agregar el correo electrónico del usuario a la imagen
            if usuario_correspondiente:
                img.correo_electronico = usuario_correspondiente.correo_electronico
            else:
                # Puedes manejar el caso en el que no se encuentra el usuario (si es relevante para tu lógica)
                img.correo_electronico = "Usuario no encontrado"

          
      
    return render_template('media/principalMedia/images.html', imagenes=imagenes_filtradas)
    
  

@imagenesOperaciones.route('/imagenesImagenesOperaciones-mostrar-Galeria', methods = ['POST'])
def imagenesImagenesOperaciones_mostrar_Galeria():
    access_token = request.form.get('access_token')
    # Hacer algo con access_token
   
    # Obtener las imágenes desde la base de datos
    #images = Image.query.all()
     # Obtener las rutas completas de las imágenes
    #image_paths = [os.path.join('static', 'uploads', image.filename) for image in images]
    
   # Obtener la ruta completa de la carpeta 'static/uploads'
    uploads_folder = os.path.join(current_app.root_path, 'static', 'uploads')

    # Obtener todas las imágenes en la carpeta 'static/uploads'
    image_files = [file for file in os.listdir(uploads_folder) if file.endswith(('.png', '.jpg', '.jpeg', '.gif'))]

    # Crear las rutas completas de las imágenes sin codificación de caracteres
    image_paths = [os.path.join('uploads', filename).replace(os.sep, '/') for filename in image_files]
   
    # Transformar las rutas al formato almacenado en la base de datos
   # db_image_paths = [os.path.relpath(os.path.join(current_app.root_path, path), current_app.root_path).replace('/', os.sep) for path in image_paths]

   
    if access_token:
        app = current_app._get_current_object()                    
        userid = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
            
       
        # Obtener todas las imágenes cuyas rutas coincidan con las rutas en db_image_paths
        imagenes = Image.query.filter(Image.user_id == userid).all()
        
       # Filtrar solo las imágenes (puedes ajustar esto según tus necesidades)
        imagenes_filtradas = [img for img in imagenes if es_formato_imagen(img.filepath)]

        # Procesar y asignar los paths solo a las imágenes filtradas
        for img in imagenes_filtradas:
            img.image_paths = img.filepath.replace('static\\', '').replace('\\', '/')

        #          img.image_paths = [img.filepath.replace('static\\', '').replace('\\', '/') for img in imagenes if es_formato_imagen(img.filepath)]
        
          
      
    return render_template('media/principalMedia/mostrarGaleria.html', imagenes=imagenes_filtradas)

@imagenesOperaciones.route('/eliminarImagen', methods=['POST'])
def eliminar_imagen():
    data = request.form  # Puedes ajustar esto según la forma en que envíes los datos desde tu cliente
    randomNumber = data.get('randomNumber')
    imageName = data.get('imageName')
    authorization_header = request.headers.get('Authorization')

    if authorization_header and authorization_header.startswith('Bearer '):
        # Extraer el token de acceso de la cadena del encabezado
        access_token = authorization_header[len('Bearer '):]
        app = current_app._get_current_object()
        userid = jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']

        try:
            
            # Reemplazar barras diagonales hacia adelante ("/") por barras diagonales hacia atrás ("\")
            ruta_base_datos = imageName.replace('/', '\\')

            # Agregar "static" al inicio de la ruta
            ruta_base_datos = os.path.normpath('static\\' + ruta_base_datos)
            # Obtener la imagen correspondiente al nombre de la imagen y al ID del usuario
            imagen = Image.query.filter_by(user_id=userid, filepath=ruta_base_datos).first()

            if imagen:
                # Eliminar la imagen de la base de datos
                db.session.delete(imagen)
                db.session.commit()
                ruta_imagen = os.path.join(ruta_base_datos)
                os.remove(ruta_imagen)
                return jsonify({'message': 'Imagen eliminada con éxito'}), 200
            else:
                return jsonify({'error': 'Imagen no encontrada'}), 404
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': 'Error al eliminar la imagen'}), 500
    else:
        return jsonify({'error': 'Token de autorización no válido'}), 401
    
def es_formato_imagen(filepath):
    # Extensiones de archivo de imagen comunes
    extensiones_imagen = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Verificar si la extensión del archivo está en la lista de extensiones de imagen
    return any(filepath.lower().endswith(ext) for ext in extensiones_imagen)