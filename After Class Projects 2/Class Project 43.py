from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox, ttk

import pandas as pd


BACKGROUND = "#f3f5f8"
INK = "#202b3c"
MUTED = "#65738a"
ACCENT = "#315e66"
GRADE_ORDER = ("A", "B", "C", "D", "E", "F")


@dataclass(frozen=True)
class MarksSummary:
    count: int
    average: float
    median: float
    highest: float
    lowest: float
    standard_deviation: float
    passed: int
    failed: int
    grades: dict[str, int]


def parse_marks(text: str) -> pd.Series:
    """Convert comma-separated marks into validated percentages."""
    entries = [entry.strip() for entry in text.split(",")]
    if not entries or any(not entry for entry in entries):
        raise ValueError("Enter marks separated by commas, such as 78, 92, 65.")

    marks = pd.to_numeric(pd.Series(entries), errors="coerce")
    if marks.isna().any():
        raise ValueError("Every mark must be a number.")

    if not marks.between(0, 100).all():
        raise ValueError("Each mark must be between 0 and 100.")
    return marks


def grade_for_mark(mark: float) -> str:
    if mark >= 90:
        return "A"
    if mark >= 80:
        return "B"
    if mark >= 70:
        return "C"
    if mark >= 60:
        return "D"
    if mark >= 50:
        return "E"
    return "F"


def analyze_marks(marks: pd.Series) -> MarksSummary:
    """Calculate class statistics and letter-grade counts."""
    if marks.empty:
        raise ValueError("Provide at least one mark.")
    if marks.isna().any() or not marks.between(0, 100).all():
        raise ValueError("Each mark must be a finite number between 0 and 100.")

    student_grades = marks.map(grade_for_mark)
    grades = {
        grade: int((student_grades == grade).sum())
        for grade in GRADE_ORDER
    }

    passed = int((marks >= 50).sum())
    return MarksSummary(
        count=int(marks.size),
        average=float(marks.mean()),
        median=float(marks.median()),
        highest=float(marks.max()),
        lowest=float(marks.min()),
        standard_deviation=float(marks.std(ddof=0)),
        passed=passed,
        failed=int(marks.size) - passed,
        grades=grades,
    )


