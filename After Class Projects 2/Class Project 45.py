import tkinter as tk
from tkinter import ttk

import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


BACKGROUND = "#f3f5f8"
INK = "#202b3c"
MUTED = "#65738a"
ACCENT = "#315e66"
STATUS_ORDER = ("Success", "Partial", "Failure", "Active")
CHART_TYPES = (
    "Launches over time",
    "Mission outcomes",
    "Missions by destination",
    "Duration by mission type",
)

MISSION_RECORDS = (
    ("Aster-01", 2002, "Asteria Labs", "Moon", "Orbiter", "Success", 420),
    ("Aster-02", 2003, "Asteria Labs", "Mars", "Lander", "Partial", 110),
    ("Aster-03", 2005, "Asteria Labs", "Mars", "Rover", "Success", 780),
    ("Aster-04", 2006, "Asteria Labs", "Venus", "Orbiter", "Success", 510),
    ("Aster-05", 2008, "Asteria Labs", "Jupiter", "Flyby", "Failure", 14),
    ("Aster-06", 2009, "Asteria Labs", "Moon", "Crewed", "Success", 12),
    ("Aster-07", 2011, "Asteria Labs", "Asteroid Belt", "Sample return", "Partial", 340),
    ("Aster-08", 2012, "Asteria Labs", "Mars", "Rover", "Success", 960),
    ("Aster-09", 2014, "Asteria Labs", "Jupiter", "Orbiter", "Active", 620),
    ("Aster-10", 2015, "Asteria Labs", "Moon", "Lander", "Success", 65),
    ("Aster-11", 2017, "Asteria Labs", "Venus", "Atmospheric probe", "Failure", 3),
    ("Aster-12", 2018, "Asteria Labs", "Mars", "Sample return", "Active", 480),
    ("Aster-13", 2020, "Asteria Labs", "Asteroid Belt", "Orbiter", "Success", 330),
    ("Aster-14", 2022, "Asteria Labs", "Moon", "Crewed", "Success", 18),
    ("Aster-15", 2024, "Asteria Labs", "Mars", "Lander", "Active", 95),
    ("Orbit-01", 2001, "Orbital Union", "Earth Orbit", "Telescope", "Success", 730),
    ("Orbit-02", 2004, "Orbital Union", "Moon", "Orbiter", "Success", 260),
    ("Orbit-03", 2007, "Orbital Union", "Mars", "Flyby", "Partial", 45),
    ("Orbit-04", 2010, "Orbital Union", "Earth Orbit", "Crewed", "Success", 180),
    ("Orbit-05", 2013, "Orbital Union", "Jupiter", "Flyby", "Success", 390),
    ("Orbit-06", 2016, "Orbital Union", "Moon", "Lander", "Failure", 8),
    ("Orbit-07", 2019, "Orbital Union", "Earth Orbit", "Telescope", "Active", 2100),
    ("Orbit-08", 2021, "Orbital Union", "Mars", "Rover", "Success", 510),
    ("Orbit-09", 2023, "Orbital Union", "Moon", "Crewed", "Active", 22),
    ("Orbit-10", 2025, "Orbital Union", "Asteroid Belt", "Sample return", "Active", 160),
    ("Deep-01", 2002, "Deep Space Directorate", "Jupiter", "Flyby", "Success", 35),
    ("Deep-02", 2005, "Deep Space Directorate", "Asteroid Belt", "Orbiter", "Failure", 72),
    ("Deep-03", 2009, "Deep Space Directorate", "Mars", "Lander", "Success", 190),
    ("Deep-04", 2012, "Deep Space Directorate", "Venus", "Atmospheric probe", "Partial", 6),
    ("Deep-05", 2015, "Deep Space Directorate", "Jupiter", "Orbiter", "Success", 840),
    ("Deep-06", 2018, "Deep Space Directorate", "Asteroid Belt", "Sample return", "Success", 690),
    ("Deep-07", 2020, "Deep Space Directorate", "Mars", "Rover", "Failure", 120),
    ("Deep-08", 2022, "Deep Space Directorate", "Jupiter", "Orbiter", "Active", 560),
    ("Deep-09", 2024, "Deep Space Directorate", "Venus", "Atmospheric probe", "Active", 11),
)


def create_mission_data() -> pd.DataFrame:
    """Return the bundled, fictional sample missions as a DataFrame."""
    columns = (
        "mission",
        "year",
        "agency",
        "destination",
        "mission_type",
        "status",
        "duration_days",
    )
    return pd.DataFrame(MISSION_RECORDS, columns=columns)


def filter_missions(
    missions: pd.DataFrame,
    agency: str = "All agencies",
    destination: str = "All destinations",
) -> pd.DataFrame:
    filtered = missions
    if agency != "All agencies":
        filtered = filtered[filtered["agency"] == agency]
    if destination != "All destinations":
        filtered = filtered[filtered["destination"] == destination]
    return filtered.copy()


