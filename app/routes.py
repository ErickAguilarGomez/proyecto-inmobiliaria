from flask import request, jsonify
from app import app, db
from app.models import Usuario, Cita
from datetime import datetime

# Ruta para Crear Usuario
@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Datos no proporcionados o mal formateados"}), 400

        nombre = data.get('nombre')
        correo = data.get('correo')
        password = data.get('password')
        rol = data.get('rol')

        if not nombre or not correo or not password or not rol:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        rol = rol.strip().lower()
        if rol not in ['agente', 'cliente', 'administrador']:
            return jsonify({"error": "Rol inválido. Los roles permitidos son: agente, cliente, administrador."}), 400

        nuevo_usuario = Usuario(nombre=nombre, correo=correo, password=password, rol=rol.capitalize())
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para Ver Usuarios
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    try:
        usuarios = Usuario.query.all()
        usuarios_list = [{"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol, "correo": usuario.correo, "password": usuario.password} for usuario in usuarios]
        return jsonify(usuarios_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para Crear Cita
@app.route('/crear_cita', methods=['POST'])
def crear_cita():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Datos no proporcionados o mal formateados"}), 400

        proyecto = data['proyecto']
        consulta = data['consulta']
        usuario_id = data['usuario_id']

        if not proyecto or not consulta or not usuario_id:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        usuario = Usuario.query.get(usuario_id)

        if not usuario:
            return jsonify({"error": "Usuario no encontrado"}), 404

        if usuario.rol.lower() != 'cliente':
            return jsonify({"error": "Solo los usuarios con rol 'cliente' pueden crear citas"}), 403

        fecha_actual = datetime.now()

        nueva_cita = Cita(fecha=fecha_actual, proyecto=proyecto, consulta=consulta, usuario_id=usuario_id, agente_id=None, fecha_cierre=None)
        db.session.add(nueva_cita)
        db.session.commit()

        return jsonify({"mensaje": "Cita creada exitosamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para Asignar una Cita a un Agente
@app.route('/asignar_cita/<int:cita_id>', methods=['POST'])
def asignar_cita(cita_id):
    try:
        data = request.get_json()

        if 'correo' not in data or 'password' not in data or 'agente_id' not in data:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        correo = data['correo']
        password = data['password']
        agente_id = data['agente_id']

        usuario = Usuario.query.filter_by(correo=correo, password=password).first()

        if not usuario:
            return jsonify({"error": "Usuario no encontrado o credenciales incorrectas"}), 404

        if usuario.rol.lower() != 'administrador':
            return jsonify({"error": "Solo los usuarios con rol 'administrador' pueden asignar citas"}), 403

        agente = Usuario.query.get(agente_id)
        if not agente or agente.rol.lower() != 'agente':
            return jsonify({"error": "Solo los usuarios con rol 'agente' pueden ser asignados a citas"}), 403

        cita = Cita.query.get_or_404(cita_id)
        cita.agente_id = agente_id
        cita.fecha_cierre = None
        cita.estado = 'pendiente'
        db.session.commit()

        return jsonify({"mensaje": "Cita asignada al agente exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para Ver Citas Pendientes
@app.route('/citas_pendientes', methods=['GET'])
def ver_citas_pendientes():
    try:
        citas = Cita.query.filter_by(estado='pendiente').all()
        citas_list = [{"id": cita.id, "fecha": cita.fecha,
                       "proyecto": cita.proyecto,
                       "consulta": cita.consulta,
                       "cliente_id": cita.usuario_id,
                       "agente_id": cita.agente_id if cita.agente_id else None,
                       "fecha_cierre": cita.fecha_cierre if cita.fecha_cierre else None} for cita in citas]
        return jsonify(citas_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Ruta para Ver Citas 
@app.route('/citas', methods=['GET'])
def ver_citas():
    try:
        citas = Cita.query.all()
        citas_list = [{"id_cita": cita.id, "fecha": cita.fecha,
                       "proyecto": cita.proyecto,
                       "consulta": cita.consulta,
                       "cliente_id": cita.usuario_id,
                       "agente_id": cita.agente_id if cita.agente_id else None,
                       "fecha_cierre": cita.fecha_cierre if cita.fecha_cierre else None} for cita in citas]
        return jsonify(citas_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para Cambiar el Estado de una Cita a 'Completada'
@app.route('/cerrar_cita/<int:cita_id>', methods=['POST'])
def cerrar_cita(cita_id):
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')

        if not correo or not password:
            return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

        usuario = Usuario.query.filter_by(correo=correo, password=password).first()
        if not usuario:
            return jsonify({"error": "Credenciales incorrectas"}), 403

        if usuario.rol.lower() not in ['administrador', 'agente']:
            return jsonify({"error": "No tiene permisos para cerrar citas"}), 403

        cita = Cita.query.get_or_404(cita_id)
        cita.estado = 'completada'
        cita.fecha_cierre = datetime.now()
        db.session.commit()

        return jsonify({"mensaje": "Cita cerrada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Ruta para Reabrir una Cita Completada
@app.route('/abrir_cita/<int:cita_id>', methods=['POST'])
def abrir_cita(cita_id):
    try:
        data = request.get_json()
        correo = data.get('correo')
        password = data.get('password')

        if not correo or not password:
            return jsonify({"error": "Correo y contraseña son obligatorios"}), 400

        usuario = Usuario.query.filter_by(correo=correo, password=password).first()
        if not usuario:
            return jsonify({"error": "Credenciales incorrectas"}), 403

        if usuario.rol.lower() not in ['administrador', 'agente']:
            return jsonify({"error": "No tiene permisos para reabrir citas"}), 403

        cita = Cita.query.get_or_404(cita_id)
        cita.estado = 'pendiente'
        cita.fecha_cierre = None
        db.session.commit()

        return jsonify({"mensaje": "Cita reabierta exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
