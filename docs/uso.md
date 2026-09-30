# Guía de uso

## Requisitos

- Python 3.10 o posterior.
- Acceso a internet durante la instalación de dependencias. La interfaz carga las fuentes DM Sans y Manrope desde Google Fonts; sin conexión usa fuentes alternativas.

## Instalación y arranque

Desde la raíz del repositorio, crea un entorno virtual e instala las dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Inicia el servidor de desarrollo:

```bash
python app.py
```

Abre http://127.0.0.1:5000. La aplicación crea `clientes.db` y la tabla `clientes` automáticamente si aún no existen. Para detener el servidor, pulsa `Ctrl+C` en la terminal.

Para activar el depurador local:

```bash
FLASK_DEBUG=1 python app.py
```

No habilites el modo de depuración en un entorno accesible por otras personas.

## Administrar clientes

### Agregar

Pulsa **Agregar cliente**, completa el nombre obligatorio y los campos opcionales, y selecciona **Guardar cliente**. Correo, teléfono y notas pueden dejarse vacíos.

### Consultar y buscar

La página principal muestra el directorio ordenado alfabéticamente y métricas de la cartera. El campo de búsqueda encuentra coincidencias en nombre, empresa, correo y teléfono. Usa el botón de limpiar búsqueda para volver a ver todos los registros.

### Editar

En la fila correspondiente, pulsa **Editar**. El formulario se rellenará con los datos actuales. Guarda los cambios para actualizar el registro.

### Eliminar

Pulsa **Eliminar** en la fila del cliente y confirma la acción en el navegador. La eliminación es permanente en la base de datos.

## Pruebas

Con el entorno virtual activo, ejecuta:

```bash
python -m unittest discover -s tests -v
```

Las pruebas crean bases SQLite temporales y no modifican el directorio local.

## Datos y copias de seguridad

Los datos se guardan en `clientes.db`, ignorado por Git. Para respaldar el directorio, detén la aplicación y copia ese archivo a un lugar seguro. No compartas la base sin revisar que su contenido pueda divulgarse: incluye información personal de clientes.

Para configuración de despliegue y seguridad, consulta [Arquitectura](arquitectura.md) y el [README principal](../README.md).