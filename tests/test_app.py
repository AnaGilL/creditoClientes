import re
import tempfile
import unittest
from pathlib import Path

from app import app, connect_db, init_db


class ClientRoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_config = {
            key: app.config[key]
            for key in ("DATABASE", "TESTING", "SECRET_KEY", "WTF_CSRF_ENABLED")
        }
        app.config.update(
            DATABASE=Path(self.temp_dir.name) / "test.db",
            TESTING=True,
            SECRET_KEY="test-secret-key",
            WTF_CSRF_ENABLED=True,
        )
        init_db()
        self.client = app.test_client()
        response = self.client.get("/")
        token_match = re.search(
            rb'name="csrf_token" value="([^"]+)"', response.data
        )
        self.assertIsNotNone(token_match)
        self.csrf_token = token_match.group(1).decode()

    def tearDown(self):
        app.config.update(self.original_config)
        self.temp_dir.cleanup()

    def create_client(self, **fields):
        data = {
            "csrf_token": self.csrf_token,
            "nombre": "Cliente de prueba",
            "empresa": "Empresa de prueba",
            "correo": "cliente@example.com",
            "telefono": "555-0100",
            "notas": "Nota de prueba",
        }
        data.update(fields)
        return self.client.post("/clientes/guardar", data=data)

    def get_client_id(self, name="Cliente de prueba"):
        with connect_db() as connection:
            row = connection.execute(
                "SELECT id FROM clientes WHERE nombre = ?", (name,)
            ).fetchone()
        return row["id"]

    def test_index_shows_empty_directory(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Tu directorio empieza aquí".encode(), response.data)
        self.assertIn(b"0 clientes", response.data)

    def test_create_client(self):
        response = self.create_client()

        self.assertEqual(response.status_code, 302)
        page = self.client.get("/")
        self.assertIn("Cliente de prueba".encode(), page.data)
        self.assertIn(b"Cliente agregado.", page.data)

    def test_search_matches_client_fields(self):
        self.create_client()
        self.create_client(nombre="Otra persona", empresa="Otra empresa")

        response = self.client.get("/?q=Empresa%20de%20prueba")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Cliente de prueba".encode(), response.data)
        self.assertNotIn("Otra persona".encode(), response.data)

    def test_update_client(self):
        self.create_client()
        client_id = self.get_client_id()

        response = self.create_client(
            id=str(client_id),
            nombre="Cliente actualizado",
            empresa="Nueva empresa",
        )

        self.assertEqual(response.status_code, 302)
        with connect_db() as connection:
            row = connection.execute(
                "SELECT nombre, empresa FROM clientes WHERE id = ?", (client_id,)
            ).fetchone()
        self.assertEqual(row["nombre"], "Cliente actualizado")
        self.assertEqual(row["empresa"], "Nueva empresa")

    def test_delete_client(self):
        self.create_client()
        client_id = self.get_client_id()

        response = self.client.post(
            f"/clientes/{client_id}/eliminar",
            data={"csrf_token": self.csrf_token},
        )

        self.assertEqual(response.status_code, 302)
        with connect_db() as connection:
            count = connection.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        self.assertEqual(count, 0)

    def test_name_is_required(self):
        response = self.create_client(nombre="   ")

        self.assertEqual(response.status_code, 302)
        page = self.client.get("/")
        self.assertIn("El nombre es obligatorio.".encode(), page.data)
        with connect_db() as connection:
            count = connection.execute("SELECT COUNT(*) FROM clientes").fetchone()[0]
        self.assertEqual(count, 0)

    def test_post_without_csrf_token_is_rejected(self):
        response = self.client.post(
            "/clientes/guardar", data={"nombre": "Sin token"}
        )

        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()