class StudentMarksAnalyzer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Student Marks Analyzer")
        self.root.geometry("780x690")
        self.root.minsize(680, 600)
        self.root.configure(bg=BACKGROUND)

        self.summary_values = {
            "Students": tk.StringVar(),
            "Average": tk.StringVar(),
            "Median": tk.StringVar(),
            "Highest": tk.StringVar(),
            "Lowest": tk.StringVar(),
            "Std. deviation": tk.StringVar(),
            "Passed": tk.StringVar(),
            "Failed": tk.StringVar(),
        }
        self._configure_styles()
        self._build_ui()
        self._analyze()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.configure("Page.TFrame", background=BACKGROUND)
        style.configure("Title.TLabel", background=BACKGROUND, foreground=INK,
                        font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background=BACKGROUND, foreground=MUTED,
                        font=("Segoe UI", 10))
        style.configure("Card.TLabelframe", background="white", borderwidth=0)
        style.configure("Card.TLabelframe.Label", background="white", foreground=INK,
                        font=("Segoe UI", 11, "bold"))
        style.configure("Metric.TFrame", background="white")
        style.configure("MetricName.TLabel", background="white", foreground=MUTED,
                        font=("Segoe UI", 9))
        style.configure("MetricValue.TLabel", background="white", foreground=INK,
                        font=("Segoe UI", 14, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_ui(self) -> None:
        page = ttk.Frame(self.root, style="Page.TFrame", padding=(24, 20))
        page.pack(fill="both", expand=True)
        page.columnconfigure(0, weight=1)
        page.rowconfigure(4, weight=1)

        ttk.Label(page, text="Student Marks Analyzer", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            page,
            text="Enter marks as percentages to see class performance at a glance.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 16))

        input_card = ttk.LabelFrame(
            page, text="  Enter marks (0-100)  ", padding=14,
            style="Card.TLabelframe",
        )
        input_card.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        input_card.columnconfigure(0, weight=1)
        self.marks_entry = ttk.Entry(input_card, font=("Segoe UI", 10))
        self.marks_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.marks_entry.insert(0, "78, 92, 65, 48, 85, 73")
        self.marks_entry.bind("<Return>", lambda _event: self._analyze())
        ttk.Button(
            input_card, text="Analyze", style="Accent.TButton", command=self._analyze
        ).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(input_card, text="Clear", command=self._clear).grid(row=0, column=2)

        summary_card = ttk.LabelFrame(
            page, text="  Class summary  ", padding=14,
            style="Card.TLabelframe",
        )
        summary_card.grid(row=3, column=0, sticky="new", pady=(0, 14))
        for column in range(4):
            summary_card.columnconfigure(column, weight=1)
        for index, (name, value) in enumerate(self.summary_values.items()):
            row, column = divmod(index, 4)
            metric = ttk.Frame(summary_card, style="Metric.TFrame")
            metric.grid(row=row, column=column, sticky="ew", padx=6, pady=5)
            ttk.Label(metric, text=name, style="MetricName.TLabel").pack(anchor="w")
            ttk.Label(metric, textvariable=value, style="MetricValue.TLabel").pack(
                anchor="w", pady=(2, 0)
            )

        details_card = ttk.LabelFrame(
            page, text="  Individual results  ", padding=14,
            style="Card.TLabelframe",
        )
        details_card.grid(row=4, column=0, sticky="nsew")
        details_card.columnconfigure(0, weight=1)
        details_card.rowconfigure(0, weight=1)
        self.results = ttk.Treeview(
            details_card, columns=("student", "mark", "grade"), show="headings"
        )
        self.results.heading("student", text="Student")
        self.results.heading("mark", text="Mark (%)")
        self.results.heading("grade", text="Grade")
        self.results.column("student", width=120, anchor="w")
        self.results.column("mark", width=120, anchor="center")
        self.results.column("grade", width=100, anchor="center")
        self.results.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(details_card, orient="vertical",
                                  command=self.results.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.results.configure(yscrollcommand=scrollbar.set)
        self.grade_summary = tk.StringVar()
        ttk.Label(details_card, textvariable=self.grade_summary,
                  style="Subtitle.TLabel").grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

    def _analyze(self) -> None:
        try:
            marks = parse_marks(self.marks_entry.get())
            summary = analyze_marks(marks)
        except ValueError as error:
            messagebox.showerror("Invalid marks", str(error), parent=self.root)
            return

        values = {
            "Students": str(summary.count),
            "Average": f"{summary.average:.2f}%",
            "Median": f"{summary.median:.2f}%",
            "Highest": f"{summary.highest:g}%",
            "Lowest": f"{summary.lowest:g}%",
            "Std. deviation": f"{summary.standard_deviation:.2f}",
            "Passed": str(summary.passed),
            "Failed": str(summary.failed),
        }
        for name, value in values.items():
            self.summary_values[name].set(value)

        self.results.delete(*self.results.get_children())
        for index, mark in enumerate(marks, start=1):
            self.results.insert(
                "", "end",
                values=(f"Student {index}", f"{mark:g}", grade_for_mark(float(mark))),
            )
        self.grade_summary.set(
            "Grade distribution: "
            + "  |  ".join(f"{grade}: {summary.grades[grade]}" for grade in GRADE_ORDER)
        )

    def _clear(self) -> None:
        self.marks_entry.delete(0, tk.END)
        self.results.delete(*self.results.get_children())
        self.grade_summary.set("")
        for value in self.summary_values.values():
            value.set("")


def main() -> None:
    root = tk.Tk()
    StudentMarksAnalyzer(root)
    root.mainloop()


if __name__ == "__main__":
    main()