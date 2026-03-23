from app import db
from models import Programa, Usuario, Aspirante
from werkzeug.security import generate_password_hash
from flask.cli import with_appcontext
import click

# Comando CLI para inicializar la base de datos con datos de prueba
@click.command("seed-db")
@with_appcontext
def seed_db_command():
    """Inicializa la base de datos con datos de prueba."""
    from flask import current_app
    click.echo(f"Sembrando base de datos en: {current_app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Limpiamos tablas para evitar conflictos de integridad
    db.session.query(Aspirante).delete()
    db.session.query(Usuario).delete()
    db.session.query(Programa).delete()
    db.session.commit()
    
    # Creamos algunos programas academicos basicos
    p1 = Programa(nombre="Ingeniería de Sistemas", descripcion="Programa de formación en tecnología")
    p2 = Programa(nombre="Enfermería", descripcion="Programa de formación en salud")
    p3 = Programa(nombre="Derecho", descripcion="Programa de formación en leyes")
    db.session.add_all([p1, p2, p3])
    db.session.commit()

    # Usuario para Registro y Control (RYC)
    ryc = Usuario(
        nombre_usuario='ryc1', 
        contrasena=generate_password_hash('password'), 
        rol='RYC', 
        nombre_completo='Personal Registro y Control',
        correo='frankmonsalve27@gmail.com'
    )
    
    # Usuario para Mercadeo Institucional (MEI)
    mei = Usuario(
        nombre_usuario='mei1', 
        contrasena=generate_password_hash('password'), 
        rol='MEI', 
        nombre_completo='Personal Mercadeo',
        correo='frankmonsalve27@gmail.com'
    )
    
    # Usuarios para Coordinadores de Programa (CPG)
    cpg1 = Usuario(
        nombre_usuario='cpg_sistemas', 
        contrasena=generate_password_hash('password'), 
        rol='CPG', 
        nombre_completo='Coordinador Sistemas', 
        programa_id=p1.id,
        correo='frankmonsalve27@gmail.com'
    )
    cpg2 = Usuario(
        nombre_usuario='cpg_enfermeria', 
        contrasena=generate_password_hash('password'), 
        rol='CPG', 
        nombre_completo='Coordinador Enfermería', 
        programa_id=p2.id,
        correo='frankmonsalve27@gmail.com'
    )
    cpg3 = Usuario(
        nombre_usuario='cpg_derecho', 
        contrasena=generate_password_hash('password'), 
        rol='CPG', 
        nombre_completo='Coordinador Derecho', 
        programa_id=p3.id,
        correo='frankmonsalve27@gmail.com'
    )

    # Agregamos todos los usuarios administrativos a la base de datos
    db.session.add_all([ryc, mei, cpg1, cpg2, cpg3])
    db.session.commit()
    
    click.echo("¡Base de datos inicializada exitosamente!")
