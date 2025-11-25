"""
Smart Student Performance Analyzer (Capstone Project)
-----------------------------------------------------
Course: Problem Solving with Python (ETCCCPP103)
Program: BCA (AI & DS)

Description:
This script loads a CSV dataset of student marks, cleans and validates the data,
models students using OOP, performs statistical analysis, generates a 4-chart
dashboard using Matplotlib, and exports final reports (CSV + TXT).

Author: Ritik
Date: 25-11-2025
"""

# ------------------------------------------------------
# Import Library
# ------------------------------------------------------
import logging
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------------
# Setup logging
# ------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------------------
# Folder & File Paths
# ------------------------------------------------------
ROOT = Path.cwd()
DATA_DIR = ROOT / "data"
OUTPUT_DIR = ROOT / "output"

DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

SAMPLE_CSV = DATA_DIR / "sample_student_scores.csv"
CLEANED_CSV = OUTPUT_DIR / "cleaned_student_data.csv"
SUMMARY_CSV = OUTPUT_DIR / "student_summary.csv"
DASHBOARD_PNG = OUTPUT_DIR / "student_performance_dashboard.png"
SUMMARY_TXT = OUTPUT_DIR / "performance_summary.txt"


# ------------------------------------------------------
# Utility: Safe CSV Reader
# ------------------------------------------------------
def safe_read_csv(path: Path) -> pd.DataFrame:
    """Safely read a CSV file with error handling."""
    try:
        df = pd.read_csv(path)
        logging.info(f"Loaded data from: {path}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        raise
    except pd.errors.EmptyDataError:
        logging.error(f"File is empty: {path}")
        raise
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        raise


# ------------------------------------------------------
# Auto-generate sample dataset (for demo/grading)
# ------------------------------------------------------
def ensure_sample_data():
    """Create sample CSV only if it does not already exist."""
    if SAMPLE_CSV.exists():
        return

    sample = pd.DataFrame([
        {"Name": "Aman Kumar", "Roll_No": "23BCA001", "Gender": "M",
         "Subject": "Math", "Marks": 78, "Attendance": 92, "Semester": 1},
        {"Name": "Aman Kumar", "Roll_No": "23BCA001", "Gender": "M",
         "Subject": "Physics", "Marks": 72, "Attendance": 92, "Semester": 1},
        {"Name": "Aman Kumar", "Roll_No": "23BCA001", "Gender": "M",
         "Subject": "Chemistry", "Marks": 81, "Attendance": 92, "Semester": 1},

        {"Name": "Nisha Sharma", "Roll_No": "23BCA002", "Gender": "F",
         "Subject": "Math", "Marks": 88, "Attendance": 95, "Semester": 1},
        {"Name": "Nisha Sharma", "Roll_No": "23BCA002", "Gender": "F",
         "Subject": "Physics", "Marks": 91, "Attendance": 95, "Semester": 1},
        {"Name": "Nisha Sharma", "Roll_No": "23BCA002", "Gender": "F",
         "Subject": "Chemistry", "Marks": 85, "Attendance": 95, "Semester": 1},

        {"Name": "Ravi Verma", "Roll_No": "23BCA003", "Gender": "M",
         "Subject": "Math", "Marks": 54, "Attendance": 68, "Semester": 1},
        {"Name": "Ravi Verma", "Roll_No": "23BCA003", "Gender": "M",
         "Subject": "Physics", "Marks": 47, "Attendance": 68, "Semester": 1},
        {"Name": "Ravi Verma", "Roll_No": "23BCA003", "Gender": "M",
         "Subject": "Chemistry", "Marks": 50, "Attendance": 68, "Semester": 1},

        {"Name": "Priya Singh", "Roll_No": "23BCA004", "Gender": "F",
         "Subject": "Math", "Marks": 96, "Attendance": 98, "Semester": 1},
        {"Name": "Priya Singh", "Roll_No": "23BCA004", "Gender": "F",
         "Subject": "Physics", "Marks": 94, "Attendance": 98, "Semester": 1},
        {"Name": "Priya Singh", "Roll_No": "23BCA004", "Gender": "F",
         "Subject": "Chemistry", "Marks": 97, "Attendance": 98, "Semester": 1},
    ])

    sample.to_csv(SAMPLE_CSV, index=False)
    logging.info(f"Sample dataset created at {SAMPLE_CSV}")


# ------------------------------------------------------
# Student Class (OOP Model)
# ------------------------------------------------------
class Student:
    """Represents a student with subjects and marks."""

    def __init__(self, name: str, roll_no: str, gender: str = None):
        self.name = name
        self.roll_no = roll_no
        self.gender = gender
        self.marks: Dict[str, float] = {}

    def add_mark(self, subject: str, marks: float):
        self.marks[subject] = float(marks)

    def total(self) -> float:
        return sum(self.marks.values())

    def average(self) -> float:
        return self.total() / len(self.marks)

    def grade(self) -> str:
        avg = self.average()
        if avg >= 90: return "A+"
        if avg >= 80: return "A"
        if avg >= 70: return "B"
        if avg >= 60: return "C"
        if avg >= 50: return "D"
        return "F"

    def to_dict(self) -> Dict[str, float]:
        """Convert student data to a dictionary row for CSV export."""
        d = {
            "Name": self.name,
            "Roll_No": self.roll_no,
            "Gender": self.gender,
            "Total": self.total(),
            "Average": round(self.average(), 2),
            "Grade": self.grade(),
        }
        d.update({f"Mark_{sub}": m for sub, m in self.marks.items()})
        return d

    def __str__(self):
        return f"{self.roll_no} - {self.name} | Avg: {self.average():.2f} Grade: {self.grade()}"


# ------------------------------------------------------
# Student Manager (Handles data processing)
# ------------------------------------------------------
class StudentManager:
    """Loads CSV data, builds Student objects, computes statistics."""

    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.df: pd.DataFrame = pd.DataFrame()

    def load_csv(self, path: Path):
        """Load and clean the CSV dataset."""
        df = safe_read_csv(path)

        required_cols = {"Name", "Roll_No", "Subject", "Marks"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"CSV missing required columns: {required_cols}")

        if "Attendance" not in df.columns:
            df["Attendance"] = np.nan

        df["Marks"] = pd.to_numeric(df["Marks"], errors="coerce")
        df = df.dropna(subset=["Marks", "Name", "Roll_No", "Subject"])

        df = df[(df["Marks"] >= 0) & (df["Marks"] <= 100)]

        self.df = df.copy()
        logging.info("Dataset cleaned and stored successfully.")

    def build_students(self):
        """Create Student objects based on grouped dataset."""
        if self.df.empty:
            logging.error("No data loaded.")
            return

        grouped = self.df.groupby(["Roll_No", "Name"])

        for (roll, name), grp in grouped:
            gender = grp["Gender"].iloc[0] if "Gender" in grp else None
            student = Student(name, roll, gender)

            for _, row in grp.iterrows():
                student.add_mark(row["Subject"], row["Marks"])

            self.students[roll] = student

        logging.info(f"Built {len(self.students)} students.")

    def student_summary_df(self) -> pd.DataFrame:
        rows = [s.to_dict() for s in self.students.values()]
        df_summary = pd.DataFrame(rows)

        ordered_cols = ["Roll_No", "Name", "Gender"] + \
                       [c for c in df_summary.columns if c.startswith("Mark_")] + \
                       ["Total", "Average", "Grade"]

        return df_summary[ordered_cols]

    def top_bottom_performers(self, n=3) -> Tuple[List[Student], List[Student]]:
        sorted_students = sorted(self.students.values(),
                                 key=lambda s: s.average(), reverse=True)
        return sorted_students[:n], sorted_students[-n:]

    def subject_wise_stats(self) -> pd.DataFrame:
        if self.df.empty:
            return pd.DataFrame()

        stats = self.df.groupby("Subject")["Marks"].agg(
            ["mean", "min", "max", "std"]
        ).reset_index()

        stats.columns = ["Subject", "Mean", "Min", "Max", "StdDev"]
        return stats


# ------------------------------------------------------
# Visualization Dashboard (2×2 charts)
# ------------------------------------------------------
def create_dashboard(manager: StudentManager, out_path: Path = DASHBOARD_PNG):
    """Create a 4-chart dashboard and save as PNG."""
    df_summary = manager.student_summary_df()
    if df_summary.empty:
        logging.error("Cannot plot dashboard: No summary data.")
        return

    # Bar chart
    x = df_summary["Name"]
    y = df_summary["Average"]

    # Pie chart
    grade_counts = df_summary["Grade"].value_counts()

    # Line chart
    subject_stats = manager.subject_wise_stats()

    # Scatter (Attendance vs Average)
    att_df = manager.df.groupby("Roll_No")["Attendance"].mean().reset_index()
    merged = df_summary.merge(att_df, on="Roll_No", how="left")

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    plt.subplots_adjust(hspace=0.35, wspace=0.25)

    # 1 — Bar Chart
    axes[0, 0].bar(x, y)
    axes[0, 0].set_title("Average Marks by Student")
    axes[0, 0].set_ylabel("Average Marks")
    axes[0, 0].tick_params(axis="x", rotation=45)

    # 2 — Pie Chart
    axes[0, 1].pie(grade_counts.values, labels=grade_counts.index,
                    autopct="%1.1f%%", startangle=90)
    axes[0, 1].set_title("Grade Distribution")

    # 3 — Line Chart
    axes[1, 0].plot(subject_stats["Subject"], subject_stats["Mean"], marker="o")
    axes[1, 0].set_title("Subject-wise Average Marks")
    axes[1, 0].set_ylabel("Average")
    axes[1, 0].tick_params(axis="x", rotation=45)

    # 4 — Scatter Plot
    axes[1, 1].scatter(merged["Attendance"], merged["Average"])
    axes[1, 1].set_title("Attendance vs Average Marks")
    axes[1, 1].set_xlabel("Attendance (%)")
    axes[1, 1].set_ylabel("Average Marks")

    fig.suptitle("Student Performance Dashboard", fontsize=15)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(out_path)

    logging.info(f"Dashboard saved to {out_path}")


# ------------------------------------------------------
# Export Outputs
# ------------------------------------------------------
def export_outputs(manager: StudentManager):
    """Save cleaned CSV, summary CSV, and text report."""
    # Save cleaned data
    manager.df.to_csv(CLEANED_CSV, index=False)

    # Save summary table
    summary_df = manager.student_summary_df()
    summary_df.to_csv(SUMMARY_CSV, index=False)

    # Save text report
    top, bottom = manager.top_bottom_performers()

    class_avg = summary_df["Average"].mean()

    with open(SUMMARY_TXT, "w") as f:
        f.write("Performance Summary Report\n")
        f.write("============================\n")
        f.write(f"Total Students: {len(manager.students)}\n")
        f.write(f"Class Average: {class_avg:.2f}\n\n")

        f.write("Top Performers:\n")
        for s in top:
            f.write(f"- {s.roll_no} | {s.name} : {s.average():.2f}\n")

        f.write("\nBottom Performers:\n")
        for s in bottom:
            f.write(f"- {s.roll_no} | {s.name} : {s.average():.2f}\n")

    logging.info(f"Summary written to {SUMMARY_TXT}")


# ------------------------------------------------------
# CLI Menu
# ------------------------------------------------------
def run_cli():
    ensure_sample_data()
    manager = StudentManager()

    print("\nSmart Student Performance Analyzer\n---------------------------------\n")

    while True:
        print("\nMenu:")
        print("1. Load CSV dataset")
        print("2. Preview cleaned data")
        print("3. Build student objects")
        print("4. Show student summary table")
        print("5. Generate dashboard")
        print("6. Export all outputs")
        print("7. Quick Run (auto-load sample + process)")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                path_input = input(f"Enter CSV path (default: {SAMPLE_CSV}): ").strip()
                path = SAMPLE_CSV if path_input == "" else Path(path_input)
                manager.load_csv(path)
                print("Dataset loaded & cleaned.")

            elif choice == "2":
                if manager.df.empty:
                    print("Load data first.")
                else:
                    print(manager.df.head(10).to_string(index=False))

            elif choice == "3":
                manager.build_students()
                print("Built student objects.")

            elif choice == "4":
                if not manager.students:
                    print("Build students first.")
                else:
                    print(manager.student_summary_df().to_string(index=False))

            elif choice == "5":
                if not manager.students:
                    print("Build students first.")
                else:
                    create_dashboard(manager)
                    print(f"Dashboard saved to {DASHBOARD_PNG}")

            elif choice == "6":
                if manager.df.empty:
                    print("Load data first.")
                else:
                    export_outputs(manager)
                    print("All outputs exported.")

            elif choice == "7":
                manager.load_csv(SAMPLE_CSV)
                manager.build_students()
                export_outputs(manager)
                create_dashboard(manager)
                print("Quick run completed. Check output folder.")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            logging.exception("An error occurred.")


# ------------------------------------------------------
# Main Entry Point
# ------------------------------------------------------
if __name__ == "__main__":
    run_cli()
