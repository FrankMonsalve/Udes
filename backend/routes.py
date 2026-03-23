from flask import Blueprint, request, jsonify
from app import db, mail
from flask_mail import Message
from models import Usuario, Aspirante, Programa
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Endpoint para la pre-inscripción del aspirante (Registro básico)
@main_bp.route('/pre-registro', methods=['POST'])
def pre_registro():
    datos = request.json
    
    # Se crea el usuario para el aspirante usando su número de documento como username y contraseña inicial
    password_hash = generate_password_hash(datos['numero_documento'])
    usuario = Usuario(
        nombre_usuario=datos['numero_documento'], 
        contrasena=password_hash, 
        rol='ASP', 
        nombre_completo=f"{datos['nombres']} {datos['apellidos']}"
    )
    db.session.add(usuario)
    db.session.flush()

    # Se crea el registro del aspirante con la información proporcionada
    aspirante = Aspirante(
        usuario_id = usuario.id,
        tipo_documento = datos['tipo_documento'],
        numero_documento = datos['numero_documento'],
        nombres = datos['nombres'],
        apellidos = datos['apellidos'],
        genero = datos['genero'],
        celular = datos['celular'],
        correo = datos['correo'],
        tipo_aspirante = datos['tipo_aspirante'],
        programa_id = datos['programa_id'],
        estado = 'PRE-INSCRIPCION'
    )
    db.session.add(aspirante)
    db.session.commit()
    
    # Enviar correos de notificacion
    try:
        # 1. Correo al Aspirante (ASP)
        msg_asp = Message(
            'Bienvenido a la UDES - Credenciales de Acceso',
            recipients=[datos['correo']]
        )
        msg_asp.body = f"""
        Hola {datos['nombres']},
        
        Su pre-inscripcion en la UDES ha sido exitosa.
        Puede continuar diligenciando su informacion en el portal
        
        Credenciales:
        Usuario: {datos['numero_documento']}
        Contrasena: {datos['numero_documento']}
        
        Atentamente,
        Universidad de Santander (UDES)
        """
        mail.send(msg_asp)
        
        # 2. Correo a Administrativos (RYC, MEI, CPG)
        admins = Usuario.query.filter(Usuario.rol.in_(['RYC', 'MEI', 'CPG'])).all()
        admin_emails = [a.correo for a in admins if a.correo]
        
        if admin_emails:
            msg_admin = Message(
                'Nueva Pre-inscripcion Recibida - UDES',
                recipients=admin_emails
            )
            msg_admin.body = f"""
            Se ha registrado una nueva pre-inscripcion:
            
            Nombre: {datos['nombres']} {datos['apellidos']}
            Documento: {datos['numero_documento']}
            Programa ID: {datos['programa_id']}
            
            Favor revisar el panel administrativo.
            """
            mail.send(msg_admin)
        
    except Exception as e:
        print(f"Error enviando correos: {str(e)}")
    
    return jsonify({"mensaje": "Pre-registro exitoso", "usuario_id": usuario.id}), 201

# Endpoint para el inicio de sesión (Simplificado sin JWT)
@main_bp.route('/login', methods=['POST'])
def login():
    datos = request.json
    usuario = Usuario.query.filter_by(nombre_usuario=datos['username']).first()
    
    if usuario and check_password_hash(usuario.contrasena, datos['password']):
        return jsonify(rol=usuario.rol, usuario_id=usuario.id)
    
    return jsonify({"msg": "Usuario o contraseña incorrectos"}), 401

# Endpoint para obtener el perfil del aspirante por ID de usuario
@main_bp.route('/aspirante/perfil/<int:usuario_id>', methods=['GET'])
def obtener_perfil(usuario_id):
    aspirante = Aspirante.query.filter_by(usuario_id=usuario_id).first()
    
    if not aspirante:
        return jsonify({"msg": "Aspirante no encontrado"}), 404
    
    if aspirante.estado == 'PRE-INSCRIPCION':
        aspirante.estado = 'DILIGENCIANDO FORMULARIO'
        db.session.commit()
        
    return jsonify({
        "id": aspirante.id,
        "usuario_id": aspirante.usuario_id,
        "nombres": aspirante.nombres,
        "apellidos": aspirante.apellidos,
        "correo": aspirante.correo,
        "celular": aspirante.celular,
        "tipo_documento": aspirante.tipo_documento,
        "numero_documento": aspirante.numero_documento,
        "tipo_aspirante": aspirante.tipo_aspirante,
        "programa_id": aspirante.programa_id,
        "programa_nombre": Programa.query.get(aspirante.programa_id).nombre if aspirante.programa_id else None,
        "estado": aspirante.estado,
        "estrato": aspirante.estrato,
        "fecha_nacimiento": aspirante.fecha_nacimiento.isoformat() if aspirante.fecha_nacimiento else None,
        "lugar_nacimiento": aspirante.lugar_nacimiento,
        "direccion_residencia": aspirante.direccion_residencia,
        "motivacion": aspirante.motivacion,
        "medio_enterado": aspirante.medio_enterado,
        "canal_informativo": aspirante.canal_informativo
    })

