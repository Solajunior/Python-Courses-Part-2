import tkinter as tk
from datetime import date
from tkinter import filedialog, messagebox, scrolledtext, ttk


WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 760
APP_BACKGROUND = "#f4f1ec"
INK = "#243447"
MUTED = "#687789"
ACCENT = "#315e66"


def format_letter(
    sender: str,
    recipient: str,
    letter_date: str,
    subject: str,
    greeting: str,
    body: str,
    closing: str,
    signature: str,
) -> str:
    """Build a neatly spaced letter from its non-empty sections."""
    header = [part.strip() for part in (sender, letter_date) if part.strip()]
    recipient = recipient.strip()
    subject = subject.strip()
    greeting = greeting.strip()
    body = body.strip()
    closing = closing.strip()
    signature = signature.strip()

    sections: list[str] = []
    if header:
        sections.append("\n".join(header))
    if recipient:
        sections.append(recipient)
    if subject:
        sections.append(f"Subject: {subject}")
    if greeting:
        sections.append(greeting)
    if body:
        sections.append(body)
    if closing or signature:
        sections.append("\n".join(part for part in (closing, signature) if part))
    return "\n\n".join(sections)


class LetterWritingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Letter Writing Studio")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(850, 640)
        self.root.configure(bg=APP_BACKGROUND)
        self._configure_styles()

        page = ttk.Frame(root, padding=(26, 20))
        page.pack(fill="both", expand=True)
        page.columnconfigure(0, weight=1)
        page.rowconfigure(1, weight=1)

        header = ttk.Frame(page)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        ttk.Label(
            header,
            text="Letter Writing Studio",
            style="Title.TLabel",
        ).pack(anchor="w")
        ttk.Label(
            header,
            text="Gather your thoughts, shape your message, and make it yours.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        columns = ttk.Frame(page)
        columns.grid(row=1, column=0, sticky="nsew")
        columns.columnconfigure(0, weight=1, uniform="column")
        columns.columnconfigure(1, weight=1, uniform="column")
        columns.rowconfigure(0, weight=1)

        compose_card = ttk.LabelFrame(
            columns, text="  Write your letter  ", padding=16, style="Card.TLabelframe"
        )
        compose_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        compose_card.columnconfigure(0, weight=1)
        compose_card.rowconfigure(11, weight=1)

        self.fields: dict[str, ttk.Entry] = {}
        self._add_entry(compose_card, "sender", "Your name and address", 0)
        self._add_entry(compose_card, "recipient", "Recipient and address", 1)
        self._add_entry(
            compose_card,
            "letter_date",
            "Date",
            2,
            initial=date.today().strftime("%B %d, %Y"),
        )
        self._add_entry(compose_card, "subject", "Subject (optional)", 3)
        self._add_entry(compose_card, "greeting", "Greeting", 4, initial="Dear,")

        ttk.Label(compose_card, text="Message", style="Field.TLabel").grid(
            row=10, column=0, sticky="w", pady=(12, 5)
        )
        self.body_input = scrolledtext.ScrolledText(
            compose_card,
            height=8,
            wrap="word",
            undo=True,
            font=("Segoe UI", 10),
            padx=10,
            pady=9,
            relief="solid",
            borderwidth=1,
            background="#ffffff",
            foreground=INK,
            insertbackground=INK,
        )
        self.body_input.grid(row=11, column=0, sticky="nsew")
        self.body_input.bind("<KeyRelease>", self.update_preview)

        closing_row = ttk.Frame(compose_card)
        closing_row.grid(row=12, column=0, sticky="ew", pady=(10, 0))
        closing_row.columnconfigure(0, weight=1)
        closing_row.columnconfigure(1, weight=1)
        ttk.Label(closing_row, text="Closing", style="Field.TLabel").grid(
            row=0, column=0, sticky="w", padx=(0, 6), pady=(0, 5)
        )
        ttk.Label(closing_row, text="Your signature", style="Field.TLabel").grid(
            row=0, column=1, sticky="w", padx=(6, 0), pady=(0, 5)
        )
        self.fields["closing"] = ttk.Entry(closing_row, font=("Segoe UI", 10))
        self.fields["closing"].insert(0, "Warm regards,")
        self.fields["closing"].grid(row=1, column=0, sticky="ew", padx=(0, 6))
        self.fields["signature"] = ttk.Entry(closing_row, font=("Segoe UI", 10))
        self.fields["signature"].grid(row=1, column=1, sticky="ew", padx=(6, 0))
        self.fields["closing"].bind("<KeyRelease>", self.update_preview)
        self.fields["signature"].bind("<KeyRelease>", self.update_preview)

        preview_card = ttk.LabelFrame(
            columns,
            text="  Live preview  ",
            padding=16,
            style="Card.TLabelframe",
        )
        preview_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        preview_card.columnconfigure(0, weight=1)
        preview_card.rowconfigure(0, weight=1)

        self.preview = scrolledtext.ScrolledText(
            preview_card,
            wrap="word",
            state="disabled",
            font=("Georgia", 11),
            padx=20,
            pady=20,
            relief="solid",
            borderwidth=1,
            background="#fffefa",
            foreground="#263238",
            insertwidth=0,
        )
        self.preview.grid(row=0, column=0, sticky="nsew")

        actions = ttk.Frame(page)
        actions.grid(row=2, column=0, sticky="ew", pady=(16, 0))
        ttk.Button(
            actions, text="New letter", command=self.new_letter, style="Secondary.TButton"
        ).pack(side="left")
        ttk.Frame(actions).pack(side="left", fill="x", expand=True)
        ttk.Button(
            actions, text="Copy letter", command=self.copy_letter, style="Secondary.TButton"
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            actions, text="Save as text file", command=self.save_letter, style="Accent.TButton"
        ).pack(side="left")

        self._refresh_preview()
        self.fields["sender"].focus_set()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background=APP_BACKGROUND)
        style.configure(
            "Title.TLabel",
            background=APP_BACKGROUND,
            foreground=INK,
            font=("Segoe UI", 24, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=APP_BACKGROUND,
            foreground=MUTED,
            font=("Segoe UI", 10),
        )
        style.configure(
            "Field.TLabel",
            background=APP_BACKGROUND,
            foreground=INK,
            font=("Segoe UI", 9, "bold"),
        )
        style.configure(
            "Card.TLabelframe",
            background=APP_BACKGROUND,
            foreground=ACCENT,
            bordercolor="#d8d4cd",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=APP_BACKGROUND,
            foreground=ACCENT,
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "TEntry",
            fieldbackground="#ffffff",
            foreground=INK,
            padding=(8, 7),
            bordercolor="#d8d4cd",
        )
        style.configure(
            "TButton",
            font=("Segoe UI", 9, "bold"),
            padding=(14, 9),
        )
        style.configure(
            "Accent.TButton",
            background=ACCENT,
            foreground="#ffffff",
            bordercolor=ACCENT,
        )
        style.map("Accent.TButton", background=[("active", "#244a51")])
        style.configure(
            "Secondary.TButton",
            background="#e8e4dd",
            foreground=INK,
            bordercolor="#e8e4dd",
        )
        style.map("Secondary.TButton", background=[("active", "#dcd6cc")])

    def _add_entry(
        self,
        parent: ttk.LabelFrame,
        name: str,
        label: str,
        row: int,
        initial: str = "",
    ) -> None:
        ttk.Label(parent, text=label, style="Field.TLabel").grid(
            row=row * 2, column=0, sticky="w", pady=(0, 5 if row == 0 else 4)
        )
        entry = ttk.Entry(parent, font=("Segoe UI", 10))
        if initial:
            entry.insert(0, initial)
        entry.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(0, 4))
        entry.bind("<KeyRelease>", self.update_preview)
        self.fields[name] = entry

    def _letter_text(self) -> str:
        return format_letter(
            sender=self.fields["sender"].get(),
            recipient=self.fields["recipient"].get(),
            letter_date=self.fields["letter_date"].get(),
            subject=self.fields["subject"].get(),
            greeting=self.fields["greeting"].get(),
            body=self.body_input.get("1.0", "end-1c"),
            closing=self.fields["closing"].get(),
            signature=self.fields["signature"].get(),
        )

    def _refresh_preview(self) -> None:
        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", self._letter_text())
        self.preview.configure(state="disabled")

    def update_preview(self, _: tk.Event | None = None) -> None:
        self._refresh_preview()

    def copy_letter(self) -> None:
        letter = self._letter_text()
        if not letter.strip():
            messagebox.showinfo("Nothing to copy", "Write a little before copying your letter.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(letter)
        messagebox.showinfo("Letter copied", "Your letter is ready to paste.")

    def save_letter(self) -> None:
        letter = self._letter_text()
        if not letter.strip():
            messagebox.showinfo("Nothing to save", "Write a little before saving your letter.")
            return
        path = filedialog.asksaveasfilename(
            title="Save your letter",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="my-letter.txt",
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8", newline="\n") as letter_file:
                letter_file.write(letter + "\n")
        except OSError as error:
            messagebox.showerror("Could not save letter", f"Your letter was not saved.\n\n{error}")
            return
        messagebox.showinfo("Letter saved", f"Your letter was saved to:\n{path}")

    def new_letter(self) -> None:
        if self._letter_text().strip() and not messagebox.askyesno(
            "Start a new letter?",
            "This will clear your current letter. Save it first if you want to keep it.",
        ):
            return
        for name, entry in self.fields.items():
            entry.delete(0, "end")
            if name == "letter_date":
                entry.insert(0, date.today().strftime("%B %d, %Y"))
            elif name == "greeting":
                entry.insert(0, "Dear,")
            elif name == "closing":
                entry.insert(0, "Warm regards,")
        self.body_input.delete("1.0", "end")
        self._refresh_preview()
        self.fields["sender"].focus_set()


def main() -> None:
    root = tk.Tk()
    LetterWritingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()