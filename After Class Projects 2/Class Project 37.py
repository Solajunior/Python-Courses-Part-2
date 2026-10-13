import tkinter as tk
from tkinter import ttk, messagebox


TASKS = [
    "Change out of school clothes",
    "Eat a healthy snack",
    "Finish all homework",
    "Practice reading or writing",
    "Take a short break and stretch",
    "Pack your school bag",
    "Set out tomorrow's clothes",
    "Clean up your desk and room",
]


class AfterSchoolRoutineChecker:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("After-School Routine Checker")
        self.root.geometry("700x560")
        self.root.minsize(620, 500)
        self.root.configure(bg="#f7f5f2")

        title = ttk.Label(
            root,
            text="After-School Routine",
            font=("Segoe UI", 22, "bold"),
            foreground="#2b3d55",
        )
        title.pack(pady=(20, 10))

        subtitle = ttk.Label(
            root,
            text="Check off each task you completed after school.",
            font=("Segoe UI", 11),
            foreground="#4b5872",
        )
        subtitle.pack(pady=(0, 10))

        self.check_vars = []
        self.task_frames = []

        for task in TASKS:
            var = tk.BooleanVar()
            frame = ttk.Frame(root, padding=(18, 8), style="Routine.TFrame")
            frame.pack(fill="x", padx=22)

            check = ttk.Checkbutton(
                frame,
                text=task,
                variable=var,
                style="Routine.TCheckbutton",
                command=self.update_progress,
            )
            check.pack(anchor="w")

            self.check_vars.append(var)
            self.task_frames.append(frame)

        self.progress_var = tk.StringVar(value="0/8 tasks complete")
        self.progress_label = ttk.Label(
            root,
            textvariable=self.progress_var,
            font=("Segoe UI", 11, "bold"),
            foreground="#1f5f5b",
        )
        self.progress_label.pack(pady=(16, 10))

        button_row = ttk.Frame(root)
        button_row.pack(pady=(0, 20))

        ttk.Button(button_row, text="Check My Routine", command=self.check_routine).pack(
            side="left", padx=8
        )
        ttk.Button(button_row, text="Reset", command=self.reset_routine).pack(
            side="left", padx=8
        )

        self.update_progress()

    def update_progress(self) -> None:
        done_count = sum(1 for var in self.check_vars if var.get())
        total = len(self.check_vars)
        self.progress_var.set(f"{done_count}/{total} tasks complete")

    def check_routine(self) -> None:
        done_count = sum(1 for var in self.check_vars if var.get())
        total = len(self.check_vars)

        if done_count == total:
            message = "Excellent! Your after-school routine is complete and you are all set for tomorrow."
        elif done_count >= 6:
            message = "Great job! You are almost done. A few more steps and your routine will be complete."
        elif done_count >= 4:
            message = "Nice work! Keep going and finish the remaining tasks to stay on track."
        else:
            message = "You're making progress. Try to complete the rest of your routine before bed."

        messagebox.showinfo("Routine Check", message)

    def reset_routine(self) -> None:
        for var in self.check_vars:
            var.set(False)
        self.update_progress()


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("Routine.TFrame", background="#f7f5f2")
    style.configure("Routine.TCheckbutton", font=("Segoe UI", 11), background="#f7f5f2")
    AfterSchoolRoutineChecker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
