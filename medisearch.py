import csv
import json
import random
import webbrowser
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# ── Optional AI (prescription scan) ──────────────────────────────────────────
AI_AVAILABLE = False
try:
    from google import genai as _genai
    import PIL.Image as _PILImage

    try:
        import config as _cfg
        _api_key = _cfg.GEMINI_API_KEY
    except (ImportError, AttributeError):
        _api_key = "MISSING_KEY"

    _ai_client = _genai.Client(api_key=_api_key)
    AI_AVAILABLE = True
except Exception:
    pass

# ── Default CSV path (auto-loaded on start) ───────────────────────────────────
DEFAULT_CSV = "C:/Users/ASUS/Desktop/New folder (8)/medicine_data.csv/medicine_data.csv"

# ── Themes ────────────────────────────────────────────────────────────────────
THEMES = {
    "Midnight Teal": {
        "BG": "#0d1117", "BG_LIGHT": "#161b22",
        "PANEL": "#1c2128", "PANEL_LIGHT": "#262d34",
        "BORDER": "#373e47",
        "ACCENT": "#00d9ff", "ACCENT_DARK": "#00b8d4",
        "A_COMP": "#3b82f6", "A_DESC": "#818cf8",
        "A_SIDE": "#f59e0b", "A_INTER": "#ef4444",
        "SUCCESS": "#22d3a5", "WARNING": "#f59e0b", "DANGER": "#ff6b6b",
        "TEXT": "#e6edf3", "TEXT_MUTED": "#8b949e",
        "TAG_BG": "#21262d",
        "ROW_EVEN": "#0d1117", "ROW_ODD": "#161b22",
        "ROW_SEL": "#1f6feb",
        "HEADER_BG": "#0d1117", "STATUS_BG": "#010409",
        "CARD_BG": "#1c2128",
    },
    "Ocean Deep": {
        "BG": "#0a0e27", "BG_LIGHT": "#10162d",
        "PANEL": "#141b3a", "PANEL_LIGHT": "#1a2347",
        "BORDER": "#2d3b5f",
        "ACCENT": "#00d4ff", "ACCENT_DARK": "#00a3cc",
        "A_COMP": "#60a5fa", "A_DESC": "#a78bfa",
        "A_SIDE": "#fbbf24", "A_INTER": "#f87171",
        "SUCCESS": "#10b981", "WARNING": "#f59e0b", "DANGER": "#ef4444",
        "TEXT": "#f0f4f8", "TEXT_MUTED": "#94a3b8",
        "TAG_BG": "#1e293b",
        "ROW_EVEN": "#141b3a", "ROW_ODD": "#0f1429",
        "ROW_SEL": "#1e3a5f",
        "HEADER_BG": "#0d1230", "STATUS_BG": "#070a1a",
        "CARD_BG": "#1a2347",
    },
    "Forest Mist": {
        "BG": "#0a1810", "BG_LIGHT": "#0e1f18",
        "PANEL": "#112820", "PANEL_LIGHT": "#163328",
        "BORDER": "#2d5a42",
        "ACCENT": "#34d399", "ACCENT_DARK": "#10b981",
        "A_COMP": "#34d399", "A_DESC": "#a3e635",
        "A_SIDE": "#fbbf24", "A_INTER": "#f87171",
        "SUCCESS": "#10b981", "WARNING": "#f59e0b", "DANGER": "#ef4444",
        "TEXT": "#ecfdf5", "TEXT_MUTED": "#86a896",
        "TAG_BG": "#1a3d2f",
        "ROW_EVEN": "#112820", "ROW_ODD": "#0c1e16",
        "ROW_SEL": "#1e4a3a",
        "HEADER_BG": "#0c1f18", "STATUS_BG": "#060f0c",
        "CARD_BG": "#163328",
    },
    "Sunset Glow": {
        "BG": "#1a0f0a", "BG_LIGHT": "#241610",
        "PANEL": "#2d1a10", "PANEL_LIGHT": "#3d2418",
        "BORDER": "#5c3a26",
        "ACCENT": "#ff7b54", "ACCENT_DARK": "#e65a35",
        "A_COMP": "#fb923c", "A_DESC": "#c084fc",
        "A_SIDE": "#fbbf24", "A_INTER": "#f87171",
        "SUCCESS": "#10b981", "WARNING": "#f59e0b", "DANGER": "#ef4444",
        "TEXT": "#fef3e2", "TEXT_MUTED": "#c4a080",
        "TAG_BG": "#3d2418",
        "ROW_EVEN": "#2d1a10", "ROW_ODD": "#22130c",
        "ROW_SEL": "#4d3020",
        "HEADER_BG": "#22130c", "STATUS_BG": "#120a06",
        "CARD_BG": "#3d2418",
    },
    "Royal Purple": {
        "BG": "#120a1e", "BG_LIGHT": "#1a1029",
        "PANEL": "#1f1635", "PANEL_LIGHT": "#2a1f42",
        "BORDER": "#4c3d6b",
        "ACCENT": "#a78bfa", "ACCENT_DARK": "#8b5cf6",
        "A_COMP": "#818cf8", "A_DESC": "#ec4899",
        "A_SIDE": "#fbbf24", "A_INTER": "#f87171",
        "SUCCESS": "#10b981", "WARNING": "#f59e0b", "DANGER": "#ef4444",
        "TEXT": "#f5f3ff", "TEXT_MUTED": "#c4b5fd",
        "TAG_BG": "#2a1f42",
        "ROW_EVEN": "#1f1635", "ROW_ODD": "#170f27",
        "ROW_SEL": "#3d2d5f",
        "HEADER_BG": "#170f27", "STATUS_BG": "#0d0616",
        "CARD_BG": "#2a1f42",
    },
    "Midnight Steel": {
        "BG": "#0f1419", "BG_LIGHT": "#161b22",
        "PANEL": "#1c2128", "PANEL_LIGHT": "#22272e",
        "BORDER": "#373e47",
        "ACCENT": "#58a6ff", "ACCENT_DARK": "#1f6feb",
        "A_COMP": "#58a6ff", "A_DESC": "#c084fc",
        "A_SIDE": "#d29922", "A_INTER": "#f85149",
        "SUCCESS": "#3fb950", "WARNING": "#d29922", "DANGER": "#f85149",
        "TEXT": "#e6edf3", "TEXT_MUTED": "#8b949e",
        "TAG_BG": "#21262d",
        "ROW_EVEN": "#1c2128", "ROW_ODD": "#161b22",
        "ROW_SEL": "#1c3050",
        "HEADER_BG": "#161b22", "STATUS_BG": "#0d1117",
        "CARD_BG": "#22272e",
    },
}

