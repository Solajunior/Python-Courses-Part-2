import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk


class ReadingSchedulePlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Reading Schedule Planner")
        self.root.geometry("760x560")
        self.root.minsize(620, 440)
        self.root.configure(bg="#f4f6fb")
        self.schedule = []

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#4d6cfa", padx=22, pady=18)
        header.pack(fill="x")
        tk.Label(
            header, text="Reading Schedule Planner", bg="#4d6cfa", fg="white",
            font=("Arial", 20, "bold"),
        ).pack(anchor="w")
        tk.Label(
            header, text="Set a daily page goal and keep track of your progress.",
            bg="#4d6cfa", fg="#e8ecff", font=("Arial", 10),
        ).pack(anchor="w", pady=(4, 0))

        form = tk.Frame(self.root, bg="white", padx=18, pady=16)
        form.pack(fill="x", padx=16, pady=16)
        self.book_var = tk.StringVar()
        self.total_pages_var = tk.StringVar()
        self.pages_per_day_var = tk.StringVar(value="20")
        self.start_date_var = tk.StringVar(value=date.today().isoformat())
        fields = (
            ("Book title", self.book_var, 20),
            ("Total pages", self.total_pages_var, 12),
            ("Pages per day", self.pages_per_day_var, 12),
            ("Start date (YYYY-MM-DD)", self.start_date_var, 18),
        )
        for column, (label, variable, width) in enumerate(fields):
            field = tk.Frame(form, bg="white")
            field.grid(row=0, column=column, sticky="w", padx=(0, 12))
            tk.Label(
                field, text=label, bg="white", fg="#444b5c",
                font=("Arial", 9, "bold"),
            ).pack(anchor="w", pady=(0, 5))
            tk.Entry(field, textvariable=variable, width=width).pack(anchor="w")

        tk.Button(
            form, text="Create schedule", command=self.create_schedule,
            bg="#4d6cfa", fg="white", activebackground="#3e5de0",
            activeforeground="white", relief="flat", padx=14, pady=8,
            font=("Arial", 10, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=(14, 0))

        schedule_frame = tk.Frame(self.root, bg="white", padx=14, pady=12)
        schedule_frame.pack(fill="both", expand=True, padx=16, pady=(0, 12))
        self.summary_var = tk.StringVar(value="Your reading plan will appear here.")
        tk.Label(
            schedule_frame, textvariable=self.summary_var, bg="white",
            fg="#444b5c", font=("Arial", 10, "bold"), anchor="w",
        ).pack(fill="x", pady=(0, 10))

        table_frame = tk.Frame(schedule_frame, bg="white")
        table_frame.pack(fill="both", expand=True)
        self.schedule_table = ttk.Treeview(
            table_frame, columns=("date", "pages", "status"),
            show="headings", selectmode="extended",
        )
        self.schedule_table.heading("date", text="Reading date")
        self.schedule_table.heading("pages", text="Pages")
        self.schedule_table.heading("status", text="Progress")
        self.schedule_table.column("date", width=180, anchor="w")
        self.schedule_table.column("pages", width=220, anchor="w")
        self.schedule_table.column("status", width=140, anchor="center")
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.schedule_table.yview,
        )
        self.schedule_table.configure(yscrollcommand=scrollbar.set)
        self.schedule_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        actions = tk.Frame(self.root, bg="#f4f6fb")
        actions.pack(fill="x", padx=16, pady=(0, 16))
        tk.Button(
            actions, text="Toggle selected days complete",
            command=self.toggle_selected_days, relief="flat", padx=12, pady=8,
        ).pack(side="left")
        self.message_var = tk.StringVar(value="")
        tk.Label(
            actions, textvariable=self.message_var, bg="#f4f6fb",
            fg="#b23b3b", font=("Arial", 9),
        ).pack(side="left", padx=12)

    def create_schedule(self):
        title = self.book_var.get().strip()
        if not title:
            self.message_var.set("Enter a book title.")
            return

        try:
            total_pages = int(self.total_pages_var.get())
            pages_per_day = int(self.pages_per_day_var.get())
            start_date = date.fromisoformat(self.start_date_var.get().strip())
        except ValueError:
            self.message_var.set(
                "Use positive whole page counts and a valid YYYY-MM-DD date."
            )
            return
        if total_pages < 1 or pages_per_day < 1:
            self.message_var.set("Page counts must be greater than zero.")
            return

        self.schedule = []
        first_page = 1
        while first_page <= total_pages:
            last_page = min(first_page + pages_per_day - 1, total_pages)
            self.schedule.append({
                "date": start_date + timedelta(days=len(self.schedule)),
                "first_page": first_page,
                "last_page": last_page,
                "complete": False,
            })
            first_page = last_page + 1
        self.message_var.set("")
        self._refresh_schedule()

    def _refresh_schedule(self):
        for item in self.schedule_table.get_children():
            self.schedule_table.delete(item)
        for index, day in enumerate(self.schedule):
            self.schedule_table.insert(
                "", "end", iid=str(index),
                values=(
                    day["date"].strftime("%a, %b %d, %Y"),
                    f"Pages {day['first_page']}–{day['last_page']}",
                    "Complete" if day["complete"] else "To read",
                ),
            )

        if self.schedule:
            completed = sum(day["complete"] for day in self.schedule)
            self.summary_var.set(
                f"{self.book_var.get().strip()} · {completed} of "
                f"{len(self.schedule)} reading days complete"
            )
        else:
            self.summary_var.set("Your reading plan will appear here.")

    def toggle_selected_days(self):
        selected = self.schedule_table.selection()
        if not selected:
            self.message_var.set("Select one or more days in the schedule first.")
            return
        for item in selected:
            day = self.schedule[int(item)]
            day["complete"] = not day["complete"]
        self.message_var.set("")
        self._refresh_schedule()


def main():
    root = tk.Tk()
    ReadingSchedulePlanner(root)
    root.mainloop()


if __name__ == "__main__":
    main()