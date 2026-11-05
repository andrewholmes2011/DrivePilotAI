import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json

from organizer import scan_folder, apply_moves, undo_moves

class DrivePilotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DrivePilotAI")
        self.root.geometry("1050x680")
        self.root.minsize(800, 520)
        self.folder = ""
        self.items = []
        self.last_journal = []
        self._build()

    def _build(self):
        self.root.configure(bg="#111827")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=28, background="#1f2937",
                        fieldbackground="#1f2937", foreground="#f9fafb")
        style.configure("Treeview.Heading", background="#374151", foreground="white")
        style.configure("TButton", padding=8)
        header = tk.Frame(self.root, bg="#111827")
        header.pack(fill="x", padx=22, pady=(18, 10))
        tk.Label(header, text="DrivePilotAI", fg="#f9fafb", bg="#111827",
                 font=("Segoe UI", 23, "bold")).pack(anchor="w")
        tk.Label(header, text="A free, safety-first Google Drive and file organizer",
                 fg="#9ca3af", bg="#111827", font=("Segoe UI", 10)).pack(anchor="w")

        bar = tk.Frame(self.root, bg="#111827")
        bar.pack(fill="x", padx=22, pady=8)
        ttk.Button(bar, text="Choose local folder", command=self.choose_folder).pack(side="left")
        ttk.Button(bar, text="Scan folder", command=self.scan).pack(side="left", padx=8)
        ttk.Button(bar, text="Connect Google Drive (read-only)", command=self.scan_drive).pack(side="left")
        ttk.Button(bar, text="Preview organization", command=self.preview).pack(side="right")

        self.location = tk.Label(self.root, text="No local folder selected",
                                 bg="#111827", fg="#d1d5db", anchor="w")
        self.location.pack(fill="x", padx=24, pady=5)
        columns = ("name", "category", "size", "modified", "path")
        self.table = ttk.Treeview(self.root, columns=columns, show="headings")
        for col, title, width in [
            ("name", "File", 220), ("category", "Suggested category", 150),
            ("size", "Size (bytes)", 100), ("modified", "Modified", 140),
            ("path", "Current location", 380)
        ]:
            self.table.heading(col, text=title)
            self.table.column(col, width=width, anchor="w")
        self.table.pack(fill="both", expand=True, padx=22, pady=10)

        footer = tk.Frame(self.root, bg="#111827")
        footer.pack(fill="x", padx=22, pady=(0, 18))
        ttk.Button(footer, text="Apply local moves", command=self.apply).pack(side="left")
        ttk.Button(footer, text="Undo last moves", command=self.undo).pack(side="left", padx=8)
        self.status = tk.Label(footer, text="Ready. Scanning does not change your files.",
                               bg="#111827", fg="#9ca3af")
        self.status.pack(side="right")

    def choose_folder(self):
        folder = filedialog.askdirectory(title="Choose a folder to scan")
        if folder:
            self.folder = folder
            self.location.config(text=f"Local folder: {folder}")
            self.status.config(text="Folder selected.")

    def scan(self):
        if not self.folder:
            return messagebox.showinfo("Choose a folder", "Select a local folder first.")
        try:
            self.items = scan_folder(self.folder)
            self.show_items()
            self.status.config(text=f"Found {len(self.items)} files. No changes made.")
        except Exception as exc:
            messagebox.showerror("Scan failed", str(exc))

    def scan_drive(self):
        try:
            from drive_api import connect_and_list
            files = connect_and_list()
            self.items = []
            for f in files:
                self.items.append({
                    "name": f.get("name", "Unnamed"),
                    "category": "Google Drive (read-only)",
                    "size": int(f.get("size", 0) or 0),
                    "modified": f.get("modifiedTime", ""),
                    "path": "Google Drive"
                })
            self.show_items()
            self.status.config(text=f"Loaded {len(files)} Drive items (read-only).")
        except Exception as exc:
            messagebox.showerror("Google Drive connection", str(exc))

    def show_items(self):
        self.table.delete(*self.table.get_children())
        for item in self.items:
            self.table.insert("", "end", values=(
                item["name"], item["category"], item["size"],
                item["modified"], item["path"]
            ))

    def preview(self):
        if not self.items:
            return messagebox.showinfo("Nothing to preview", "Scan a folder first.")
        counts = {}
        for item in self.items:
            counts[item["category"]] = counts.get(item["category"], 0) + 1
        summary = "\n".join(f"{key}: {value}" for key, value in sorted(counts.items()))
        messagebox.showinfo("Organization preview", f"{len(self.items)} items scanned.\n\n{summary}\n\nNo files have been moved.")

    def apply(self):
        if not self.folder or not self.items:
            return messagebox.showinfo("Scan first", "Scan a local folder before applying moves.")
        if any(item["path"] == "Google Drive" for item in self.items):
            return messagebox.showwarning("Read-only Drive scan", "Google Drive changes are not enabled in this first version. Select and scan a local folder to organize local files.")
        if not messagebox.askyesno("Confirm file moves",
                f"Move {len(self.items)} files into category folders inside:\n{self.folder}\n\nNo files will be deleted. Continue?"):
            return
        try:
            self.last_journal = apply_moves(self.items, self.folder)
            Path("undo_log.json").write_text(json.dumps(self.last_journal, indent=2), encoding="utf-8")
            self.items = scan_folder(self.folder)
            self.show_items()
            self.status.config(text=f"Moved {len(self.last_journal)} files.")
        except Exception as exc:
            messagebox.showerror("Move failed", str(exc))

    def undo(self):
        if not self.last_journal:
            log = Path("undo_log.json")
            if log.exists():
                self.last_journal = json.loads(log.read_text(encoding="utf-8"))
        if not self.last_journal:
            return messagebox.showinfo("Nothing to undo", "No saved move history was found.")
        if not messagebox.askyesno("Undo moves", "Restore files to their original locations?"):
            return
        restored = undo_moves(self.last_journal)
        self.last_journal = []
        Path("undo_log.json").unlink(missing_ok=True)
        if self.folder:
            self.items = scan_folder(self.folder)
            self.show_items()
        self.status.config(text=f"Restored {restored} files.")

if __name__ == "__main__":
    root = tk.Tk()
    DrivePilotApp(root)
    root.mainloop()