# ── Fonts ──────────────────────────────────────────────────────────────────────
FONT_TITLE   = ("Segoe UI", 26, "bold")
FONT_HEADING = ("Segoe UI", 15, "bold")
FONT_LABEL   = ("Segoe UI", 11)
FONT_BOLD    = ("Segoe UI", 11, "bold")
FONT_SMALL   = ("Segoe UI", 10)
FONT_TINY    = ("Segoe UI", 8)
FONT_MONO    = ("Consolas", 10)
FONT_STAT    = ("Segoe UI", 22, "bold")

# ── Shops ──────────────────────────────────────────────────────────────────────
SHOPS = [
    {"name": "Choudhary Medicals",
     "url": "https://www.google.com/maps/place/Indore+-+Bhopal+Rd,+Kothri,+Madhya+Pradesh+466114/@23.0851306,76.8084776,13z"},
    {"name": "Dwivedi Medicals",
     "url": "https://www.google.com/maps/place/23%C2%B004'13.7%22N+76%C2%B050'52.0%22E/@23.0851306,76.8084776,13z"},
    {"name": "Mathur Medicals",
     "url": "https://www.google.com/maps/place/23%C2%B004'42.8%22N+76%C2%B051'51.6%22E/@23.0851306,76.8084776,13z"},
    {"name": "Goyal Medicose",
     "url": "https://www.google.com/maps/place/23%C2%B006'52.4%22N+76%C2%B051'22.9%22E/@23.0851306,76.8084776,13z"},
    {"name": "Agrawal Medicos",
     "url": "https://www.google.com/maps/place/23.076012,76.810279/@23.0851306,76.8084776,13z"},
    {"name": "Raskar Medicose",
     "url": "https://www.google.com/maps/place/23.030015,76.836254/@23.0908513,76.6987173,11.88z"},
]

# ── Data helpers ───────────────────────────────────────────────────────────────

def load_data(file_path: str):
    try:
        rows = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rows.append(row)
        return rows
    except Exception:
        return None


def remove_duplicates(data: list) -> list:
    seen, unique = set(), []
    for row in data:
        key = row.get("product_name", "").lower()
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique


def search_medicine(data: list, query: str, max_results: int) -> list:
    q = query.lower()
    results = []
    for row in data:
        if (q in row.get("product_name", "").lower() or
                q in row.get("salt_composition", "").lower()):
            results.append(row)
            if len(results) >= max_results:
                break
    return results


