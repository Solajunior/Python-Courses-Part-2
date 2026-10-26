import math
import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk


PURPLE = "#855cd6"
CATEGORY_COLORS = {
    "Motion": "#4c97ff",
    "Looks": "#9966ff",
    "Sound": "#cf63cf",
    "Events": "#ffbf00",
    "Control": "#ffab19",
    "Sensing": "#4cbfe6",
    "Operators": "#59c059",
    "Variables": "#ff8c1a",
    "My Blocks": "#ff6680",
    "Pen": "#0fbd8c",
    "Music": "#e1a91a",
}

BLOCKS = {
    "Motion": [
        ("move", "move", ("10",), "steps"),
        ("turn", "turn clockwise", ("15",), "degrees"),
        ("goto", "go to x", ("0",), "y", ("0",)),
        ("glide", "glide", ("1",), "seconds to x", ("0",), "y", ("0",)),
        ("point_direction", "point in direction", ("90",)),
        ("point_towards", "point towards", ("mouse-pointer",)),
        ("change_x", "change x by", ("10",)),
        ("set_x", "set x to", ("0",)),
        ("change_y", "change y by", ("10",)),
        ("set_y", "set y to", ("0",)),
        ("edge_bounce", "if on edge, bounce", ()),
        ("rotation_style", "set rotation style", ("left-right",)),
        ("x_position", "x position", ()),
        ("y_position", "y position", ()),
        ("direction", "direction", ()),
    ],
    "Looks": [
        ("say", "say", ("Hello!",), "for", ("2",), "seconds"),
        ("think", "think", ("Hmm...",), "for", ("2",), "seconds"),
        ("say_forever", "say", ("Hello!",)),
        ("think_forever", "think", ("Hmm...",)),
        ("show", "show", ()),
        ("hide", "hide", ()),
        ("switch_costume", "switch costume to", ("costume1",)),
        ("next_costume", "next costume", ()),
        ("switch_backdrop", "switch backdrop to", ("backdrop1",)),
        ("next_backdrop", "next backdrop", ()),
        ("change_size", "change size by", ("10",)),
        ("set_size", "set size to", ("100",), "%"),
        ("size", "size", ()),
        ("change_effect", "change", ("color",), "effect by", ("25",)),
        ("set_effect", "set", ("color",), "effect to", ("0",)),
        ("clear_effects", "clear graphic effects", ()),
        ("go_front", "go to front layer", ()),
        ("go_back", "go back", ("1",), "layers"),
    ],
    "Sound": [
        ("play_sound", "start sound", ("Meow",)),
        ("play_sound_wait", "start sound", ("Meow",), "and wait"),
        ("stop_sounds", "stop all sounds", ()),
        ("change_volume", "change volume by", ("-10",)),
        ("set_volume", "set volume to", ("100",), "%"),
        ("volume", "volume", ()),
        ("change_pitch", "change pitch by", ("10",)),
        ("set_pitch", "set pitch to", ("100",)),
        ("play_drum", "play drum", ("1",), "for", ("0.25",), "beats"),
        ("play_note", "play note", ("60",), "for", ("0.5",), "beats"),
    ],
    "Events": [
        ("when_flag", "when green flag clicked", ()),
        ("when_key", "when", ("space",), "key pressed"),
        ("when_clicked", "when this sprite clicked", ()),
        ("when_backdrop", "when backdrop switches to", ("backdrop1",)),
        ("when_loudness", "when loudness >", ("10",)),
        ("broadcast", "broadcast", ("message1",)),
        ("broadcast_wait", "broadcast", ("message1",), "and wait"),
        ("when_receive", "when I receive", ("message1",)),
    ],
    "Control": [
        ("repeat", "repeat", ("4",), "times"),
        ("end", "end repeat", ()),
        ("forever", "forever", ()),
        ("end_forever", "end forever", ()),
        ("if", "if", ("condition",), "then"),
        ("else", "else", ()),
        ("end_if", "end if", ()),
        ("if_else", "if", ("condition",), "then ... else"),
        ("repeat_until", "repeat until", ("condition",)),
        ("wait_until", "wait until", ("condition",)),
        ("wait", "wait", ("1",), "seconds"),
        ("stop", "stop", ("all",)),
        ("create_clone", "create clone of", ("myself",)),
        ("delete_clone", "delete this clone", ()),
    ],
    "Sensing": [
        ("touching", "touching", ("mouse-pointer",), "?"),
        ("touching_color", "touching color", ("#ff0000",), "?"),
        ("color_touching", "color", ("#ff0000",), "is touching", ("#00ff00",), "?"),
        ("distance", "distance to", ("mouse-pointer",)),
        ("ask", "ask", ("What's your name?",), "and wait"),
        ("answer", "answer", ()),
        ("key_pressed", "key", ("space",), "pressed?"),
        ("mouse_down", "mouse down?"),
        ("mouse_x", "mouse x"),
        ("mouse_y", "mouse y"),
        ("loudness", "loudness"),
        ("timer", "timer"),
        ("reset_timer", "reset timer"),
        ("property_of", "property", ("x position",), "of", ("Sprite1",)),
        ("current_date", "current", ("year",)),
        ("days_since_2000", "days since 2000"),
        ("username", "username"),
    ],
    "Operators": [
        ("add", ("",), ("10",), "+", ("10",)),
        ("subtract", ("",), ("10",), "-", ("10",)),
        ("multiply", ("",), ("10",), "*", ("10",)),
        ("divide", ("",), ("10",), "/", ("10",)),
        ("random", "pick random", ("1",), "to", ("10",)),
        ("greater_than", ("",), ("50",), ">", ("50",)),
        ("less_than", ("",), ("50",), "<", ("50",)),
        ("equals", ("",), ("50",), "=", ("50",)),
        ("and", ("",), ("true",), "and", ("true",)),
        ("or", ("",), ("true",), "or", ("false",)),
        ("not", "not", ("true",)),
        ("join", "join", ("hello",), ("world",)),
        ("letter_of", "letter", ("1",), "of", ("world",)),
        ("length", "length of", ("world",)),
        ("contains", ("",), ("world",), "contains", ("word",), "?"),
        ("modulo", ("",), ("10",), "mod", ("3",)),
        ("round", "round", ("3.14",)),
        ("math_operation", ("",), ("abs",), "of", ("10",)),
    ],
    "Variables": [
        ("set_variable", "set", ("my variable",), "to", ("0",)),
        ("change_variable", "change", ("my variable",), "by", ("1",)),
        ("show_variable", "show variable", ("my variable",)),
        ("hide_variable", "hide variable", ("my variable",)),
        ("variable", ("my variable",)),
    ],
    "My Blocks": [
        ("define_block", "define", ("my block",)),
    ],
    "Pen": [
        ("erase_all", "erase all"),
        ("stamp", "stamp"),
        ("pen_down", "pen down"),
        ("pen_up", "pen up"),
        ("set_pen_color", "set pen color to", ("#0000ff",)),
        ("change_pen_color", "change pen color by", ("10",)),
        ("set_pen_size", "set pen size to", ("1",)),
        ("change_pen_size", "change pen size by", ("1",)),
    ],
    "Music": [
        ("music_instrument", "set instrument to", ("1",)),
        ("music_drum", "play drum", ("1",), "for", ("0.25",), "beats"),
        ("music_note", "play note", ("60",), "for", ("0.5",), "beats"),
        ("music_rest", "rest for", ("0.25",), "beats"),
        ("music_tempo", "set tempo to", ("60",), "bpm"),
        ("music_change_tempo", "change tempo by", ("20",)),
        ("music_get_tempo", "tempo"),
    ],
}


