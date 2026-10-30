"""Validate notebook documents/IPython syntax without executing any cells."""
import ast
import json
from pathlib import Path
import nbformat
from IPython.core.inputtransformer2 import TransformerManager

root = Path(__file__).resolve().parents[1]
paths = sorted((root / "notebooks").rglob("*.ipynb"))
if not paths:
    raise RuntimeError("No notebook inputs found; a sparse checkout must include notebook source")
transformer = TransformerManager()
code_cells = 0
non_python = []
retired = 0
for path in paths:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    nbformat.validate(notebook)
    if "deprecated" in path.relative_to(root).parts:
        retired += 1
        continue
    metadata = notebook.get("metadata", {})
    language = metadata.get("language_info", {}).get("name") or metadata.get("kernelspec", {}).get("language") or metadata.get("kernelspec", {}).get("name", "unknown")
    if "python" not in language.lower():
        non_python.append((str(path.relative_to(root)), language))
        continue
    for index, cell in enumerate(notebook["cells"]):
        if cell["cell_type"] == "code":
            text = cell["source"]
            text = "".join(text) if isinstance(text, list) else text
            transformed = transformer.transform_cell(text)
            ast.parse(transformed, filename=f"{path.relative_to(root)}:cell{index}")
            code_cells += 1
print(f"Validated {len(paths)} notebook schemas and {code_cells} transformed IPython code cells. No cells executed; cloud, model and clinical outcomes remain unverified.")
print("Non-Python notebooks (schema only):", non_python)

print("Deprecated notebooks (schema only, matching upstream standards scope):", retired)
