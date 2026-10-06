# Git 101 · Guion para quien imparte el taller

CodeLab · Edición 2026 · Sesión prevista para el 23 de octubre de 2026.
El mes se toma del contexto de preparación; confirma aula y horario antes de difundirlos.

## Objetivo y ritmo

Al terminar, cada participante debe guardar cambios con Git, crear una rama, resolver un conflicto y abrir un pull request con su propio fragmento de código. No necesita programar: puede copiar y adaptar el ejemplo.

Reserva dos horas. El contenido ocupa 90 minutos y deja 30 para instalaciones, acceso a GitHub y dudas. Si vas tarde, convierte parte de las ramas en demostración. Protege los 25 minutos del pull request.

| Minutos | Bloque | Resultado que debes comprobar |
| --- | --- | --- |
| 0–10 | Qué son Git y GitHub | Distinguen herramienta local y servicio web |
| 10–30 | Historial local | Dos commits y un árbol de trabajo limpio |
| 30–45 | Ramas | Una rama nueva y una fusión sencilla |
| 45–60 | Conflicto | Dos versiones de la misma línea y resolución |
| 60–85 | Fork y pull request | Contribución subida al fork y PR abierto |
| 85–90 | Web y cierre | Explicación de validación, despliegue y encuesta |

## Antes de empezar

Para participantes: portátil, Git instalado, editor de texto y cuenta de GitHub con correo verificado. En Windows, usa Git Bash para todos los comandos del taller. No les pidas instalar Python: solo lo necesita quien ejecuta la web o las pruebas.

Para organización: un ponente y, si es posible, una persona que ayude en las mesas. Amplía la letra de la terminal y prepara navegador, repositorio y web. Comprueba Wi-Fi, proyector, enchufes y autenticación antes de la sesión. Conserva la web estática generada como alternativa si falla Internet.

La edición 2026 debe estar publicada antes del taller. El contenido preparado solo en este equipo no aparece en los forks del alumnado. La organización debe comprobar un PR de ensayo desde un fork, su ejecución en Actions y su despliegue real en Pages. No publiques datos personales, claves ni tokens.

Prueba local de organización, desde la raíz de git101:

```powershell
.\2026\taller.ps1 probar
.\2026\taller.ps1 exportar
.\2026\taller.ps1 servir
```

El último comando abre un servidor local en http://127.0.0.1:5000. Déjalo en una terminal aparte; Ctrl+C lo detiene. Si PowerShell bloquea el script, usa directamente el Python del entorno, sin cambiar la política del equipo:

```powershell
.\.venv\Scripts\python.exe .\2026\app.py
```

## 1. Qué son Git y GitHub · 10 minutos

Empieza con una pregunta: «¿Cuántos tenéis archivos llamados final, final2 o definitivo?». Explica: «Git guarda versiones de un proyecto y permite comparar cambios. GitHub aloja repositorios y facilita revisar contribuciones. Git funciona sin GitHub y sin Internet».

Un repositorio contiene archivos y su historial. Un commit registra una versión con un mensaje y un identificador. Una rama permite continuar el trabajo desde un punto del historial. No es una copia manual de toda la carpeta.

Dibuja el recorrido: archivo editado → cambios preparados con add → versión guardada con commit → versión enviada con push. Un commit no sube nada a Internet. Guardar el archivo en el editor no crea un commit.

Pregunta de control: «Si se cae el Wi-Fi, ¿puedo hacer commits?». Respuesta: sí. «¿Un commit ya está en GitHub?». Respuesta: no.

## 2. Historial local · 20 minutos

Trabaja en una carpeta nueva. No ejecutes el ejercicio dentro del repositorio de una asignatura ni dentro del propio git101. Los siguientes comandos son para Git Bash, macOS o Linux.

```bash
git --version
mkdir git101-practica
cd git101-practica
git init -b main
git config user.name "Participante CodeLab"
git config user.email "participante@example.invalid"
git config core.editor "nano"
printf 'Lema inicial\n' > lema.txt
git status
git add lema.txt
git diff --staged
git commit -m "Añade el lema inicial"
git log --oneline
```

El nombre y correo son ejemplos para esta práctica local. Cada participante puede usar los suyos; los commits públicos dejan visible ese correo. Para GitHub, recomienda el correo noreply que aparece en los ajustes de su cuenta. Estas órdenes configuran solo este repositorio: no uses --global sin explicar su efecto.

