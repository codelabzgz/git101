# Git 101 · Edición 2026

Taller práctico de Git y GitHub para principiantes. El objetivo es crear un historial local, trabajar en ramas, resolver un conflicto y abrir un pull request para una web compartida.

## Materiales

- [Guion del ponente](GUION.md): explicaciones, tiempos, comandos, puntos de control y errores frecuentes.
- `snippets/hola.json`: ejemplo que cada participante copia con otro nombre.
- `tests/test_workshop.py`: 21 pruebas de validación, páginas, exportación y conflicto real de Git.
- `taller.ps1`: arranque y pruebas en Windows.
- `conflictos/PARTICIPANTES.md`: material opcional para la demostración; el conflicto reproducible está en el guion.

Reserva dos horas: 90 minutos de contenido y 30 para ayuda. El alumnado solo necesita Git, editor y cuenta de GitHub. Python y Flask son herramientas de la organización, no requisitos del taller.

## Entorno de la organización

Usa Python 3.11 o 3.12. Desde la raíz del repositorio, en PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r .\2026\requirements.txt
.\2026\taller.ps1 probar
.\2026\taller.ps1 exportar
.\2026\taller.ps1 servir
```

Si no tienes el lanzador py, usa la ruta de tu Python para crear el entorno. No hace falta activarlo ni cambiar la política de PowerShell. Si el equipo bloquea scripts, estas órdenes son equivalentes, desde 2026:

```powershell
..\.venv\Scripts\python.exe validate.py
..\.venv\Scripts\python.exe -m unittest discover -s tests -v
..\.venv\Scripts\python.exe freeze.py
..\.venv\Scripts\python.exe app.py
```

La web local escucha solo en http://127.0.0.1:5000. Ctrl+C la detiene. No uses este servidor de desarrollo como servicio público.

En macOS o Linux, desde la raíz:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r 2026/requirements.txt
cd 2026
../.venv/bin/python validate.py
../.venv/bin/python -m unittest discover -s tests -v
../.venv/bin/python freeze.py
../.venv/bin/python app.py
```

La exportación genera 2026/build. Sus enlaces relativos sirven tanto en local como en la subruta de GitHub Pages. Para probar esa exportación en un navegador, ejecuta desde 2026:

```powershell
..\.venv\Scripts\python.exe -m http.server 8000 --bind 127.0.0.1 --directory build
```

Abre http://127.0.0.1:8000. Los estilos y el logo están incluidos; no necesitan un CDN.

## Aporte del participante

1. Haz un fork de https://github.com/codelabzgz/git101 en tu cuenta.
2. Copia su URL HTTPS y clona ese fork, no el repositorio de la organización.
3. Crea una rama con `git switch -c snippet-tuusuario`.
4. Copia `2026/snippets/hola.json` a `2026/snippets/tuusuario.json`. Sustituye tuusuario por tu identificador, en minúsculas, con números o guiones.
5. Cambia slug para que coincida con el nombre del archivo, sin .json. Completa author, title, language, code y description con texto.
6. Revisa `git diff`. Prepara solo tu archivo con `git add 2026/snippets/tuusuario.json`.
7. Haz commit y `git push -u origin snippet-tuusuario`.
8. Abre un PR con destino codelabzgz/git101, rama main. Comprueba sus cambios y Checks.
9. Si el JSON falla, corrige, haz otro commit y push en la misma rama. El PR se actualiza.

El máximo por archivo es 32 KiB. JSON exige comillas dobles y no admite comentarios ni comas finales. La web muestra código como texto; nunca lo ejecuta. No publiques contraseñas, tokens ni datos personales innecesarios.

Para commits públicos, usa tu correo elegido para publicar o el noreply de GitHub. GitHub no acepta la contraseña normal de la cuenta para un push HTTPS: usa el acceso por navegador de Git Credential Manager o un método ya configurado. No pegues tokens en una pantalla compartida.

## Publicación de la organización

La preparación local no está publicada por el mero hecho de existir. Antes del taller:

1. Revisa los cambios y autoriza su publicación. Conserva 2025 como edición anterior.
2. Publica la edición 2026 en el repositorio y comprueba que ambas rutas de Actions siguen apuntando a 2026.
3. En Settings → Pages, selecciona GitHub Actions como origen.
4. Comprueba el workflow de validación y el de despliegue, la URL resultante y los enlaces de las tarjetas.
5. Ensaya un PR desde un fork. Los nuevos colaboradores pueden necesitar aprobación para ejecutar Actions.
6. Revisa cada contribución antes de fusionarla. La validación solo tiene permisos de lectura.
7. Conserva las contribuciones y el historial tras la sesión. No vacíes carpetas de una edición anterior.

Las pruebas locales comprueban el código y la exportación. No demuestran que los permisos de Pages ni el despliegue remoto estén configurados: esa verificación se hace en GitHub.

## Dependencias

requirements.txt fija las dependencias directas de la edición. requirements-lock.txt registra todas las versiones usadas en el ensayo local. Para reproducir ese entorno, instala este último archivo.

## Contacto

codelabzgz@unizar.es · https://codelabzgz.dev
