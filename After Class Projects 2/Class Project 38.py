import tkinter as tk
from tkinter import messagebox, ttk


VALID_PIN = "1234"


class AtmPinChecker:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("ATM PIN Checker")
        self.root.geometry("420x330")
        self.root.minsize(380, 300)
        self.root.configure(bg="#f3f4f6")

        title = ttk.Label(
            root,
            text="ATM PIN Checker",
            font=("Segoe UI", 22, "bold"),
            foreground="#1f2937",
        )
        title.pack(pady=(24, 10))

        ttk.Label(
            root,
            text="Enter your 4-digit PIN:",
            font=("Segoe UI", 11, "bold"),
            foreground="#374151",
        ).pack(pady=(0, 8))

        self.pin_entry = ttk.Entry(root, show="*", font=("Segoe UI", 16), width=18)
        self.pin_entry.pack(pady=(0, 14))
        self.pin_entry.bind("<Return>", self.check_pin)

        self.check_button = ttk.Button(root, text="Check PIN", command=self.check_pin)
        self.check_button.pack(pady=(0, 12))

        ttk.Button(root, text="Clear", command=self.clear_pin).pack()

        self.status_var = tk.StringVar(value="")
        self.status_label = ttk.Label(
            root,
            textvariable=self.status_var,
            font=("Segoe UI", 10, "bold"),
            foreground="#1d4ed8",
            wraplength=300,
        )
        self.status_label.pack(pady=(18, 0))

        self.pin_entry.focus_set()

    def check_pin(self, event: tk.Event | None = None) -> str | None:
        pin = self.pin_entry.get().strip()

        if len(pin) != 4 or not pin.isdigit():
            self.status_var.set("PIN must be exactly 4 digits.")
            self.status_label.configure(foreground="#b91c1c")
            self.pin_entry.focus_set()
            return "break" if event is not None else None

        if pin == VALID_PIN:
            self.status_var.set("Access granted. Correct PIN!")
            self.status_label.configure(foreground="#15803d")
        else:
            self.status_var.set("Access denied. Wrong PIN.")
            self.status_label.configure(foreground="#b91c1c")

        self.pin_entry.delete(0, "end")
        self.pin_entry.focus_set()
        return "break" if event is not None else None

    def clear_pin(self) -> None:
        self.pin_entry.delete(0, "end")
        self.status_var.set("")
        self.pin_entry.focus_set()


def main() -> None:
    root = tk.Tk()
    AtmPinChecker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
