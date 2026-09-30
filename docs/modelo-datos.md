# Modelo de datos

## Entidad `Cliente`

La aplicación almacena cada cliente como una fila de la tabla SQLite `clientes`.

| Campo | Tipo SQLite | Regla | Descripción |
| --- | --- | --- | --- |
| `id` | `INTEGER` | Clave primaria autoincremental | Identificador interno usado para editar y borrar. |
| `nombre` | `TEXT` | Obligatorio (`NOT NULL`) | Nombre que se muestra en el directorio. La aplicación rechaza nombres vacíos tras quitar espacios. |
| `empresa` | `TEXT` | `NOT NULL`, valor predeterminado `''` | Empresa asociada al cliente. |
| `correo` | `TEXT` | `NOT NULL`, valor predeterminado `''` | Correo electrónico. Se enlaza como `mailto:` cuando está presente. |
| `telefono` | `TEXT` | `NOT NULL`, valor predeterminado `''` | Teléfono. Se enlaza como `tel:` cuando está presente. |
| `notas` | `TEXT` | `NOT NULL`, valor predeterminado `''` | Notas libres sobre el cliente. |
| `creado_en` | `TEXT` | `NOT NULL`, valor predeterminado `CURRENT_TIMESTAMP` | Fecha y hora de creación asignada por SQLite. No se muestra ni se modifica desde la interfaz. |

Los campos de contacto y notas son opcionales en el formulario. La tabla usa cadenas vacías en lugar de `NULL` para esos valores.

## Relaciones e índices

Actualmente no hay otras entidades, claves foráneas ni índices adicionales. La empresa es un campo de texto en el registro del cliente, no una entidad normalizada. La métrica de empresas cuenta los valores distintos no vacíos.

La lista se ordena por nombre sin distinguir mayúsculas y minúsculas. La búsqueda aplica coincidencia parcial con `LIKE` a nombre, empresa, correo y teléfono; las notas y la fecha de creación no forman parte de la búsqueda.

## Persistencia y cambios de esquema

La ruta de la base se configura en `app.config["DATABASE"]` y por defecto apunta al archivo `clientes.db` junto a `app.py`. `init_db()` crea la tabla con `CREATE TABLE IF NOT EXISTS`; no aplica migraciones ni modifica tablas existentes. Para cambios futuros de esquema, habrá que planificar una migración antes de desplegar una versión incompatible.

El archivo de base de datos contiene información de clientes, no se versiona y debe respaldarse de forma segura. Las pruebas sustituyen la ruta por una base temporal aislada.