class Scratch:
    def __init__(self, root):
        self.root = root
        self.root.title("Scratch")
        self.root.geometry("1280x760")
        self.root.minsize(1000, 620)
        self.root.configure(bg="#f7f7f7")

        self.blocks = []
        self.running = False
        self.run_token = 0
        self.sprite_x = 0
        self.sprite_y = 0
        self.direction = 90
        self.sprite_visible = True
        self.category = tk.StringVar(value="Motion")
        self.drag_definition = None
        self.reading_schedule = []
        self.planner_window = None

        self._build_ui()
        self.add_block("when_flag", ())
        self._draw_stage()
        self._render_blocks()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#ffffff", height=56)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(
            header, text="Scratch", bg="#ffffff", fg=PURPLE,
            font=("Arial", 22, "bold"),
        ).pack(side="left", padx=18)
        tk.Label(
            header, text="Create stories, games, and animations",
            bg="#ffffff", fg="#575e75", font=("Arial", 11),
        ).pack(side="left", padx=12)

        toolbar = tk.Frame(self.root, bg="#f7f7f7", padx=12, pady=8)
        toolbar.pack(fill="x")
        self.run_button = tk.Button(
            toolbar, text="🟢  Run", command=self.run_script,
            bg="#4caf50", fg="white", activebackground="#43a047",
            activeforeground="white", relief="flat", padx=14, pady=7,
            font=("Arial", 10, "bold"),
        )
        self.run_button.pack(side="left", padx=(0, 8))
        tk.Button(
            toolbar, text="■  Stop", command=self.stop_script,
            bg="#ef5350", fg="white", activebackground="#e53935",
            activeforeground="white", relief="flat", padx=14, pady=7,
            font=("Arial", 10, "bold"),
        ).pack(side="left")
        tk.Button(
            toolbar, text="Reset", command=self.reset_sprite,
            relief="flat", padx=14, pady=7,
        ).pack(side="left", padx=8)
        tk.Button(
            toolbar, text="Clear blocks", command=self.clear_blocks,
            relief="flat", padx=14, pady=7,
        ).pack(side="left")
        tk.Button(
            toolbar, text="Reading planner", command=self.open_reading_planner,
            relief="flat", padx=14, pady=7,
        ).pack(side="left", padx=8)
        self.status_var = tk.StringVar(value="Choose blocks from a category to build your script.")
        tk.Label(
            toolbar, textvariable=self.status_var, bg="#f7f7f7",
            fg="#575e75", font=("Arial", 10),
        ).pack(side="right", padx=8)

        body = tk.Frame(self.root, bg="#f7f7f7")
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        palette = tk.Frame(body, bg="#ffffff", width=350)
        palette.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        palette.grid_propagate(False)
        tk.Label(
            palette, text="BLOCKS", bg="#ffffff", fg="#575e75",
            font=("Arial", 10, "bold"), anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 8))
        palette_content = tk.Frame(palette, bg="#ffffff")
        palette_content.pack(fill="both", expand=True, padx=8, pady=(0, 8))
        category_list = tk.Frame(palette_content, bg="#ffffff", width=96)
        category_list.pack(side="left", fill="y")
        category_list.pack_propagate(False)
        for name, color in CATEGORY_COLORS.items():
            tk.Radiobutton(
                category_list, text=name, value=name, variable=self.category,
                command=self._render_palette, indicatoron=False, padx=5, pady=7,
                bg=color, fg="white", selectcolor=color, activebackground=color,
                activeforeground="white", relief="flat", font=("Arial", 8, "bold"),
            ).pack(fill="x", pady=2)

        palette_list = tk.Frame(palette_content, bg="#ffffff")
        palette_list.pack(side="left", fill="both", expand=True, padx=(8, 0))
        self.palette_canvas = tk.Canvas(
            palette_list, bg="#ffffff", highlightthickness=0,
        )
        palette_scroll = ttk.Scrollbar(
            palette_list, orient="vertical", command=self.palette_canvas.yview,
        )
        self.palette_canvas.configure(yscrollcommand=palette_scroll.set)
        self.palette_canvas.pack(side="left", fill="both", expand=True)
        palette_scroll.pack(side="right", fill="y")
        self.palette_area = tk.Frame(self.palette_canvas, bg="#ffffff")
        self.palette_window = self.palette_canvas.create_window(
            (0, 0), window=self.palette_area, anchor="nw",
        )
        self.palette_area.bind(
            "<Configure>",
            lambda event: self.palette_canvas.configure(
                scrollregion=self.palette_canvas.bbox("all")
            ),
        )
        self.palette_canvas.bind(
            "<Configure>",
            lambda event: self.palette_canvas.itemconfigure(
                self.palette_window, width=event.width,
            ),
        )
        tk.Label(
            palette, text="Drag a block into your script, or click it to add it.",
            bg="#ffffff", fg="#7c8191", font=("Arial", 9), wraplength=320,
            justify="left",
        ).pack(fill="x", padx=12, pady=(0, 12))
        self.root.bind_all("<ButtonRelease-1>", self._finish_palette_drag, add="+")
        self._render_palette()

        scripts_panel = tk.Frame(body, bg="#f0f0f0")
        scripts_panel.grid(row=0, column=1, sticky="nsew", padx=(0, 8))
        scripts_panel.rowconfigure(1, weight=1)
        scripts_panel.columnconfigure(0, weight=1)
        tk.Label(
            scripts_panel, text="Code", bg="#f0f0f0", fg="#575e75",
            font=("Arial", 11, "bold"), anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=8, pady=(8, 4))
        self.workspace_canvas = tk.Canvas(
            scripts_panel, bg="#ffffff", highlightthickness=0,
        )
        workspace_scroll = ttk.Scrollbar(
            scripts_panel, orient="vertical", command=self.workspace_canvas.yview,
        )
        self.workspace_canvas.configure(yscrollcommand=workspace_scroll.set)
        self.workspace_canvas.grid(row=1, column=0, sticky="nsew")
        workspace_scroll.grid(row=1, column=1, sticky="ns")
        self.workspace = tk.Frame(self.workspace_canvas, bg="#ffffff")
        self.workspace_window = self.workspace_canvas.create_window(
            (12, 12), window=self.workspace, anchor="nw",
        )
        self.workspace.bind("<Configure>", self._workspace_changed)
        self.workspace_canvas.bind("<Configure>", self._workspace_resized)

        stage_panel = tk.Frame(body, bg="#ffffff", width=390)
        stage_panel.grid(row=0, column=2, sticky="nsew")
        stage_panel.grid_propagate(False)
        tk.Label(
            stage_panel, text="Stage", bg="#ffffff", fg="#575e75",
            font=("Arial", 11, "bold"), anchor="w",
        ).pack(fill="x", padx=12, pady=(12, 7))
        self.stage = tk.Canvas(
            stage_panel, width=360, height=270, bg="#ffffff",
            highlightthickness=1, highlightbackground="#dddddd",
        )
        self.stage.pack(padx=12, pady=(0, 10))
        self.stage.bind("<Configure>", lambda event: self._draw_stage())
        self.sprite_name_var = tk.StringVar(value="Sprite1")
        tk.Label(
            stage_panel, textvariable=self.sprite_name_var,
            bg="#ffffff", fg="#575e75", font=("Arial", 10),
        ).pack(anchor="w", padx=14)
        tk.Label(
            stage_panel, text="x: 0     y: 0     direction: 90°",
            name="sprite_info", bg="#ffffff", fg="#7c8191",
            font=("Arial", 9),
        ).pack(anchor="w", padx=14, pady=(3, 0))
        self.sprite_info = stage_panel.children["sprite_info"]
        self.bubble_var = tk.StringVar(value="")
        tk.Label(
            stage_panel, textvariable=self.bubble_var, bg="#ffffff",
            fg="#575e75", font=("Arial", 10), wraplength=330, justify="left",
        ).pack(fill="x", padx=14, pady=12)

    def _render_palette(self):
        for child in self.palette_area.winfo_children():
            child.destroy()
        blocks = BLOCKS.get(self.category.get(), [])
        for definition in blocks:
            text = self._block_name(definition)
            color = CATEGORY_COLORS[self.category.get()]
            block = tk.Canvas(
                self.palette_area, height=44, bg="#ffffff", highlightthickness=0,
            )
            block.pack(fill="x", pady=2)
            block.bind(
                "<Configure>",
                lambda event, widget=block, block_id=definition[0],
                category=self.category.get(), color=color: self._draw_block_shape(
                    widget, event.width, event.height, block_id, category, color,
                ),
            )
            self._draw_block_shape(
                block, block.winfo_width(), 44, definition[0],
                self.category.get(), color,
            )
            block.create_text(
                14, 22, text=text, anchor="w", fill="white",
                font=("Arial", 10, "bold"), tags=("block-label",),
            )
            block.bind(
                "<ButtonPress-1>",
                lambda event, d=definition: self._start_palette_drag(d),
            )
            block.bind(
                "<ButtonRelease-1>",
                lambda event, d=definition: self._click_palette_block(d),
            )

    def _click_palette_block(self, definition):
        if self.drag_definition == definition:
            self.drag_definition = None
            self._add_definition(definition)

    def _block_shape(self, block_id, category):
        if block_id.startswith("when_"):
            return "hat"
        if block_id in {
            "touching", "touching_color", "color_touching", "key_pressed",
            "mouse_down", "greater_than", "less_than", "equals", "and",
            "or", "not", "contains",
        }:
            return "boolean"
        if category in {"Operators", "Sensing"} or block_id in {
            "x_position", "y_position", "direction", "size", "volume",
            "answer", "loudness", "timer", "mouse_x", "mouse_y",
            "days_since_2000", "username", "variable", "music_get_tempo",
        }:
            return "reporter"
        return "stack"

    def _draw_block_shape(self, canvas, width, height, block_id, category, color):
        canvas.delete("block-shape")
        if width < 2 or height < 2:
            return
        shape = self._block_shape(block_id, category)
        if shape == "reporter":
            canvas.create_oval(
                1, 2, width - 1, height - 2, fill=color, outline="",
                tags=("block-shape",),
            )
        elif shape == "boolean":
            canvas.create_polygon(
                1, height / 2, 10, 2, width - 10, 2,
                width - 1, height / 2, width - 10, height - 2,
                10, height - 2, fill=color, outline="", tags=("block-shape",),
            )
        else:
            points = [
                0, 10,
                18, 10, 18, 14, 21, 18, 26, 20, 34, 20,
                39, 18, 42, 14, 42, 10,
                width, 10, width, height - 10,
                39, height - 10, 36, height - 4, 33, height,
                25, height, 22, height - 4, 19, height - 10,
                0, height - 10,
            ]
            if shape == "hat":
                points = [
                    0, 14, 2, 8, 7, 4, 15, 2, 28, 2, 36, 4,
                    41, 9, 43, 14,
                    width, 14, width, height - 10,
                    39, height - 10, 36, height - 4, 33, height,
                    25, height, 22, height - 4, 19, height - 10,
                    0, height - 10,
                ]
            canvas.create_polygon(
                *points, fill=color, outline="", tags=("block-shape",),
            )
        canvas.tag_lower("block-shape")

    def open_reading_planner(self):
        if self.planner_window is not None and self.planner_window.winfo_exists():
            self.planner_window.lift()
            return

        window = tk.Toplevel(self.root)
        window.title("Reading Schedule Planner")
        window.geometry("720x540")
        window.minsize(600, 420)
        window.configure(bg="#f7f7f7")
        self.planner_window = window

        form = tk.Frame(window, bg="#ffffff", padx=16, pady=14)
        form.pack(fill="x", padx=14, pady=14)
        tk.Label(
            form, text="Plan your reading", bg="#ffffff", fg="#575e75",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, columnspan=6, sticky="w", pady=(0, 12))

        self.book_title_var = tk.StringVar()
        self.page_count_var = tk.StringVar()
        self.pages_per_day_var = tk.StringVar(value="20")
        self.start_date_var = tk.StringVar(value=date.today().isoformat())
        fields = [
            ("Book", self.book_title_var, 20),
            ("Total pages", self.page_count_var, 10),
            ("Pages per day", self.pages_per_day_var, 10),
            ("Start date (YYYY-MM-DD)", self.start_date_var, 14),
        ]
        for column, (label, variable, width) in enumerate(fields):
            field = tk.Frame(form, bg="#ffffff")
            field.grid(row=1, column=column, sticky="w", padx=(0, 10))
            tk.Label(
                field, text=label, bg="#ffffff", fg="#575e75",
                font=("Arial", 9, "bold"),
            ).pack(anchor="w", pady=(0, 4))
            tk.Entry(field, textvariable=variable, width=width).pack(anchor="w")

        tk.Button(
            form, text="Create schedule", command=self._generate_reading_schedule,
            bg="#4caf50", fg="white", activebackground="#43a047",
            activeforeground="white", relief="flat", padx=12, pady=7,
            font=("Arial", 10, "bold"),
        ).grid(row=2, column=0, sticky="w", pady=(14, 0))

        schedule_panel = tk.Frame(window, bg="#ffffff", padx=12, pady=10)
        schedule_panel.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        self.reading_summary_var = tk.StringVar(value="Create a schedule to get started.")
        tk.Label(
            schedule_panel, textvariable=self.reading_summary_var,
            bg="#ffffff", fg="#575e75", font=("Arial", 10, "bold"),
            anchor="w",
        ).pack(fill="x", pady=(0, 8))
        columns = ("day", "pages", "status")
        self.reading_tree = ttk.Treeview(
            schedule_panel, columns=columns, show="headings", height=12,
        )
        self.reading_tree.heading("day", text="Date")
        self.reading_tree.heading("pages", text="Pages to read")
        self.reading_tree.heading("status", text="Progress")
        self.reading_tree.column("day", width=150, anchor="w")
        self.reading_tree.column("pages", width=180, anchor="w")
        self.reading_tree.column("status", width=130, anchor="center")
        scrollbar = ttk.Scrollbar(
            schedule_panel, orient="vertical", command=self.reading_tree.yview,
        )
        self.reading_tree.configure(yscrollcommand=scrollbar.set)
        self.reading_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = tk.Frame(window, bg="#f7f7f7")
        actions.pack(fill="x", padx=14, pady=(0, 14))
        tk.Button(
            actions, text="Toggle selected as complete",
            command=self._toggle_reading_day, relief="flat", padx=12, pady=7,
        ).pack(side="left")
        self._refresh_reading_schedule()
        window.protocol("WM_DELETE_WINDOW", self._close_reading_planner)

    def _close_reading_planner(self):
        if self.planner_window is not None:
            self.planner_window.destroy()
        self.planner_window = None

    def _generate_reading_schedule(self):
        title = self.book_title_var.get().strip()
        if not title:
            self.reading_summary_var.set("Enter a book title to create your schedule.")
            return
        try:
            total_pages = int(self.page_count_var.get())
            pages_per_day = int(self.pages_per_day_var.get())
            start_day = date.fromisoformat(self.start_date_var.get().strip())
        except ValueError:
            self.reading_summary_var.set(
                "Enter valid positive page counts and a date in YYYY-MM-DD format."
            )
            return
        if total_pages <= 0 or pages_per_day <= 0:
            self.reading_summary_var.set("Page counts must be greater than zero.")
            return

        self.reading_schedule = []
        first_page = 1
        day_number = 0
        while first_page <= total_pages:
            last_page = min(first_page + pages_per_day - 1, total_pages)
            self.reading_schedule.append({
                "date": start_day + timedelta(days=day_number),
                "first_page": first_page,
                "last_page": last_page,
                "complete": False,
            })
            first_page = last_page + 1
            day_number += 1
        self._refresh_reading_schedule(title)

    def _refresh_reading_schedule(self, title=None):
        if not hasattr(self, "reading_tree") or not self.reading_tree.winfo_exists():
            return
        for item in self.reading_tree.get_children():
            self.reading_tree.delete(item)
        for index, day in enumerate(self.reading_schedule):
            status = "Complete" if day["complete"] else "To read"
            self.reading_tree.insert(
                "", "end", iid=str(index),
                values=(
                    day["date"].strftime("%a, %b %d, %Y"),
                    f"Pages {day['first_page']}–{day['last_page']}",
                    status,
                ),
            )
        if title is None:
            title = self.book_title_var.get().strip() if hasattr(
                self, "book_title_var"
            ) else ""
        if self.reading_schedule:
            completed = sum(day["complete"] for day in self.reading_schedule)
            self.reading_summary_var.set(
                f"{title or 'Reading schedule'} · {completed} of "
                f"{len(self.reading_schedule)} days complete"
            )
        else:
            self.reading_summary_var.set("Create a schedule to get started.")

    def _toggle_reading_day(self):
        selected = self.reading_tree.selection()
        if not selected:
            self.reading_summary_var.set("Select a reading day to update its progress.")
            return
        for item in selected:
            index = int(item)
            day = self.reading_schedule[index]
            day["complete"] = not day["complete"]
        self._refresh_reading_schedule()

    def _start_palette_drag(self, definition):
        self.drag_definition = definition
        self.status_var.set(f"Dragging “{self._block_name(definition)}” block…")

    def _finish_palette_drag(self, event):
        definition = self.drag_definition
        self.drag_definition = None
        if definition is None:
            return
        left = self.workspace_canvas.winfo_rootx()
        top = self.workspace_canvas.winfo_rooty()
        right = left + self.workspace_canvas.winfo_width()
        bottom = top + self.workspace_canvas.winfo_height()
        if left <= event.x_root <= right and top <= event.y_root <= bottom:
            self._add_definition(definition)
            return
        if self.status_var.get().startswith("Dragging"):
            self.status_var.set("Choose blocks from a category to build your script.")

    def _add_definition(self, definition):
        block_id = definition[0]
        values = []
        for item in definition[1:]:
            if isinstance(item, tuple):
                values.extend(item)
        self.add_block(block_id, values)
        self.status_var.set(f"Added “{self._block_name(definition)}” block.")

    def _block_name(self, definition):
        if isinstance(definition[1], str):
            return definition[1]
        return definition[0].replace("_", " ")

    def add_block(self, block_id, values):
        self.blocks.append({"id": block_id, "values": list(values)})
        self._render_blocks()

    def clear_blocks(self):
        self.stop_script()
        self.blocks = []
        self.add_block("when_flag", ())
        self.status_var.set("Script cleared. Your green-flag event is ready.")

    def _workspace_changed(self, event=None):
        self.workspace_canvas.configure(scrollregion=self.workspace_canvas.bbox("all"))

    def _workspace_resized(self, event):
        self.workspace_canvas.itemconfigure(self.workspace_window, width=event.width - 24)

    def _render_blocks(self):
        self._block_entries = {}
        for child in self.workspace.winfo_children():
            child.destroy()
        if not self.blocks:
            tk.Label(
                self.workspace, text="Add blocks from the palette to get started.",
                bg="#ffffff", fg="#8a8f9e", font=("Arial", 11),
            ).pack(anchor="nw", padx=10, pady=14)
            return

        for index, block in enumerate(self.blocks):
            block_id = block["id"]
            category = self._category_for(block_id)
            color = CATEGORY_COLORS[category]
            card = tk.Canvas(
                self.workspace, height=52, bg="#ffffff", highlightthickness=0,
            )
            card.pack(anchor="w", fill="x", padx=8, pady=1)

            contents = tk.Frame(card, bg=color)
            contents.pack(fill="x", expand=True, padx=22, pady=(13, 9))
            self._build_block_contents(contents, block)

            controls = tk.Frame(contents, bg=color)
            controls.pack(side="right", padx=(4, 0))
            tk.Button(
                controls, text="↑", command=lambda i=index: self._move_block(i, -1),
                bg=color, fg="white", relief="flat", padx=3, font=("Arial", 9, "bold"),
            ).pack(side="left")
            tk.Button(
                controls, text="↓", command=lambda i=index: self._move_block(i, 1),
                bg=color, fg="white", relief="flat", padx=3, font=("Arial", 9, "bold"),
            ).pack(side="left")
            tk.Button(
                controls, text="×", command=lambda i=index: self._remove_block(i),
                bg=color, fg="white", relief="flat", padx=4, font=("Arial", 12, "bold"),
            ).pack(side="left")
            card.bind(
                "<Configure>",
                lambda event, widget=card, block_id=block_id, category=category,
                color=color: self._draw_block_shape(
                    widget, event.width, event.height, block_id, category, color,
                ),
            )
            self._draw_block_shape(
                card, card.winfo_width(), 52, block_id, category, color,
            )
        self.workspace.update_idletasks()
        self._workspace_changed()

    def _build_block_contents(self, parent, block):
        block_id = block["id"]
        values = block["values"]
        definition = next(
            (
                definition
                for definitions in BLOCKS.values()
                for definition in definitions
                if definition[0] == block_id
            ),
            (block_id, block_id.replace("_", " ")),
        )
        value_index = 0
        for item in definition[1:]:
            if isinstance(item, str):
                tk.Label(
                    parent, text=item, bg=parent["bg"], fg="white",
                    font=("Arial", 10, "bold"),
                ).pack(side="left", padx=(0, 5))
            elif isinstance(item, tuple):
                for default in item:
                    entry = tk.Entry(
                        parent, width=max(5, min(14, len(str(default)) + 2)),
                        relief="flat", justify="center", font=("Arial", 10),
                    )
                    entry.insert(
                        0, str(values[value_index]) if value_index < len(values)
                        else str(default),
                    )
                    entry.pack(side="left", padx=3, ipady=2)
                    entry.bind(
                        "<FocusOut>",
                        lambda event, current=block: self._save_block_values(current),
                    )
                    entry.bind(
                        "<Return>",
                        lambda event, current=block: self._save_block_values(current),
                    )
                    self._block_entries.setdefault(id(block), []).append(entry)
                    value_index += 1

    def _save_block_values(self, block):
        entries = getattr(self, "_block_entries", {}).get(id(block), [])
        if entries:
            block["values"] = [entry.get() for entry in entries]

    def _category_for(self, block_id):
        for category, definitions in BLOCKS.items():
            if any(definition[0] == block_id for definition in definitions):
                return category
        return "Motion"

    def _move_block(self, index, offset):
        destination = index + offset
        if 0 <= destination < len(self.blocks):
            self.blocks[index], self.blocks[destination] = self.blocks[destination], self.blocks[index]
            self._render_blocks()

    def _remove_block(self, index):
        if self.blocks[index]["id"] == "when_flag":
            self.status_var.set("The green-flag event block starts the script and cannot be removed.")
            return
        self.blocks.pop(index)
        self._render_blocks()

    def _draw_stage(self):
        if not hasattr(self, "stage"):
            return
        self.stage.delete("all")
        width = max(self.stage.winfo_width(), 360)
        height = max(self.stage.winfo_height(), 270)
        self.stage.create_rectangle(1, 1, width - 1, height - 1, fill="#ffffff", outline="")
        self.stage.create_oval(width - 75, 20, width - 35, 60, fill="#ffdf70", outline="")
        for x in range(0, width, 40):
            self.stage.create_line(x, height - 26, x, height - 5, fill="#e9f5e1")
        self.stage.create_rectangle(0, height - 27, width, height, fill="#e9f5e1", outline="")
        if not self.sprite_visible:
            return

        cx = width / 2 + self.sprite_x
        cy = height / 2 - self.sprite_y
        # Keep the sprite on the visible stage.
        cx = min(max(25, cx), width - 25)
        cy = min(max(35, cy), height - 20)
        self.stage.create_polygon(cx - 20, cy - 22, cx - 17, cy - 43, cx - 2, cy - 27,
                                  fill="#f4a261", outline="#9c5a27", width=2)
        self.stage.create_polygon(cx + 3, cy - 27, cx + 19, cy - 43, cx + 21, cy - 21,
                                  fill="#f4a261", outline="#9c5a27", width=2)
        self.stage.create_oval(cx - 23, cy - 30, cx + 23, cy + 18,
                               fill="#ffbd69", outline="#9c5a27", width=2)
        self.stage.create_oval(cx - 11, cy - 12, cx - 6, cy - 5, fill="#292929", outline="")
        self.stage.create_oval(cx + 6, cy - 12, cx + 11, cy - 5, fill="#292929", outline="")
        self.stage.create_oval(cx - 3, cy - 2, cx + 3, cy + 2, fill="#d95d5d", outline="")
        radians = math.radians(self.direction)
        tip_x = cx + math.sin(radians) * 31
        tip_y = cy - math.cos(radians) * 31
        self.stage.create_line(cx, cy + 18, tip_x, tip_y, fill="#555555", width=3, arrow=tk.LAST)
        self.sprite_info.config(
            text=f"x: {self.sprite_x}     y: {self.sprite_y}     direction: {self.direction}°"
        )

    def reset_sprite(self):
        self.stop_script()
        self.sprite_x = 0
        self.sprite_y = 0
        self.direction = 90
        self.sprite_visible = True
        self.bubble_var.set("")
        self._draw_stage()
        self.status_var.set("Sprite reset.")

    def stop_script(self):
        self.running = False
        self.run_token += 1
        self.run_button.config(text="🟢  Run")

    def _read_block_inputs(self):
        for block in self.blocks:
            self._save_block_values(block)
        result = []
        for block in self.blocks:
            block_id = block["id"]
            values = block["values"]
            if block_id not in {
                "when_flag", "move", "turn", "goto", "say", "think",
                "show", "hide", "repeat", "end", "wait",
            }:
                raise ValueError(
                    f"The {block_id.replace('_', ' ')} block is in the palette "
                    "but is not runnable in this preview yet."
                )
            if block_id in {"move", "turn", "wait", "repeat"}:
                value = float(values[0])
                if not math.isfinite(value):
                    raise ValueError("Enter a finite number for every block input.")
                if block_id != "wait" and not value.is_integer():
                    raise ValueError(f"{block_id.title()} needs a whole number.")
                if block_id == "wait" and value < 0:
                    raise ValueError("Wait time cannot be negative.")
                if block_id == "repeat" and value < 0:
                    raise ValueError("Repeat count cannot be negative.")
                value = int(value) if value.is_integer() else value
                result.append((block_id, value))
            elif block_id == "goto":
                result.append((block_id, int(values[0]), int(values[1])))
            elif block_id in {"say", "think"}:
                duration = float(values[1])
                if not math.isfinite(duration):
                    raise ValueError("Speech duration must be a finite number.")
                if duration < 0:
                    raise ValueError("Speech duration cannot be negative.")
                result.append((block_id, values[0], duration))
            else:
                result.append((block_id,))
        return result

    def _compile_blocks(self, instructions):
        def parse(index, inside_repeat=False):
            actions = []
            while index < len(instructions):
                instruction = instructions[index]
                index += 1
                block_id = instruction[0]
                if block_id == "end":
                    if not inside_repeat:
                        raise ValueError("There is an “end repeat” block without a matching “repeat” block.")
                    return actions, index
                if block_id == "repeat":
                    count = instruction[1]
                    body, index = parse(index, inside_repeat=True)
                    actions.extend(body * count)
                elif block_id != "when_flag":
                    actions.append(instruction)
            if inside_repeat:
                raise ValueError("A “repeat” block needs an “end repeat” block.")
            return actions, index

        return parse(0)[0]

    def run_script(self):
        self.stop_script()
        try:
            instructions = self._read_block_inputs()
            actions = self._compile_blocks(instructions)
        except (ValueError, IndexError) as exc:
            self.status_var.set(f"Block error: {exc}")
            return
        self.reset_sprite()
        self.running = True
        token = self.run_token
        self.run_button.config(text="Running…")
        self.status_var.set("Running script…")
        self._run_next(actions, 0, token)

    def _run_next(self, actions, index, token):
        if not self.running or token != self.run_token:
            return
        if index >= len(actions):
            self.running = False
            self.run_button.config(text="🟢  Run")
            self.status_var.set("Script finished.")
            return

        instruction = actions[index]
        block_id = instruction[0]
        delay = 120
        if block_id == "move":
            distance = instruction[1]
            self.sprite_x += round(math.sin(math.radians(self.direction)) * distance)
            self.sprite_y += round(math.cos(math.radians(self.direction)) * distance)
        elif block_id == "turn":
            self.direction = (self.direction + instruction[1]) % 360
        elif block_id == "goto":
            self.sprite_x, self.sprite_y = instruction[1], instruction[2]
        elif block_id in {"say", "think"}:
            self.bubble_var.set(instruction[1])
            delay = max(120, int(instruction[2] * 1000))
        elif block_id == "show":
            self.sprite_visible = True
        elif block_id == "hide":
            self.sprite_visible = False
        elif block_id == "wait":
            delay = max(0, int(instruction[1] * 1000))

        self._draw_stage()
        self.root.after(delay, lambda: self._run_next(actions, index + 1, token))


def main():
    root = tk.Tk()
    Scratch(root)
    root.mainloop()


if __name__ == "__main__":
    main()
