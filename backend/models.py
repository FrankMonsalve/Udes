from app import db
from datetime import datetime

# Modelo para Programas Académicos
class Programa(db.Model):
    __tablename__ = 'programa'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text)

# Modelo para Usuarios del Sistema (Aspirantes y Personal Administrativo)
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False) # Para ASP será su número de documento
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(10), nullable=False) # Roles: ASP, RYC, MEI, CPG
    nombre_completo = db.Column(db.String(255))
    correo = db.Column(db.String(100))
    programa_id = db.Column(db.Integer, db.ForeignKey('programa.id')) # Solo aplica para coordinadores (CPG)
    
    # Relación uno a uno con la información del aspirante
    aspirante = db.relationship('Aspirante', backref='usuario', uselist=False)

# Modelo para la información detallada de la inscripción del Aspirante
class Aspirante(db.Model):
    __tablename__ = 'aspirante'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    tipo_documento = db.Column(db.String(20))
    numero_documento = db.Column(db.String(20), unique=True)
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    genero = db.Column(db.String(20))
    celular = db.Column(db.String(20))
    correo = db.Column(db.String(100))
    tipo_aspirante = db.Column(db.String(50)) # Nacional, Internacional, Transferencia, etc.
    programa_id = db.Column(db.Integer, db.ForeignKey('programa.id'))
    
    # Datos complementarios (Tab 1)
    fecha_nacimiento = db.Column(db.Date)
    lugar_nacimiento = db.Column(db.String(100))
    direccion_residencia = db.Column(db.String(200))
    estrato = db.Column(db.Integer)
    
    # Nombres de archivos de documentos (Tab 2)
    foto_archivo = db.Column(db.String(255))
    documento_id_archivo = db.Column(db.String(255))
    diploma_archivo = db.Column(db.String(255))
    
    # Encuesta de mercadeo (Tab 3)
    motivacion = db.Column(db.Text)
    medio_enterado = db.Column(db.String(100))
    canal_informativo = db.Column(db.String(100))
    
    # Estado de la inscripción
    estado = db.Column(db.String(50), default='PRE-INSCRIPCION')
    # Estados: PRE-INSCRIPCION, DILIGENCIANDO FORMULARIO, FINALIZO INSCRIPCION, APROBADO, ADMITIDO, RECHAZADO
    
    observaciones = db.Column(db.Text)
    creado_en = db.Column(db.DateTime, default=datetime.utcnow)
    actualizado_en = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
