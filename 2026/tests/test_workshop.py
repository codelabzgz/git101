import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import app, load_snippets
from freeze import build_site
from validate import validate_snippets

EXAMPLE = dict(slug="ejemplo", author="Lucía", title="Un café", language="python",
               code='print("¡Hola!")', description="Descripción con tildes.")


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.directory = Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)

    def save(self, data=EXAMPLE, filename="ejemplo.json", encoding="utf-8"):
        (self.directory / filename).write_text(json.dumps(data, ensure_ascii=False), encoding=encoding)

    def test_valid_unicode(self):
        self.save()
        self.assertEqual(validate_snippets(self.directory), [])

    def test_windows_bom(self):
        self.save(encoding="utf-8-sig")
        self.assertEqual(validate_snippets(self.directory), [])

    def test_empty_folder(self):
        self.assertTrue(validate_snippets(self.directory))

    def test_broken_json(self):
        (self.directory / "ejemplo.json").write_text('{"slug":', encoding="utf-8")
        self.assertTrue(validate_snippets(self.directory))

    def test_not_object(self):
        for value in [[], None, 42, "texto"]:
            with self.subTest(value=value):
                self.save(value)
                self.assertTrue(validate_snippets(self.directory))

    def test_missing_field(self):
        data = EXAMPLE.copy()
        del data["code"]
        self.save(data)
        self.assertTrue(validate_snippets(self.directory))

    def test_wrong_type(self):
        for value in [None, [], {}, 123, False]:
            with self.subTest(value=value):
                self.save(dict(EXAMPLE, code=value))
                self.assertTrue(validate_snippets(self.directory))

    def test_empty_text(self):
        self.save(dict(EXAMPLE, title="   "))
        self.assertTrue(validate_snippets(self.directory))

    def test_slug_format(self):
        for slug in ["../fuera", "Nombre", "con espacios", "café", "a--b", ""]:
            with self.subTest(slug=slug):
                self.save(dict(EXAMPLE, slug=slug))
                self.assertTrue(validate_snippets(self.directory))

    def test_name_mismatch(self):
        self.save(filename="otro.json")
        self.assertTrue(validate_snippets(self.directory))

    def test_large_file(self):
        self.save(dict(EXAMPLE, code="x" * 33_000))
        self.assertTrue(validate_snippets(self.directory))

    def test_bad_encoding(self):
        (self.directory / "ejemplo.json").write_bytes(b'\xff\xff')
        self.assertTrue(validate_snippets(self.directory))


class WebsiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name) / "snippets"
        self.directory.mkdir()
        (self.directory / "ejemplo.json").write_text(json.dumps(EXAMPLE, ensure_ascii=False), encoding="utf-8")
        self.config = patch.dict(app.config, TESTING=True, SNIPPETS_DIR=self.directory)
        self.config.start()
        self.addCleanup(self.config.stop)
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Un café", response.get_data(as_text=True))

    def test_detail_unicode(self):
        response = self.client.get("/snippet/ejemplo.html")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Lucía", response.get_data(as_text=True))

    def test_missing(self):
        self.assertEqual(self.client.get("/snippet/no-existe.html").status_code, 404)

    def test_bad_slug(self):
        self.assertEqual(self.client.get("/snippet/..html").status_code, 404)

    def test_escape_html(self):
        data = dict(EXAMPLE, code='<script>alert("x")</script>', title="<b>hola</b>")
        (self.directory / "ejemplo.json").write_text(json.dumps(data), encoding="utf-8")
        html = self.client.get("/snippet/ejemplo.html").get_data(as_text=True)
        self.assertNotIn('<script>alert(', html)
        self.assertIn("&lt;script&gt;", html)

    def test_assets(self):
        for name in ["style.css", "codelabzgz-logo.png"]:
            with self.subTest(name=name):
                response = self.client.get(f"/static/{name}")
                self.assertEqual(response.status_code, 200)
                response.close()

    def test_working_directory_independent(self):
        old = Path.cwd()
        try:
            os.chdir(self.temp.name)
            self.assertEqual(load_snippets()[0]["author"], "Lucía")
        finally:
            os.chdir(old)

    def test_export_relative_links(self):
        destination = Path(self.temp.name) / "build"
        with patch.dict(app.config):
            build_site(destination)
        self.assertTrue((destination / "index.html").is_file())
        self.assertTrue((destination / "snippet/ejemplo.html").is_file())
        self.assertTrue((destination / "static/style.css").is_file())
        self.assertIn('href="../static/style.css"', (destination / "snippet/ejemplo.html").read_text(encoding="utf-8"))
        self.assertIn('href="../index.html"', (destination / "snippet/ejemplo.html").read_text(encoding="utf-8"))


@unittest.skipUnless(shutil.which("git"), "Git no está instalado")
class GitExerciseTests(unittest.TestCase):
    def test_conflict_and_resolution(self):
        with tempfile.TemporaryDirectory(prefix="git101-exercise-") as directory:
            root = Path(directory)
            def git(*args, check=True):
                return subprocess.run(["git", "-c", f"safe.directory={root.as_posix()}", *args],
                    cwd=root, text=True, capture_output=True, check=check)
            git("init", "-b", "main")
            git("config", "user.name", "Taller CodeLab")
            git("config", "user.email", "taller@example.invalid")
            git("config", "commit.gpgsign", "false")
            git("config", "core.autocrlf", "false")
            file = root / "lema.txt"
            file.write_text("Lema inicial\n", encoding="utf-8")
            git("add", "lema.txt")
            git("commit", "-m", "Lema inicial")
            git("switch", "-c", "propuesta")
            file.write_text("Version propuesta\n", encoding="utf-8")
            git("commit", "-am", "Propuesta")
            git("switch", "main")
            file.write_text("Version principal\n", encoding="utf-8")
            git("commit", "-am", "Principal")
            result = git("merge", "propuesta", check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("<<<<<<<", file.read_text(encoding="utf-8"))
            file.write_text("Lema acordado\n", encoding="utf-8")
            git("add", "lema.txt")
            git("commit", "-m", "Resuelve el conflicto")
            self.assertEqual(git("status", "--porcelain").stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
