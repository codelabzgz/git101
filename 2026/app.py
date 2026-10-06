from flask import Flask, render_template, abort
from pathlib import Path
import json
from validate import SLUG, validate_snippets

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
app.config["SNIPPETS_DIR"] = BASE_DIR / "snippets"

def load_snippets():
  snips_dir = Path(app.config["SNIPPETS_DIR"])
  errors = validate_snippets(snips_dir)
  if errors:
    raise ValueError("\n".join(errors))
  snippets = []
  for file in sorted(snips_dir.glob("*.json")):
    snippets.append(json.loads(file.read_text(encoding="utf-8-sig")))
  return snippets


@app.route("/")
def index():
  snippets = load_snippets()
  return render_template("index.html", snippets=snippets)

@app.route("/snippet/<slug>.html")
def snippet(slug):
    if not SLUG.fullmatch(slug):
        abort(404)
    path = Path(app.config["SNIPPETS_DIR"]) / f"{slug}.json"
    if not path.is_file():
        abort(404)
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return render_template("snippet.html", snippet=data)

if __name__ == "__main__":
  app.run(host="127.0.0.1", port=5000)