Explica el estado antes de ejecutar cada orden. «Untracked» significa que Git aún no sigue ese archivo. add prepara la versión actual del archivo; no todas sus ediciones futuras. diff --staged muestra lo que entrará en el siguiente commit.

```bash
printf 'Lema inicial\nAprendemos juntos\n' > lema.txt
git diff
git add lema.txt
git commit -m "Añade una segunda línea"
git status
git log --oneline --graph --all
```

Checkpoint: cada persona debe ver dos commits y ningún cambio pendiente. No avances con media sala bloqueada.

Demuestra también git restore lema.txt tras editarlo sin confirmar. Antes de hacerlo, avisa: descarta cambios del archivo que no están preparados. Para sacar un cambio de la zona de preparación usa git restore --staged lema.txt; conserva la edición. No enseñes reset --hard ni push --force como soluciones generales.

## 3. Ramas y fusión · 15 minutos

```bash
git switch -c mejora
printf 'Lema inicial\nAprendemos juntos\nProbamos sin pisarnos\n' > lema.txt
git add lema.txt
git commit -m "Completa el lema en la rama mejora"
git switch main
cat lema.txt
git merge mejora
git log --oneline --graph --all
```

Explica antes de cambiar de rama: «Mirad el archivo. En main todavía no está la tercera línea». Tras merge, aparece. Aquí Git puede avanzar main directamente, porque no se han creado cambios divergentes en main: es una fusión fast-forward.

Una rama no es un usuario, y trabajar en ramas no evita todos los conflictos. Antes de switch o merge, consulta status y guarda o confirma el trabajo. No hace falta borrar las ramas durante la charla.

## 4. Conflicto reproducible · 15 minutos

Usa el mismo repositorio local. Dos ramas deben modificar la misma línea desde un antepasado común. Que toda la sala edite archivos parecidos en repositorios distintos no provoca por sí solo un conflicto.

```bash
git switch -c propuesta
printf 'Git nos une\n' > lema.txt
git add lema.txt
git commit -m "Propone el lema de la rama"
git switch main
printf 'Versionamos juntos\n' > lema.txt
git add lema.txt
git commit -m "Propone el lema de main"
git merge propuesta
git status
cat lema.txt
```

La fusión debe detenerse con un conflicto. Explica las tres marcas: <<<<<<< inicia la versión actual; ======= separa versiones; >>>>>>> cierra la versión que se fusiona. Git no sabe cuál expresa nuestra intención. No se ha perdido el historial.

Elige un texto que combine las ideas y elimina todas las marcas. Puedes editar el archivo o ejecutar:

```bash
printf 'Git nos une: versionamos juntos\n' > lema.txt
git add lema.txt
git commit -m "Acuerda un lema y resuelve el conflicto"
git status
git log --oneline --graph --all
```

add marca el archivo como resuelto; commit termina la fusión. No pulses «aceptar actual» o «aceptar entrante» sin leer ambos cambios. Si quieres volver al estado previo a esta fusión, git merge --abort sirve mientras siga abierta. Hazlo solo en esta práctica, que empezó sin cambios pendientes.

Checkpoint: status debe quedar limpio. Pregunta: «¿Quién decidió el contenido final, Git o nosotros?».

## 5. GitHub, fork y pull request · 25 minutos

Abre https://github.com/codelabzgz/git101 y muestra el botón Fork. Explica: fork crea una copia del repositorio en la cuenta de GitHub; clone crea una copia en el ordenador. No son lo mismo. Quien no tenga permisos en CodeLab debe subir al fork, no al repositorio de la organización.

Cada participante hace el fork en el navegador y copia su URL HTTPS desde el botón Code. Vuelve a la carpeta superior de la práctica; no clones dentro de git101-practica. Este ejemplo usa la cuenta ficticia participante:

```bash
cd ..
git clone https://github.com/participante/git101.git
cd git101
git config user.name "Participante CodeLab"
git config user.email "participante@example.invalid"
git remote -v
git switch -c snippet-participante
cp 2026/snippets/hola.json 2026/snippets/participante.json
```

Sustituye participante por el usuario real y configura el correo elegido para la publicación. Abre el nuevo JSON con el editor. Cambia slug a participante, author, title, language, code y description. El nombre del archivo debe coincidir con slug; usa minúsculas, números y guiones. No edites hola.json: cada asistente añade un archivo propio.

