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
   flask db migrate

6. Aplicar las migraciones:
   flask db upgrade
7. Ejecutar la aplicación:
   Una vez que las dependencias estén instaladas y la base de datos esté configurada, puedes iniciar el servidor de desarrollo de Flask con el siguiente comando:

```bash
 flask run
```

La aplicación estará disponible en http://127.0.0.1:5000/ por defecto. Abre esta URL en tu navegador para acceder a la aplicación.

# Instrucciones para interactuar con la API

### 1. Crear un nuevo usuario

**POST** `http://127.0.0.1:5000/crear_usuario`

-Aquí debes crear el usuario y asignarle uno de los siguientes roles: **cliente**, **agente** o **administrador**.

```json
{
  "correo": "usuario1@gmail.com",
  "nombre": "clienteusuario",
  "password": "cliente",
  "rol": "cliente"
}
```

### 2. Obtener lista de usuarios
**GET** http://127.0.0.1:5000/usuarios

### 3. Crear una cita
**POST** http://127.0.0.1:5000/crear_cita

-Solo un usuario con el rol usuario o administrador podrá crear citas.

```json

{
  "proyecto": "Inmobiliaria",
  "consulta": "Quiero revisar los avances y entregables del proyecto",
  "usuario_id": "1"
}
```

### 4. Obtener citas pendientes
**GET**  http://127.0.0.1:5000/citas_pendientes

### 5. Obtener todas las citas
**GET**  http://127.0.0.1:5000/citas

-En esta URL verás todas las citas, sean pendientes o no.

### 6. Asignar una cita
**POST**  http://127.0.0.1:5000/asignar_cita/1

-Solo un usuario con el rol administrador podrá asignar citas. El agente_id debe ser un usuario con el rol agente. Debes colocar el ID de la cita en la URL.

```json

{
  "correo": "usuario3@gmail.com",
  "password": "administrador",
  "agente_id": "2"
}
```

### 7. Cerrar una cita
**POST**  http://127.0.0.1:5000/cerrar_cita/1

- Solo un agente podrá cerrar la cita. Debes colocar el ID de la cita en la URL.

```json

{
  "correo": "usuario2@gmail.com",
  "password": "agente"
}
```

### 8. Reabrir una cita
**POST** http://127.0.0.1:5000/abrir_cita/1

- Solo un agente o administrador podrá reabrir una cita. Debes colocar el ID de la cita en la URL.

```json

{
  "correo": "usuario2@gmail.com",
  "password": "agente"
}
```