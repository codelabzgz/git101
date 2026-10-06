from app import app, load_snippets, BASE_DIR
from flask_frozen import Freezer
from pathlib import Path

app.config['FREEZER_RELATIVE_URLS'] = True
app.config['FREEZER_DESTINATION'] = str(BASE_DIR / 'build')
app.config['FREEZER_REMOVE_EXTRA_FILES'] = True
freezer = Freezer(app)

# Snippet pages
@freezer.register_generator
def snippet():
    snippets = load_snippets()
    for s in snippets:
        if 'slug' in s and s['slug']:
            yield {'slug': s['slug']}

# Static files
@freezer.register_generator
def static_files():
    static_folder = Path(app.static_folder)
    for filepath in static_folder.rglob('*'):
        if filepath.is_file():
            rel_path = filepath.relative_to(static_folder)
            yield f'/static/{rel_path.as_posix()}'

def build_site(destination=None):
    load_snippets()
    if destination is not None:
        app.config['FREEZER_DESTINATION'] = str(destination)
    freezer.freeze()


if __name__ == "__main__":
    build_site()
    print(f"Web generada en {app.config['FREEZER_DESTINATION']}")
