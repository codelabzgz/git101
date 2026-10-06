"""Validate contributions without executing participants' code."""
import json
import re
import sys
from pathlib import Path

CAMPOS = {"slug", "author", "title", "language", "code", "description"}
SNIPS = Path(__file__).resolve().parent / "snippets"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
MAX_BYTES = 32_768

def validate_snippets(directory=SNIPS):
    errores = []
    files = sorted(Path(directory).glob("*.json"))
    if not files:
        return ["No hay snippets JSON en la carpeta indicada."]
    for f in files:
        if f.stat().st_size > MAX_BYTES:
            errores.append(f"{f.name}: supera el límite de 32 KiB.")
            continue
        try:
            data = json.loads(f.read_text(encoding="utf-8-sig"))
        except (ValueError, UnicodeError, OSError) as e:
            errores.append(f"{f.name}: JSON invalido ({e})")
            continue
        if not isinstance(data, dict):
            errores.append(f"{f.name}: el JSON debe ser un objeto, no una lista o valor.")
            continue
        faltan = CAMPOS - data.keys()
        if faltan:
            errores.append(f"{f.name}: faltan campos {sorted(faltan)}")
        vacios = [k for k in CAMPOS & data.keys() if not isinstance(data[k], str) or not data[k].strip()]
        if vacios:
            errores.append(f"{f.name}: campos que deben ser texto no vacío {sorted(vacios)}")
        slug = data.get("slug", "")
        if not isinstance(slug, str) or not SLUG.fullmatch(slug):
            errores.append(f"{f.name}: slug inválido; usa minúsculas, números y guiones.")
        elif slug != f.stem:
            errores.append(f"{f.name}: el slug '{slug}' no coincide con el nombre del fichero '{f.stem}'")
    return errores


def main() -> int:
    errores = validate_snippets()
    if errores:
        print("Snippets con problemas:")
        for e in errores:
            print(" -", e)
        return 1
    print(f"OK: {len(list(SNIPS.glob('*.json')))} snippets válidos")
    return 0

if __name__ == "__main__":
    sys.exit(main())