def summarize_missions(missions: pd.DataFrame) -> tuple[int, str, str]:
    count = len(missions)
    completed = missions[missions["status"] != "Active"]
    if completed.empty:
        success_rate = "N/A"
    else:
        success_rate = f"{(completed['status'] == 'Success').mean():.0%}"
    if missions.empty:
        average_duration = "N/A"
    else:
        average_duration = f"{missions['duration_days'].mean():,.0f} days"
    return count, success_rate, average_duration


def draw_chart(axis, missions: pd.DataFrame, chart_type: str) -> None:
    axis.clear()
    axis.set_facecolor("white")
    if missions.empty:
        axis.text(
            0.5, 0.5, "No missions match these filters.",
            ha="center", va="center", color=MUTED, transform=axis.transAxes,
        )
        axis.set_axis_off()
        return

    axis.set_axis_on()
    if chart_type == "Launches over time":
        annual = missions.groupby("year", as_index=False).size()
        sns.lineplot(
            data=annual, x="year", y="size", marker="o",
            color=ACCENT, linewidth=2.5, ax=axis,
        )
        axis.set(xlabel="Launch year", ylabel="Missions", title="Launches over time")
    elif chart_type == "Mission outcomes":
        sns.countplot(
            data=missions, x="status", order=STATUS_ORDER,
            color=ACCENT, ax=axis,
        )
        axis.set(xlabel="", ylabel="Missions", title="Mission outcomes")
    elif chart_type == "Missions by destination":
        destination_counts = (
            missions.groupby("destination", as_index=False)
            .size()
            .sort_values("size", ascending=False)
        )
        sns.barplot(
            data=destination_counts, x="destination", y="size",
            color=ACCENT, ax=axis,
        )
        axis.set(xlabel="", ylabel="Missions", title="Missions by destination")
        axis.tick_params(axis="x", rotation=25)
    elif chart_type == "Duration by mission type":
        sns.boxplot(
            data=missions, x="mission_type", y="duration_days",
            color="#b9d1cc", ax=axis,
        )
        axis.set(xlabel="", ylabel="Duration (days)", title="Duration by mission type")
        axis.tick_params(axis="x", rotation=25)
    else:
        raise ValueError(f"Unknown chart type: {chart_type}")

    axis.grid(axis="y", color="#e8edf1c5", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right"]].set_visible(False)


class SpaceMissionDataExplorer:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Space Mission Data Explorer")
        self.root.geometry("1180x820")
        self.root.minsize(940, 700)
        self.root.configure(bg=BACKGROUND)

        self.missions = create_mission_data()
        self._configure_styles()
        self._build_ui()
        self._refresh_dashboard()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.configure("Page.TFrame", background=BACKGROUND)
        style.configure(
            "Title.TLabel", background=BACKGROUND, foreground=INK,
            font=("Segoe UI", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel", background=BACKGROUND, foreground=MUTED,
            font=("Segoe UI", 10),
        )
        style.configure("Card.TLabelframe", background="white", borderwidth=0)
        style.configure(
            "Card.TLabelframe.Label", background="white", foreground=INK,
            font=("Segoe UI", 11, "bold"),
        )
        style.configure("Metric.TFrame", background="white")
        style.configure(
            "MetricName.TLabel", background="white", foreground=MUTED,
            font=("Segoe UI", 9),
        )
        style.configure(
            "MetricValue.TLabel", background="white", foreground=INK,
            font=("Segoe UI", 16, "bold"),
        )
        style.configure("Treeview", rowheight=25, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))

    def _build_ui(self) -> None:
        page = ttk.Frame(self.root, style="Page.TFrame", padding=(22, 18))
        page.pack(fill="both", expand=True)
        page.columnconfigure(0, weight=1)

        ttk.Label(page, text="Space Mission Data Explorer", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            page,
            text="Explore mission outcomes, destinations, launch years, and durations.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(3, 5))
        ttk.Label(
            page,
            text="Demo dataset: fictional sample records for learning and visualization.",
            style="Subtitle.TLabel",
        ).grid(row=2, column=0, sticky="w", pady=(0, 14))

        self._build_controls(page)
        self._build_metrics(page)
        self._build_content(page)

    def _build_controls(self, page: ttk.Frame) -> None:
        controls = ttk.LabelFrame(
            page, text="  Filters and chart  ", padding=12,
            style="Card.TLabelframe",
        )
        controls.grid(row=3, column=0, sticky="ew", pady=(0, 12))
        controls.columnconfigure(1, weight=1)
        controls.columnconfigure(3, weight=1)
        controls.columnconfigure(5, weight=2)

        ttk.Label(controls, text="Agency").grid(row=0, column=0, sticky="w", padx=(0, 7))
        self.agency_var = tk.StringVar(value="All agencies")
        self.agency_picker = ttk.Combobox(
            controls,
            textvariable=self.agency_var,
            values=("All agencies", *sorted(self.missions["agency"].unique())),
            state="readonly",
        )
        self.agency_picker.grid(row=0, column=1, sticky="ew", padx=(0, 16))
        self.agency_picker.bind("<<ComboboxSelected>>", self._on_filter_change)

        ttk.Label(controls, text="Destination").grid(
            row=0, column=2, sticky="w", padx=(0, 7)
        )
        self.destination_var = tk.StringVar(value="All destinations")
        self.destination_picker = ttk.Combobox(
            controls,
            textvariable=self.destination_var,
            values=("All destinations", *sorted(self.missions["destination"].unique())),
            state="readonly",
        )
        self.destination_picker.grid(row=0, column=3, sticky="ew", padx=(0, 16))
        self.destination_picker.bind("<<ComboboxSelected>>", self._on_filter_change)

        ttk.Label(controls, text="View").grid(row=0, column=4, sticky="w", padx=(0, 7))
        self.chart_var = tk.StringVar(value=CHART_TYPES[0])
        self.chart_picker = ttk.Combobox(
            controls, textvariable=self.chart_var, values=CHART_TYPES, state="readonly"
        )
        self.chart_picker.grid(row=0, column=5, sticky="ew", padx=(0, 12))
        self.chart_picker.bind("<<ComboboxSelected>>", self._on_filter_change)
        ttk.Button(controls, text="Reset", command=self._reset_filters).grid(
            row=0, column=6, sticky="e"
        )

    def _build_metrics(self, page: ttk.Frame) -> None:
        metrics = ttk.Frame(page, style="Page.TFrame")
        metrics.grid(row=4, column=0, sticky="ew", pady=(0, 12))
        for column in range(3):
            metrics.columnconfigure(column, weight=1)

        self.metric_values = {
            "Missions shown": tk.StringVar(),
            "Success rate": tk.StringVar(),
            "Average duration": tk.StringVar(),
        }
        for column, (name, value) in enumerate(self.metric_values.items()):
            card = ttk.LabelFrame(
                metrics, text=f"  {name}  ", padding=(14, 8),
                style="Card.TLabelframe",
            )
            card.grid(row=0, column=column, sticky="ew", padx=(0, 8))
            ttk.Label(
                card, textvariable=value, style="MetricValue.TLabel"
            ).pack(anchor="w")

    def _build_content(self, page: ttk.Frame) -> None:
        content = ttk.Frame(page, style="Page.TFrame")
        content.grid(row=5, column=0, sticky="nsew")
        page.rowconfigure(5, weight=1)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=2)
        content.rowconfigure(0, weight=1)

        chart_card = ttk.LabelFrame(
            content, text="  Mission analysis  ", padding=10,
            style="Card.TLabelframe",
        )
        chart_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self.figure = Figure(figsize=(7.0, 4.7), dpi=100, facecolor="white")
        self.axis = self.figure.add_subplot(111)
        self.figure_canvas = FigureCanvasTkAgg(self.figure, master=chart_card)
        self.figure_canvas.get_tk_widget().pack(fill="both", expand=True)

        table_card = ttk.LabelFrame(
            content, text="  Filtered missions  ", padding=10,
            style="Card.TLabelframe",
        )
        table_card.grid(row=0, column=1, sticky="nsew")
        table_card.columnconfigure(0, weight=1)
        table_card.rowconfigure(0, weight=1)
        columns = ("mission", "year", "destination", "status")
        self.mission_table = ttk.Treeview(
            table_card, columns=columns, show="headings", selectmode="browse"
        )
        for column, title, width in (
            ("mission", "Mission", 85),
            ("year", "Year", 55),
            ("destination", "Destination", 115),
            ("status", "Status", 75),
        ):
            self.mission_table.heading(column, text=title)
            self.mission_table.column(column, width=width, anchor="w")
        self.mission_table.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            table_card, orient="vertical", command=self.mission_table.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.mission_table.configure(yscrollcommand=scrollbar.set)

    def _on_filter_change(self, _event: tk.Event) -> None:
        self._refresh_dashboard()

    def _reset_filters(self) -> None:
        self.agency_var.set("All agencies")
        self.destination_var.set("All destinations")
        self.chart_var.set(CHART_TYPES[0])
        self._refresh_dashboard()

    def _refresh_dashboard(self) -> None:
        filtered = filter_missions(
            self.missions, self.agency_var.get(), self.destination_var.get()
        )
        count, success_rate, average_duration = summarize_missions(filtered)
        self.metric_values["Missions shown"].set(str(count))
        self.metric_values["Success rate"].set(success_rate)
        self.metric_values["Average duration"].set(average_duration)

        draw_chart(self.axis, filtered, self.chart_var.get())
        self.figure.tight_layout()
        self.figure_canvas.draw_idle()

        self.mission_table.delete(*self.mission_table.get_children())
        for mission in filtered.itertuples(index=False):
            self.mission_table.insert(
                "",
                "end",
                values=(mission.mission, mission.year, mission.destination, mission.status),
            )


def main() -> None:
    sns.set_theme(style="whitegrid", palette="deep")
    root = tk.Tk()
    SpaceMissionDataExplorer(root)
    root.mainloop()


if __name__ == "__main__":
    main()