# Endpoint para actualizar datos complementarios del aspirante
@main_bp.route('/aspirante/actualizar-perfil/<int:usuario_id>', methods=['POST'])
def actualizar_perfil(usuario_id):
    aspirante = Aspirante.query.filter_by(usuario_id=usuario_id).first()
    datos = request.json
    
    if datos.get('fecha_nacimiento'):
        aspirante.fecha_nacimiento = datetime.strptime(datos['fecha_nacimiento'], '%Y-%m-%d').date()
    
    aspirante.lugar_nacimiento = datos.get('lugar_nacimiento')
    aspirante.direccion_residencia = datos.get('direccion_residencia')
    aspirante.estrato = datos.get('estrato')
    
    # MEI puede editar campos básicos también
    if datos.get('nombres'):
        aspirante.nombres = datos.get('nombres')
    if datos.get('apellidos'):
        aspirante.apellidos = datos.get('apellidos')
    if datos.get('correo'):
        aspirante.correo = datos.get('correo')
    if datos.get('celular'):
        aspirante.celular = datos.get('celular')
    if datos.get('tipo_aspirante'):
        aspirante.tipo_aspirante = datos.get('tipo_aspirante')
    if datos.get('programa_id'):
        aspirante.programa_id = datos.get('programa_id')
    
    # Encuesta
    if datos.get('motivacion'):
        aspirante.motivacion = datos.get('motivacion')
    if datos.get('medio_enterado'):
        aspirante.medio_enterado = datos.get('medio_enterado')
    if datos.get('canal_informativo'):
        aspirante.canal_informativo = datos.get('canal_informativo')

    db.session.commit()
    return jsonify({"mensaje": "Perfil actualizado exitosamente"})

# Endpoint para la carga de documentos (Simulado con guardado de nombres de archivo)
@main_bp.route('/aspirante/cargar-documentos/<int:usuario_id>', methods=['POST'])
def cargar_documentos(usuario_id):
    aspirante = Aspirante.query.filter_by(usuario_id=usuario_id).first()
    if not aspirante:
        return jsonify({"msg": "Aspirante no encontrado"}), 404

    archivos = request.files
    # En un entorno real guardaríamos los archivos en disco
    # Aquí simularemos que se guardaron y actualizaremos los nombres en la BD
    if 'foto' in archivos:
        aspirante.foto_archivo = secure_filename(archivos['foto'].filename)
    if 'documento' in archivos:
        aspirante.documento_id_archivo = secure_filename(archivos['documento'].filename)
    if 'diploma' in archivos:
        aspirante.diploma_archivo = secure_filename(archivos['diploma'].filename)
    
    db.session.commit()
    return jsonify({"mensaje": "Documentos cargados exitosamente"})

# Endpoint para guardar la encuesta de mercadeo
@main_bp.route('/aspirante/encuesta/<int:usuario_id>', methods=['POST'])
def guardar_encuesta(usuario_id):
    aspirante = Aspirante.query.filter_by(usuario_id=usuario_id).first()
    datos = request.json
    
    aspirante.motivacion = datos.get('motivacion')
    aspirante.medio_enterado = datos.get('medio_enterado')
    aspirante.canal_informativo = datos.get('canal_informativo')
    
    db.session.commit()
    return jsonify({"mensaje": "Encuesta guardada exitosamente"})

# Endpoint para confirmar la inscripción final
@main_bp.route('/aspirante/confirmar/<int:usuario_id>', methods=['POST'])
def confirmar_inscripcion(usuario_id):
    aspirante = Aspirante.query.filter_by(usuario_id=usuario_id).first()
    aspirante.estado = 'FINALIZO INSCRIPCION'
    db.session.commit()
    return jsonify({"mensaje": "Inscripción confirmada satisfactoriamente"})

# Endpoint administrativo para listar aspirantes (Abierto)
@main_bp.route('/admin/aspirantes', methods=['GET'])
def listar_aspirantes():
    aspirantes = Aspirante.query.all()
    return jsonify([{
        "id": a.id,
        "usuario_id": a.usuario_id,
        "nombre_completo": f"{a.nombres} {a.apellidos}",
        "estado": a.estado,
        "numero_documento": a.numero_documento,
        "programa_id": a.programa_id
    } for a in aspirantes])

# Acciones Administrativas (RYC, MEI, CPG)

@main_bp.route('/admin/aprobar-ryc/<int:aspirante_id>', methods=['POST'])
def aprobar_ryc(aspirante_id):
    aspirante = Aspirante.query.get_or_404(aspirante_id)
    aspirante.estado = 'APROBADO'
    db.session.commit()
    return jsonify({"mensaje": "Inscripción aprobada por Registro y Control"})

@main_bp.route('/admin/rechazar-cpg/<int:aspirante_id>', methods=['POST'])
def rechazar_cpg(aspirante_id):
    aspirante = Aspirante.query.get_or_404(aspirante_id)
    aspirante.estado = 'RECHAZADO'
    db.session.commit()
    return jsonify({"mensaje": "Inscripción rechazada"})

@main_bp.route('/admin/admitir-cpg/<int:aspirante_id>', methods=['POST'])
def admitir_cpg(aspirante_id):
    aspirante = Aspirante.query.get_or_404(aspirante_id)
    aspirante.estado = 'ADMITIDO'
    db.session.commit()
    return jsonify({"mensaje": "Aspirante admitido satisfactoriamente"})

# Endpoint para obtener la lista de programas ofertados
@main_bp.route('/programas', methods=['GET'])
def listar_programas():
    programas = Programa.query.all()
    return jsonify([{"id": p.id, "nombre": p.nombre} for p in programas])