JSON exige comillas dobles; no admite comentarios ni comas finales. Dentro de code, escribe saltos de línea como \n y escapa las comillas con \". Un snippet es texto: la web no ejecuta su código. No añadas secretos, información personal de otras personas ni material sin permiso.

```bash
git status
git diff
git add 2026/snippets/participante.json
git diff --staged
git commit -m "Añade el snippet de participante"
git push -u origin snippet-participante
```

Explica origin: es el nombre local del remoto que clonamos; en esta práctica debe apuntar al fork. -u relaciona la rama local con la rama remota para próximos push y pull.

Al subir por HTTPS, GitHub no acepta la contraseña normal de la cuenta como contraseña de Git. En Windows, Git Credential Manager suele abrir el navegador para autenticar. Haz la comprobación antes del taller. Si falla, ayuda de forma individual; no pidas pegar tokens en la terminal proyectada ni guardar claves en el repositorio.

En GitHub, abre Compare & pull request. Comprueba base: codelabzgz/git101, rama main; origen: el fork y snippet-participante. Revisa Files changed: debe aparecer solo su contribución. El título describe el cambio y la descripción explica qué aporta.

Abre Checks y muestra el resultado de la validación. Si falla, localiza el mensaje, corrige el JSON, haz otro commit y push en la misma rama. El PR se actualiza: no hace falta abrir otro.

Los PR de nuevos colaboradores pueden necesitar aprobación de la organización para ejecutar Actions. Un check verde no significa que una persona haya revisado el cambio. La organización revisa archivo, contenido y permisos antes de fusionar. No ejecutes código no revisado con secretos; mantén la validación con permisos de lectura y no uses pull_request_target para estas contribuciones.

## 6. Web y cierre · 5 minutos

Fusiona un PR de prueba revisado. Explica el recorrido: push a main → validación y pruebas → generación de HTML → despliegue de Pages. El despliegue no es instantáneo; muestra la ejecución de Actions y espera a su estado final antes de actualizar la web.

Se publican solo archivos estáticos, no un servidor Flask. Todos pueden consultar los snippets sin instalar nada. Una tarjeta nueva en la web demuestra el recorrido completo del aporte.

Si el despliegue se retrasa, muestra la web local y deja claro que todavía no es la publicación real. No prometas que todos los PR estarán online antes de salir: la revisión puede continuar después.

Cierra con la encuesta de satisfacción antes de que se vaya la gente. Pregunta qué parte costó más y muestra el enlace al material. Recuerda comprobar la asistencia y las autorizaciones para fotos según la organización del evento.

## Errores frecuentes y respuesta del ponente

| Síntoma | Qué comprobar | Qué hacer |
| --- | --- | --- |
| git no se reconoce | Instalación y terminal abierta antes de instalar | Reabrir Git Bash; comprobar git --version |
| Not a git repository | Carpeta actual | Usar pwd y entrar en la carpeta del repositorio |
| Author identity unknown | user.name y user.email locales | Configurarlos en ese repositorio |
| Nothing to commit | Archivo guardado y cambios preparados | Revisar status y diff; no inventar un cambio |
| Permission denied / 403 al subir | URL de origin y cuenta autenticada | Subir al fork propio; revisar acceso sin exponer credenciales |
| Push rejected | Cambios remotos o rama equivocada | Leer el error; consultar status y el historial. No usar force |
| JSON rojo en Checks | Mensaje de validate.py | Corregir el archivo y volver a hacer commit y push |
| No aparece conflicto | Ramas sin cambios divergentes en la misma línea | Repetir el bloque 4 en un repositorio de ensayo |
| Web sin la tarjeta nueva | PR fusionado y despliegue finalizado | Revisar Actions y recargar después de que termine |

## Si falla Internet o falta tiempo

Sin Internet, completa historial, ramas y conflicto: Git funciona localmente. Explica el PR con una captura o demostración preparada y entrega instrucciones para terminarlo después. No marques ese PR como realizado si no se abrió.

Con retraso, demuestra ramas en cinco minutos y guía un único conflicto. Mantén el ejercicio del aporte individual. Con poca experiencia previa, permite trabajar por parejas y usar el ejemplo de código.

## Referencias para quien imparte

Git merge: https://git-scm.com/docs/git-merge

Autenticación en GitHub: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/about-authentication-to-github

Pruebas de Flask: https://flask.palletsprojects.com/en/stable/testing/

Exportación estática: https://frozen-flask.readthedocs.io/en/latest/
