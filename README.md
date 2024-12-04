# Proyecto Inmobiliaria

Este proyecto está basado en Flask y utiliza varias bibliotecas para manejar bases de datos y migraciones.

### Requisitos para el entorno

- Python 3.x
- SQLite (base de datos local)

### Instrucciones para iniciar el proyecto

1. **Clonar el repositorio:**
   Primero, clona el repositorio en tu máquina local:
   ```bash
   git clone https://github.com/ErickAguilarGomez/proyecto-inmobiliaria.git
   cd proyecto-inmobiliaria
   ```

### Instrucciones para iniciar el proyecto

2. **Crear un entorno virtual:**

   Es recomendable crear un entorno virtual para manejar las dependencias del proyecto:

   ```bash
   python3 -m venv venv
   ```

   ```bash
   Activar el entorno virtual:
   En Windows:
   venv\Scripts\activate

   En Mac/Linux:
   source venv/bin/activate
   ```

3. Instalar las dependencias:
   Asegúrate de tener todas las bibliotecas necesarias instaladas ejecutando:

   ```bash
   pip install -r requirements.txt
   ```

4. Configurar la base de datos:

El proyecto usa SQLite, por lo que se creará un archivo site.db dentro de la carpeta instance/ cuando se ejecute la primera vez. Si es necesario, también puedes ejecutar las migraciones con Flask-Migrate:

Inicializar las migraciones:

   ```bash
      flask db init
   ```

5. Realizar las migraciones:
   ```bash
flask db migrate
   ```
6. Aplicar las migraciones:
```bash
flask db upgrade
```
7. Ejecutar la aplicación:
Una vez que las dependencias estén instaladas y la base de datos esté configurada, puedes iniciar el servidor de desarrollo de Flask con el siguiente comando:
   
  ```bash
   flask run
   ```

La aplicación estará disponible en http://127.0.0.1:5000/ por defecto. Abre esta URL en tu navegador para acceder a la aplicación.