def parse_interactions(raw: str) -> str:
    """Turn raw JSON-like drug_interactions into human-readable text."""
    if not raw or raw.strip() in ("", "—", "N/A"):
        return ""
    raw = raw.strip()
    try:
        data = json.loads(raw)
        if isinstance(data, list) and data:
            lines = []
            for item in data:
                if not isinstance(item, dict):
                    continue
                drug   = item.get("drug",   item.get("name",     ""))
                bound  = item.get("bound",  item.get("severity", ""))
                effect = item.get("dffct",  item.get("effect",   ""))
                for field in (drug, bound, effect):
                    if isinstance(field, list):
                        field = ", ".join(str(x) for x in field if x)
                parts = [str(x).strip() for x in (drug, effect) if x and str(x).strip()]
                if parts:
                    line = " — ".join(parts)
                    if bound:
                        line += f"  [{bound}]"
                    lines.append(f"• {line}")
            return "\n".join(lines) if lines else raw
    except Exception:
        pass
    # Not JSON — return as-is but clean brackets
    cleaned = raw.strip("[]").replace("{", "").replace("}", "")
    return cleaned if cleaned else raw


# ── Main Application ───────────────────────────────────────────────────────────

class MedicineApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚕ MediSearch Pro — Medicine Discovery Platform")
        self.state("zoomed")

        self._theme_name = "Midnight Teal"
        self._t = THEMES[self._theme_name]
        self.configure(bg=self._t["BG"])

        # ── State ──
        self.data: list          = []
        self._results: list      = []
        self._shop_map: dict     = {}
        self._search_job         = None
        self._loaded_path: str   = ""

        # ── Vars ──
        self.file_path_var = tk.StringVar(value="No file loaded")
        self.query_var     = tk.StringVar()
        self.max_var       = tk.StringVar(value="20")
        self.status_var    = tk.StringVar(value="Loading database…")

        self.query_var.trace_add("write", self._on_query_change)

        self._build_styles()
        self._build_ui()

        # Auto-load default CSV
        self.after(200, self._auto_load_default)

    # ── Shorthand ─────────────────────────────────────────────────────────────
    def _c(self, key: str) -> str:
        return self._t[key]

    # ── Styles ────────────────────────────────────────────────────────────────
    def _build_styles(self):
        t = self._t
        s = ttk.Style(self)
        s.theme_use("clam")

        s.configure(".", background=t["BG"], foreground=t["TEXT"],
                     font=FONT_LABEL, borderwidth=0, relief="flat")
        s.configure("TFrame",       background=t["BG"])
        s.configure("Panel.TFrame", background=t["PANEL"])

        s.configure("TLabel",        background=t["BG"],    foreground=t["TEXT"])
        s.configure("Muted.TLabel",  background=t["BG"],    foreground=t["TEXT_MUTED"], font=FONT_SMALL)
        s.configure("Panel.TLabel",  background=t["PANEL"], foreground=t["TEXT"])
        s.configure("Card.TLabel",   background=t["CARD_BG"], foreground=t["TEXT"])

        s.configure("Modern.TEntry",
                     fieldbackground=t["PANEL"], foreground=t["TEXT"],
                     insertcolor=t["ACCENT"], borderwidth=2,
                     relief="flat", padding=(14, 12))
        s.map("Modern.TEntry",
              fieldbackground=[("focus", t["PANEL_LIGHT"])],
              lightcolor=[("focus", t["ACCENT"])],
              darkcolor=[("focus", t["ACCENT"])])

        s.configure("Primary.TButton", background=t["ACCENT"], foreground=t["BG"],
                     font=FONT_BOLD, padding=(24, 12), borderwidth=0)
        s.map("Primary.TButton",
              background=[("active", t["ACCENT_DARK"]), ("pressed", t["ACCENT_DARK"])])

        s.configure("Secondary.TButton", background=t["PANEL_LIGHT"], foreground=t["TEXT"],
                     font=FONT_LABEL, padding=(18, 12), borderwidth=0)
        s.map("Secondary.TButton", background=[("active", t["BORDER"])])

        s.configure("Ghost.TButton", background=t["PANEL"], foreground=t["TEXT_MUTED"],
                     font=FONT_SMALL, padding=(12, 10), borderwidth=1)
        s.map("Ghost.TButton",
              background=[("active", t["PANEL_LIGHT"])],
              foreground=[("active", t["TEXT"])])

        s.configure("Icon.TButton", background=t["PANEL"], foreground=t["ACCENT"],
                     font=("Segoe UI", 15), padding=(12, 10), borderwidth=0)
        s.map("Icon.TButton", background=[("active", t["PANEL_LIGHT"])])

        s.configure("Treeview",
                     background=t["ROW_EVEN"], fieldbackground=t["ROW_EVEN"],
                     foreground=t["TEXT"], font=FONT_LABEL,
                     rowheight=48, borderwidth=0)
        s.configure("Treeview.Heading",
                     background=t["HEADER_BG"], foreground=t["ACCENT"],
                     font=FONT_BOLD, relief="flat", padding=(12, 10))
        s.map("Treeview",
              background=[("selected", t["ROW_SEL"])],
              foreground=[("selected", t["TEXT"])])
        s.map("Treeview.Heading",
              background=[("active", t["BORDER"])])

        s.configure("Vertical.TScrollbar",
                     background=t["BORDER"], troughcolor=t["BG"],
                     arrowcolor=t["TEXT_MUTED"], borderwidth=0, width=14)
        s.configure("Horizontal.TScrollbar",
                     background=t["BORDER"], troughcolor=t["BG"],
                     arrowcolor=t["TEXT_MUTED"], borderwidth=0, height=14)

        s.configure("TCombobox",
                     fieldbackground=t["PANEL"], background=t["PANEL"],
                     foreground=t["TEXT"], arrowcolor=t["ACCENT"],
                     borderwidth=1, relief="flat", padding=(6, 6))
        s.map("TCombobox",
              fieldbackground=[("readonly", t["PANEL"])],
              selectbackground=[("readonly", t["PANEL"])],
              selectforeground=[("readonly", t["TEXT"])])

        s.configure("TSpinbox",
                     fieldbackground=t["PANEL"], background=t["PANEL"],
                     foreground=t["TEXT"], arrowcolor=t["ACCENT"],
                     borderwidth=1, relief="flat", padding=(6, 6))

    # ── UI Build ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        t = self._t

        # ── HEADER ──
        hdr = tk.Frame(self, bg=t["PANEL"], height=78)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)

        # Logo + title
        logo_f = tk.Frame(hdr, bg=t["PANEL"])
        logo_f.pack(side="left", padx=28, pady=14)

        tk.Label(logo_f, text="⚕", bg=t["PANEL"], fg=t["ACCENT"],
                 font=("Segoe UI Emoji", 32)).pack(side="left", padx=(0, 12))

        title_f = tk.Frame(logo_f, bg=t["PANEL"])
        title_f.pack(side="left")
        tk.Label(title_f, text="MediSearch Pro",
                 bg=t["PANEL"], fg=t["TEXT"], font=FONT_TITLE).pack(anchor="w")
        tk.Label(title_f, text="Medicine Discovery & Analysis Platform",
                 bg=t["PANEL"], fg=t["TEXT_MUTED"], font=FONT_SMALL).pack(anchor="w")

        # Right controls (theme + DB count)
        right_f = tk.Frame(hdr, bg=t["PANEL"])
        right_f.pack(side="right", padx=28, pady=14)

        # DB stat
        db_box = tk.Frame(right_f, bg=t["CARD_BG"], padx=18, pady=10)
        db_box.pack(side="left", padx=(0, 18))
        tk.Label(db_box, text="MEDICINES",
                 bg=t["CARD_BG"], fg=t["TEXT_MUTED"], font=FONT_TINY).pack()
        self._db_count = tk.Label(db_box, text="0",
                                  bg=t["CARD_BG"], fg=t["ACCENT"], font=FONT_STAT)
        self._db_count.pack()

        # Theme
        theme_box = tk.Frame(right_f, bg=t["CARD_BG"], padx=14, pady=8)
        theme_box.pack(side="left", padx=(0, 18))
        tk.Label(theme_box, text="🎨 THEME",
                 bg=t["CARD_BG"], fg=t["TEXT_MUTED"], font=FONT_TINY).pack()
        self.theme_combo = ttk.Combobox(theme_box, values=list(THEMES.keys()),
                                        state="readonly", width=14, font=FONT_SMALL)
        self.theme_combo.set(self._theme_name)
        self.theme_combo.bind("<<ComboboxSelected>>", self._change_theme)
        self.theme_combo.pack(pady=(4, 0))

        # Version pill
        tk.Label(right_f, text=" v4.0 ", bg=t["ACCENT"], fg=t["BG"],
                 font=("Segoe UI", 9, "bold"), padx=10, pady=5).pack(side="left")

        # Accent separator
        tk.Frame(self, bg=t["ACCENT"], height=3).pack(fill="x")

        # ── TOOLBAR ──
        toolbar = tk.Frame(self, bg=t["BG"], pady=18, padx=28)
        toolbar.pack(fill="x")

        # Row 1: file + search
        row1 = tk.Frame(toolbar, bg=t["BG"])
        row1.pack(fill="x")

        # File picker
        file_f = tk.Frame(row1, bg=t["BG"])
        file_f.pack(side="left", padx=(0, 24))
        tk.Label(file_f, text="📁 DATABASE",
                 bg=t["BG"], fg=t["TEXT_MUTED"], font=FONT_TINY).pack(anchor="w")
        file_row = tk.Frame(file_f, bg=t["PANEL"])
        file_row.pack(fill="x", pady=(4, 0))
        self._file_lbl = tk.Label(file_row, textvariable=self.file_path_var,
                                   bg=t["PANEL"], fg=t["TEXT_MUTED"],
                                   font=FONT_MONO, padx=12, pady=10,
                                   width=30, anchor="w")
        self._file_lbl.pack(side="left")
        ttk.Button(file_row, text="Browse",
                   style="Ghost.TButton",
                   command=self._browse_file).pack(side="left", padx=4)

        # Divider
        tk.Frame(row1, bg=t["BORDER"], width=3).pack(side="left", fill="y", padx=20)

        # Search field
        search_f = tk.Frame(row1, bg=t["BG"])
        search_f.pack(side="left", expand=True, fill="x", padx=(0, 16))
        tk.Label(search_f, text="🔍 SEARCH  (real-time)",
                 bg=t["BG"], fg=t["TEXT_MUTED"], font=FONT_TINY).pack(anchor="w")
        search_row = tk.Frame(search_f, bg=t["BG"])
        search_row.pack(fill="x", pady=(4, 0))
        self._search_entry = ttk.Entry(search_row,
                                       textvariable=self.query_var,
                                       style="Modern.TEntry",
                                       font=("Segoe UI", 13))
        self._search_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self._search_entry.bind("<Return>", lambda e: self._do_search())

        # AI scan button
        scan_text = "📸 Scan" if AI_AVAILABLE else "📸 (AI)"
        self._scan_btn = ttk.Button(search_row, text=scan_text,
                                    style="Icon.TButton",
                                    command=self._scan_prescription)
        self._scan_btn.pack(side="left", padx=(0, 8))
        if not AI_AVAILABLE:
            self._scan_btn.state(["disabled"])

        ttk.Button(search_row, text="⚡ Search",
                   style="Primary.TButton",
                   command=self._do_search).pack(side="left", padx=(0, 8))
        ttk.Button(search_row, text="✕ Clear",
                   style="Secondary.TButton",
                   command=self._clear).pack(side="left")

        # Row 2: max results + result badge
        row2 = tk.Frame(toolbar, bg=t["BG"])
        row2.pack(fill="x", pady=(12, 0))
        tk.Label(row2, text="Max results:",
                 bg=t["BG"], fg=t["TEXT_MUTED"], font=FONT_SMALL).pack(side="left")
        ttk.Spinbox(row2, textvariable=self.max_var,
                    from_=1, to=500, width=8, font=FONT_LABEL).pack(side="left", padx=(6, 0))

        # Result count
        self._count_box = tk.Frame(row2, bg=t["CARD_BG"], padx=16, pady=8)
        self._count_box.pack(side="right")
        tk.Label(self._count_box, text="RESULTS", bg=t["CARD_BG"],
                 fg=t["TEXT_MUTED"], font=FONT_TINY).pack(side="left", padx=(0, 8))
        self._count_lbl = tk.Label(self._count_box, text="0",
                                   bg=t["CARD_BG"], fg=t["ACCENT"], font=FONT_STAT)
        self._count_lbl.pack(side="left")

        # ── BODY ──
        tk.Frame(self, bg=t["BORDER"], height=2).pack(fill="x")
        body = tk.Frame(self, bg=t["BG"])
        body.pack(fill="both", expand=True)

        # Left – results table
        left = tk.Frame(body, bg=t["BG"])
        left.pack(side="left", fill="both", expand=True, padx=(28, 0), pady=20)

        tk.Label(left, text="📋  SEARCH RESULTS",
                 bg=t["BG"], fg=t["TEXT"], font=FONT_HEADING).pack(anchor="w", pady=(0, 12))

        tree_wrap = tk.Frame(left, bg=t["BG"])
        tree_wrap.pack(fill="both", expand=True)
        tree_wrap.rowconfigure(0, weight=1)
        tree_wrap.columnconfigure(0, weight=1)

        cols = ("name", "composition", "price", "manufacturer")
        self.tree = ttk.Treeview(tree_wrap, columns=cols,
                                  show="headings", selectmode="browse")
        self.tree.heading("name",         text="💊  Medicine Name")
        self.tree.heading("composition",  text="⚗  Composition")
        self.tree.heading("price",        text="💰  Price")
        self.tree.heading("manufacturer", text="🏭  Manufacturer")
        self.tree.column("name",         width=240, anchor="w", stretch=True)
        self.tree.column("composition",  width=260, anchor="w", stretch=True)
        self.tree.column("price",        width=100, anchor="center", stretch=False)
        self.tree.column("manufacturer", width=180, anchor="w", stretch=True)
        self.tree.tag_configure("odd",  background=t["ROW_ODD"])
        self.tree.tag_configure("even", background=t["ROW_EVEN"])
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        vsb = ttk.Scrollbar(tree_wrap, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_wrap, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # ── Right – detail panel ──
        tk.Frame(body, bg=t["BORDER"], width=3).pack(side="left", fill="y")

        self._right = tk.Frame(body, bg=t["PANEL"], width=500)
        self._right.pack(side="left", fill="both", expand=False, padx=(0, 0), pady=0)
        self._right.pack_propagate(False)
        self._build_detail_panel()

        # ── STATUS BAR ──
        tk.Frame(self, bg=t["BORDER"], height=2).pack(fill="x")
        sb = tk.Frame(self, bg=t["STATUS_BG"], height=36)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)

        self._status_dot = tk.Label(sb, text="●", bg=t["STATUS_BG"],
                                     fg=t["SUCCESS"], font=("Segoe UI", 14))
        self._status_dot.pack(side="left", padx=(24, 8), pady=8)
        tk.Label(sb, textvariable=self.status_var,
                 bg=t["STATUS_BG"], fg=t["TEXT"], font=FONT_SMALL).pack(side="left")

    # ── Detail panel ──────────────────────────────────────────────────────────
    def _build_detail_panel(self):
        t = self._t
        parent = self._right

        # Header
        hdr = tk.Frame(parent, bg=t["PANEL"], pady=18, padx=20)
        hdr.pack(fill="x")
        tk.Label(hdr, text="📄  MEDICINE DETAILS",
                 bg=t["PANEL"], fg=t["ACCENT"], font=FONT_HEADING).pack(anchor="w")
        tk.Frame(parent, bg=t["BORDER"], height=2).pack(fill="x")

        # Scrollable canvas
        self._detail_canvas = tk.Canvas(parent, bg=t["PANEL"],
                                         highlightthickness=0, bd=0)
        sb2 = ttk.Scrollbar(parent, orient="vertical",
                             command=self._detail_canvas.yview)
        self._detail_canvas.configure(yscrollcommand=sb2.set)
        sb2.pack(side="right", fill="y")
        self._detail_canvas.pack(side="left", fill="both", expand=True)

        self._detail_inner = tk.Frame(self._detail_canvas, bg=t["PANEL"])
        self._cwin = self._detail_canvas.create_window(
            (0, 0), window=self._detail_inner, anchor="nw")

        def _on_frame_change(e):
            self._detail_canvas.configure(
                scrollregion=self._detail_canvas.bbox("all"))
        def _on_canvas_resize(e):
            self._detail_canvas.itemconfig(self._cwin, width=e.width)

        self._detail_inner.bind("<Configure>", _on_frame_change)
        self._detail_canvas.bind("<Configure>", _on_canvas_resize)
        self._detail_canvas.bind_all(
            "<MouseWheel>",
            lambda e: self._detail_canvas.yview_scroll(
                int(-1 * (e.delta / 120)), "units"))

        self._show_empty_detail()

    def _show_empty_detail(self):
        t = self._t
        for w in self._detail_inner.winfo_children():
            w.destroy()
        f = tk.Frame(self._detail_inner, bg=t["PANEL"])
        f.pack(fill="both", expand=True, pady=100)
        tk.Label(f, text="💊", bg=t["PANEL"], fg=t["TEXT_MUTED"],
                 font=("Segoe UI Emoji", 52)).pack(pady=(0, 16))
        tk.Label(f, text="Select a result\nto view details",
                 bg=t["PANEL"], fg=t["TEXT_MUTED"],
                 font=("Segoe UI", 13), justify="center").pack()

    def _show_detail(self, med: dict, shop: dict | None = None):
        t = self._t
        for w in self._detail_inner.winfo_children():
            w.destroy()

        pad = {"pady": (0, 10)}

        # ── Name card ──
        name_card = tk.Frame(self._detail_inner, bg=t["CARD_BG"], padx=18, pady=18)
        name_card.pack(fill="x", padx=14, pady=(16, 10))

        tk.Label(name_card, text=med.get("product_name", "—"),
                 bg=t["CARD_BG"], fg=t["ACCENT"],
                 font=("Segoe UI", 15, "bold"),
                 wraplength=440, justify="left").pack(anchor="w", pady=(0, 10))

        # Price + Manufacturer row
        meta_row = tk.Frame(name_card, bg=t["CARD_BG"])
        meta_row.pack(anchor="w")

        price = (med.get("product_price") or "").strip()
        if price:
            price_f = tk.Frame(meta_row, bg=t["SUCCESS"], padx=12, pady=5)
            price_f.pack(side="left", padx=(0, 10))
            tk.Label(price_f, text=f"₹ {price}", bg=t["SUCCESS"],
                     fg="#080808", font=("Segoe UI", 10, "bold")).pack()

        mfr = (med.get("product_manufactured") or "").strip()
        if mfr:
            tk.Label(meta_row, text=f"🏭 {mfr}",
                     bg=t["CARD_BG"], fg=t["TEXT_MUTED"],
                     font=FONT_SMALL, wraplength=320).pack(side="left")

        # ── Info blocks (colored accent per section) ──
        sections = [
            ("⚗", "COMPOSITION",       "A_COMP",  med.get("salt_composition", "")),
            ("📝", "DESCRIPTION",      "A_DESC",  med.get("medicine_desc", "")),
            ("⚠", "SIDE EFFECTS",     "A_SIDE",  med.get("side_effects", "")),
            ("💊", "DRUG INTERACTIONS","A_INTER",  parse_interactions(
                                                      med.get("drug_interactions", ""))),
        ]
        for icon, label, color_key, value in sections:
            if not value or not value.strip():
                continue
            card = tk.Frame(self._detail_inner, bg=t["CARD_BG"], padx=16, pady=14)
            card.pack(fill="x", padx=14, **pad)

            # Accent strip
            strip = tk.Frame(card, bg=t[color_key], width=4)
            strip.pack(side="left", fill="y", padx=(0, 12))

            inner = tk.Frame(card, bg=t["CARD_BG"])
            inner.pack(side="left", fill="both", expand=True)

            tk.Label(inner, text=f"{icon}  {label}",
                     bg=t["CARD_BG"], fg=t[color_key],
                     font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 6))
            tk.Label(inner, text=value.strip(),
                     bg=t["CARD_BG"], fg=t["TEXT"],
                     font=("Segoe UI", 10),
                     wraplength=390, justify="left").pack(anchor="w", fill="x")

        # ── Shop card ──
        if shop:
            shop_card = tk.Frame(self._detail_inner, bg=t["ACCENT_DARK"],
                                 padx=18, pady=16)
            shop_card.pack(fill="x", padx=14, pady=(4, 18))

            tk.Label(shop_card, text="🏪  NEAREST PHARMACY",
                     bg=t["ACCENT_DARK"], fg=t["BG"],
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 8))
            tk.Label(shop_card, text=shop["name"],
                     bg=t["ACCENT_DARK"], fg=t["BG"],
                     font=("Segoe UI", 13, "bold")).pack(anchor="w", pady=(0, 10))

            link = tk.Label(shop_card, text="📍 Open in Google Maps →",
                            bg=t["ACCENT_DARK"], fg=t["BG"],
                            font=("Segoe UI", 10, "bold"), cursor="hand2")
            link.pack(anchor="w")
            link.bind("<Button-1>",
                      lambda e, url=shop["url"]: webbrowser.open(url))

    # ── Theme switch ──────────────────────────────────────────────────────────
    def _change_theme(self, _=None):
        name = self.theme_combo.get()
        if name == self._theme_name:
            return
        self._theme_name = name
        self._t = THEMES[name]

        # Destroy and rebuild everything
        for w in self.winfo_children():
            w.destroy()

        self.configure(bg=self._t["BG"])
        self._build_styles()
        self._build_ui()

        # Restore state
        if self.data:
            self._db_count.config(text=f"{len(self.data):,}")
            self.file_path_var.set(self._loaded_path)
            self._file_lbl.config(fg=self._t["ACCENT"])
            self.status_var.set(
                f"✅ {len(self.data):,} medicines loaded — ready to search")
            self._status_dot.config(fg=self._t["SUCCESS"])
        if self._results:
            self._render_table(self._results)

    # ── Data loading ──────────────────────────────────────────────────────────
    def _auto_load_default(self):
        def worker():
            data = load_data(DEFAULT_CSV)
            self.after(0, self._on_load_done, data, DEFAULT_CSV)
        threading.Thread(target=worker, daemon=True).start()

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Select Medicine Database (CSV)",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path:
            return
        self._set_status("📂 Loading…", "WARNING")
        def worker():
            data = load_data(path)
            self.after(0, self._on_load_done, data, path)
        threading.Thread(target=worker, daemon=True).start()

    def _on_load_done(self, data, path: str):
        if data is None:
            self._set_status(f"❌ Failed to load file", "DANGER")
            return
        data = remove_duplicates(data)
        self.data = data
        self._loaded_path = Path(path).name
        self.file_path_var.set(self._loaded_path)
        self._file_lbl.config(fg=self._t["ACCENT"])
        self._db_count.config(text=f"{len(data):,}")
        self._set_status(f"✅ Loaded {len(data):,} medicines — ready to search", "SUCCESS")
        self._search_entry.focus()

    # ── Search ────────────────────────────────────────────────────────────────
    def _on_query_change(self, *_):
        """Debounced real-time search."""
        if self._search_job:
            self.after_cancel(self._search_job)
        self._search_job = self.after(350, self._do_search_silent)

    def _do_search_silent(self):
        """Search triggered by typing (no warning dialogs)."""
        if not self.data or not self.query_var.get().strip():
            return
        self._do_search(silent=True)

    def _do_search(self, silent=False):
        if not self.data:
            if not silent:
                messagebox.showwarning("No Database", "Please load a CSV file first.")
            return
        query = self.query_var.get().strip()
        if not query:
            if not silent:
                messagebox.showwarning("Empty Search", "Please enter a medicine name.")
            return
        try:
            max_r = max(1, int(self.max_var.get()))
        except ValueError:
            max_r = 20

        self._set_status(f"🔍 Searching '{query}'…", "WARNING")
        results = search_medicine(self.data, query, max_r)
        self._results = results

        for item in self.tree.get_children():
            self.tree.delete(item)
        self._show_empty_detail()

        if not results:
            self._count_lbl.config(text="0")
            self._set_status(f"❌ No results for '{query}'", "DANGER")
            return

        self._render_table(results)
        self._count_lbl.config(text=str(len(results)))
        self._set_status(f"✅ {len(results)} result(s) for '{query}'", "SUCCESS")

    def _render_table(self, results: list):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for i, med in enumerate(results):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", iid=str(i), tags=(tag,),
                             values=(
                                 med.get("product_name", "—"),
                                 med.get("salt_composition", "—"),
                                 med.get("product_price", "—"),
                                 med.get("product_manufactured", "—"),
                             ))

    def _clear(self):
        self.query_var.set("")
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._results = []
        self._show_empty_detail()
        self._count_lbl.config(text="0")
        self._set_status("Ready to search", "SUCCESS")
        self._search_entry.focus()

    def _on_select(self, _=None):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        med = self._results[idx]
        key = med.get("product_name", str(idx))
        if key not in self._shop_map:
            self._shop_map[key] = random.choice(SHOPS)
        self._show_detail(med, self._shop_map[key])

    # ── AI prescription scan ──────────────────────────────────────────────────
    def _scan_prescription(self):
        if not AI_AVAILABLE:
            messagebox.showinfo("AI Unavailable",
                                "Install google-genai and set GEMINI_API_KEY to use scan.")
            return
        path = filedialog.askopenfilename(
            title="Select Prescription Image",
            filetypes=[("Images", "*.png *.jpg *.jpeg"), ("All", "*.*")])
        if not path:
            return
        self._set_status("🔄 Scanning prescription with Gemini AI…", "WARNING")
        threading.Thread(target=self._scan_thread, args=(path,), daemon=True).start()

    def _scan_thread(self, path: str):
        try:
            img = _PILImage.open(path)
            resp = _ai_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    "Extract ONLY the primary medicine name from this prescription. "
                    "Return just the name, nothing else.",
                    img
                ])
            name = resp.text.strip()
            self.after(0, self._on_scan_done, name, None)
        except Exception as e:
            self.after(0, self._on_scan_done, None, str(e))

    def _on_scan_done(self, name: str | None, err: str | None):
        if err:
            messagebox.showerror("Scan Failed", err)
            self._set_status("❌ Scan failed", "DANGER")
            return
        if name:
            self.query_var.set(name)
            self._set_status(f"✅ AI extracted: {name}", "SUCCESS")
            self._do_search()
        else:
            self._set_status("⚠ No medicine detected", "WARNING")

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _set_status(self, msg: str, level: str = "SUCCESS"):
        color_map = {"SUCCESS": "SUCCESS", "WARNING": "WARNING", "DANGER": "DANGER"}
        self.status_var.set(msg)
        self._status_dot.config(fg=self._t[color_map.get(level, "SUCCESS")])


# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = MedicineApp()
    app.mainloop()
