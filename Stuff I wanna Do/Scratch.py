import math
import tkinter as tk
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
            tk.Button(
                self.palette_area, text=text, anchor="w", command=lambda d=definition: self._add_definition(d),
                bg=color, fg="white", activebackground=color, activeforeground="white",
                relief="flat", padx=12, pady=9, font=("Arial", 10, "bold"),
            ).pack(fill="x", pady=4)
            button = self.palette_area.winfo_children()[-1]
            button.bind("<ButtonPress-1>", lambda event, d=definition: self._start_palette_drag(d))

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
            card = tk.Frame(self.workspace, bg=color, padx=9, pady=7)
            card.pack(anchor="w", fill="x", padx=8, pady=3)

            inner = tk.Frame(card, bg=color)
            inner.pack(side="left", fill="x", expand=True)
            self._build_block_contents(inner, block)

            controls = tk.Frame(card, bg=color)
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
