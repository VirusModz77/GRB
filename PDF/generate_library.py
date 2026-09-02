#!/usr/bin/env python3
"""
Genera library.json para el visor de biblioteca (index.html).

Estructura esperada:

    mi_carpeta/
        index.html
        generate_library.py
        library.json        <- lo escribe este script
        pdfs/
            informe.pdf
            manual.pdf

El visor lee library.json SIEMPRE desde la carpeta donde está index.html,
así que el archivo se escribe ahí (no dentro de pdfs/), y cada entrada
lleva la ruta relativa completa, incluida la carpeta:

    { "documents": ["pdfs/informe.pdf", "pdfs/manual.pdf"] }

Uso:
    python3 generate_library.py            # usa la carpeta del script
    python3 generate_library.py /ruta/web  # carpeta que contiene index.html

Vuelve a ejecutarlo cada vez que añadas o quites un PDF.
"""

import json
import sys
from pathlib import Path

PDF_DIR_NAME = "pdfs"


def find_root(arg=None):
    """Carpeta que contiene index.html y la subcarpeta pdfs/."""
    if arg:
        root = Path(arg).resolve()
    else:
        # La carpeta del propio script, no el directorio actual: así
        # funciona igual si lo ejecutas con doble clic o desde otra ruta.
        root = Path(__file__).resolve().parent

    if not root.is_dir():
        sys.exit(f"Error: '{root}' no es una carpeta.")

    # Comodidad: si te has metido dentro de pdfs/, subimos un nivel.
    if root.name.lower() == PDF_DIR_NAME and (root.parent / "index.html").is_file():
        root = root.parent

    return root


def main():
    root = find_root(sys.argv[1] if len(sys.argv) > 1 else None)
    pdf_dir = root / PDF_DIR_NAME

    if not pdf_dir.is_dir():
        sys.exit(
            f"Error: no existe la carpeta '{pdf_dir}'.\n"
            f"Crea una subcarpeta llamada '{PDF_DIR_NAME}' junto a index.html "
            f"y pon dentro los PDF."
        )

    # rglob para admitir también subcarpetas dentro de pdfs/.
    # Se ignoran los archivos ocultos y los '._algo.pdf' que deja macOS.
    docs = sorted(
        (p.relative_to(root).as_posix()
         for p in pdf_dir.rglob("*")
         if p.is_file()
         and p.suffix.lower() == ".pdf"
         and not p.name.startswith(".")),
        key=str.lower,
    )

    output_path = root / "library.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"documents": docs}, f, ensure_ascii=False, indent=2)
        f.write("\n")

    if docs:
        print(f"Encontrados {len(docs)} PDF en '{pdf_dir}':")
        for name in docs:
            print(f"  - {name}")
    else:
        print(f"Aviso: no se encontró ningún PDF en '{pdf_dir}'.")

    print(f"\nEscrito: {output_path}")

    if not (root / "index.html").is_file():
        print(
            f"\nAviso: no hay ningún index.html en '{root}'. "
            "library.json debe quedar en la misma carpeta que index.html."
        )


if __name__ == "__main__":
    main()
