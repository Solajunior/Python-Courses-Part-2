import base64
import io
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

import pygame


WINDOW_WIDTH = 620
WINDOW_HEIGHT = 620
BANNER_WIDTH = 560
BANNER_HEIGHT = 140


def make_banner_image() -> bytes:
    pygame.font.init()
    banner = pygame.Surface((BANNER_WIDTH, BANNER_HEIGHT))
    banner.fill((31, 56, 82))
    pygame.draw.rect(banner, (66, 126, 143), (0, 108, BANNER_WIDTH, 32))
    pygame.draw.circle(banner, (246, 190, 92), (510, 40), 22)

    title_font = pygame.font.SysFont("arial", 32, bold=True)
    subtitle_font = pygame.font.SysFont("arial", 17)
    title = title_font.render("WORKSHOP CHECK-IN", True, (255, 255, 255))
    subtitle = subtitle_font.render("A warm welcome starts here", True, (218, 231, 235))
    banner.blit(title, (28, 30))
    banner.blit(subtitle, (30, 76))

    image_buffer = io.BytesIO()
    pygame.image.save(banner, image_buffer, "banner.png")
    return base64.b64encode(image_buffer.getvalue())


def make_welcome_message(name: str, workshop_date: str) -> str:
    return (
        f"Welcome to the workshop, {name}!\n"
        f"We're glad you're joining us.\n"
        f"Workshop date: {workshop_date}\n"
        "Please get settled and enjoy the session."
    )


class WorkshopGreetingApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.workshop_date = date.today().strftime("%B %d, %Y")
        self.root.title("Workshop Participant Check-In")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(520, 540)
        self.root.configure(bg="#f2f5f7")

        content = ttk.Frame(root, padding=24)
        content.pack(fill="both", expand=True)

        self.banner_image = tk.PhotoImage(data=make_banner_image(), format="png")
        ttk.Label(content, image=self.banner_image).pack(fill="x", pady=(0, 20))

        ttk.Label(content, text="Participant name", font=("Segoe UI", 11, "bold")).pack(
            anchor="w"
        )
        self.name_entry = ttk.Entry(content, font=("Segoe UI", 12))
        self.name_entry.pack(fill="x", pady=(6, 14))
        self.name_entry.bind("<Return>", self.check_in)

        self.check_in_button = ttk.Button(
            content, text="Check In", command=self.check_in
        )
        self.check_in_button.pack(anchor="w", pady=(0, 20))

        ttk.Label(content, text="Welcome message", font=("Segoe UI", 11, "bold")).pack(
            anchor="w", pady=(0, 6)
        )
        self.output = tk.Text(
            content,
            height=12,
            wrap="word",
            font=("Segoe UI", 11),
            padx=12,
            pady=10,
            relief="solid",
            borderwidth=1,
            state="disabled",
        )
        self.output.pack(fill="both", expand=True)
        self._append_output(
            f"Welcome to the workshop!\nWorkshop date: {self.workshop_date}\n"
            "Enter your name above and select Check In."
        )
        self.name_entry.focus_set()

    def _append_output(self, message: str) -> None:
        self.output.configure(state="normal")
        if self.output.get("1.0", "end-1c"):
            self.output.insert("end", "\n\n")
        self.output.insert("end", message)
        self.output.see("end")
        self.output.configure(state="disabled")

    def check_in(self, event: tk.Event | None = None) -> str | None:
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning(
                "Name required", "Please enter a participant name before checking in."
            )
            self.name_entry.focus_set()
            return "break" if event is not None else None

        self._append_output(make_welcome_message(name, self.workshop_date))
        self.name_entry.delete(0, "end")
        self.name_entry.focus_set()
        return "break" if event is not None else None


def main() -> None:
    root = tk.Tk()
    WorkshopGreetingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()