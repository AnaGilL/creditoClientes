# Nexo: directorio de clientes

Aplicación web CRUD en Python con Flask y SQLite. Permite crear, consultar, buscar, editar y eliminar clientes; los datos se conservan en `clientes.db`.

## Ejecutar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abre http://127.0.0.1:5000. La base de datos se crea automáticamente al iniciar.

## Ejecutar las pruebas

```bash
python -m unittest discover -s tests -v
```

Antes de desplegar, define una clave secreta propia en la variable de entorno `SECRET_KEY` y ejecuta la aplicación detrás de un servidor WSGI de producción.
