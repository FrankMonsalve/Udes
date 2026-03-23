from app import create_app, db

# Creamos la instancia de la aplicación Flask
app = create_app()

# Punto de entrada para ejecutar el servidor de desarrollo
if __name__ == '__main__':
    app.run(debug=True)
