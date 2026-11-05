from pathlib import Path
from datetime import datetime
import hashlib

CATEGORIES = {
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "Presentations": {".ppt", ".pptx", ".odp"},
    "Images": {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg"},
    "Videos": {".mp4", ".mov", ".avi", ".mkv", ".webm"},
    "Audio": {".mp3", ".wav", ".m4a", ".flac", ".ogg"},
    "Archives": {".zip", ".7z", ".rar", ".tar", ".gz"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".json"}
}

def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Other"

def scan_folder(folder: str):
    root = Path(folder).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("Choose an existing folder.")
    results = []
    for item in root.rglob("*"):
        if not item.is_file():
            continue
        try:
            stat = item.stat()
            results.append({
                "name": item.name,
                "path": str(item),
                "category": category_for(item),
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
            })
        except (PermissionError, OSError):
            continue
    return results

def apply_moves(items, root: str):
    """Move files into category folders and return an undo journal."""
    from shutil import move
    base = Path(root).resolve()
    journal = []
    for item in items:
        source = Path(item["path"]).resolve()
        if not source.exists() or base not in source.parents:
            continue
        destination_dir = base / item["category"]
        destination_dir.mkdir(exist_ok=True)
        destination = destination_dir / source.name
        if destination.exists():
            stem, suffix, n = source.stem, source.suffix, 1
            while (destination_dir / f"{stem} ({n}){suffix}").exists():
                n += 1
            destination = destination_dir / f"{stem} ({n}){suffix}"
        move(str(source), str(destination))
        journal.append({"from": str(source), "to": str(destination)})
    return journal

def undo_moves(journal):
    from shutil import move
    restored = 0
    for entry in reversed(journal):
        source, destination = Path(entry["to"]), Path(entry["from"])
        if source.exists() and not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            move(str(source), str(destination))
            restored += 1
    return restored
