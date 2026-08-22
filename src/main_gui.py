import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import csv

from capture import SpectrometerCapture
from calibrate import Calibration
from analysis import analyze_spectrum


class SpectrometerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spectrometer - Raspberry Pi")
        self.root.geometry("1000x760")
        self.root.minsize(900, 650)

        self.calibration = Calibration.load()
        self.capture = SpectrometerCapture()
        self.current_spectrum = []
        self.status = tk.StringVar(value="Ready")

        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self.root, bg="#3498db", height=78)
        header.pack(fill="x")
        tk.Label(
            header,
            text="🔬 RASPBERRY PI SPECTROMETER",
            font=("Arial", 24, "bold"),
            fg="white",
            bg="#3498db",
        ).pack(pady=20)

        nav = tk.Frame(self.root, bg="#34495e", height=90)
        nav.pack(fill="x", padx=0, pady=0)

        buttons = [
            ("📷 CAPTURE", "#2ecc71", self.capture_data),
            ("🔍 ANALYZE", "#e74c3c", self.analyze_data),
            ("⚙ CALIBRATE", "#f39c12", self.open_calibration),
            ("▣ EXPORT", "#9b59b6", self.export_csv),
        ]
        for text, color, command in buttons:
            tk.Button(
                nav, text=text, command=command,
                bg=color, fg="white", activebackground=color,
                font=("Arial", 13, "bold"), relief="raised",
                width=17, height=2
            ).pack(side="left", padx=12, pady=18)

        frame = tk.LabelFrame(
            self.root, text="SPECTRUM DATA",
            font=("Arial", 15, "bold"),
            padx=10, pady=10
        )
        frame.pack(fill="both", expand=True, padx=25, pady=18)

        columns = ("wavelength", "intensity", "frequency", "color")
        self.table = ttk.Treeview(frame, columns=columns, show="headings")
        headings = {
            "wavelength": "Wavelength (nm)",
            "intensity": "Intensity (%)",
            "frequency": "Frequency (THz)",
            "color": "Color",
        }
        widths = {"wavelength": 180, "intensity": 180, "frequency": 180, "color": 180}
        for col in columns:
            self.table.heading(col, text=headings[col])
            self.table.column(col, width=widths[col], anchor="center")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scroll.set)
        self.table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        bottom = tk.Frame(self.root, bg="#34495e")
        bottom.pack(fill="x")
        self.stats = tk.Label(
            bottom, text="Peaks: 0 | Max Intensity: 0%",
            bg="#34495e", fg="white", font=("Arial", 13)
        )
        self.stats.pack(pady=12)

        tk.Label(
            self.root, textvariable=self.status, anchor="w",
            bg="#95a5a6", fg="white", padx=12
        ).pack(fill="x")

    def capture_data(self):
        try:
            self.status.set("Capturing...")
            self.root.update_idletasks()
            frame = self.capture.capture_frame()
            self.current_spectrum = self.capture.frame_to_spectrum(frame)
            self.status.set("Capture complete")
            self._display_spectrum(self.current_spectrum)
        except Exception as exc:
            messagebox.showerror("Capture error", str(exc))
            self.status.set("Capture failed")

    def analyze_data(self):
        if not self.current_spectrum:
            self.capture_data()
            if not self.current_spectrum:
                return

        result = analyze_spectrum(
            self.current_spectrum,
            self.calibration.blue_wavelength,
            self.calibration.red_wavelength,
        )
        self.current_spectrum = result
        self._display_spectrum(result)
        max_intensity = max((r["intensity"] for r in result), default=0)
        self.stats.config(
            text=f"Peaks: {len(result)} | Max Intensity: {max_intensity:.0f}%"
        )
        self.status.set("Analysis complete")

    def _display_spectrum(self, rows):
        for item in self.table.get_children():
            self.table.delete(item)

        for row in rows:
            self.table.insert(
                "", "end",
                values=(
                    f'{row["wavelength"]:.0f}',
                    f'{row["intensity"]:.1f}',
                    f'{row["frequency"]:.1f}',
                    row["color"],
                ),
                tags=(row["color"].lower(),)
            )

        # Light background tint similar to the original UI.
        for tag, color in [
            ("blue", "#d8d6ff"),
            ("cyan", "#d6ffff"),
            ("green", "#c8ffc8"),
            ("yellow", "#ffffcc"),
            ("orange", "#ffe2b8"),
            ("red", "#ffd0d0"),
        ]:
            self.table.tag_configure(tag, background=color)

    def open_calibration(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Calibration")
        dialog.geometry("430x300")
        dialog.resizable(False, False)

        tk.Label(
            dialog, text="Calibration Settings",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        form = tk.Frame(dialog)
        form.pack(pady=5)

        tk.Label(form, text="Red wavelength (nm):").grid(row=0, column=0, padx=10, pady=10)
        red_var = tk.StringVar(value=str(self.calibration.red_wavelength))
        tk.Entry(form, textvariable=red_var, width=18).grid(row=0, column=1)

        tk.Label(form, text="Blue wavelength (nm):").grid(row=1, column=0, padx=10, pady=10)
        blue_var = tk.StringVar(value=str(self.calibration.blue_wavelength))
        tk.Entry(form, textvariable=blue_var, width=18).grid(row=1, column=1)

        def save():
            try:
                red = float(red_var.get())
                blue = float(blue_var.get())
                if red <= blue:
                    raise ValueError("Red wavelength must be greater than blue wavelength.")
                self.calibration = Calibration(red, blue)
                self.calibration.save()
                dialog.destroy()
                self.status.set("Calibration saved")
            except Exception as exc:
                messagebox.showerror("Calibration error", str(exc), parent=dialog)

        tk.Button(
            dialog, text="Save", command=save,
            bg="#27ae60", fg="white", font=("Arial", 11, "bold"),
            width=12
        ).pack(pady=25)

    def export_csv(self):
        if not self.current_spectrum:
            messagebox.showwarning("Export", "Analyze a spectrum first.")
            return

        path = filedialog.asksaveasfilename(
            title="Export spectrum",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")]
        )
        if not path:
            return

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Wavelength (nm)", "Intensity (%)", "Frequency (THz)", "Color"])
            for row in self.current_spectrum:
                writer.writerow([
                    f'{row["wavelength"]:.2f}',
                    f'{row["intensity"]:.2f}',
                    f'{row["frequency"]:.2f}',
                    row["color"],
                ])

        self.status.set(f"Exported: {Path(path).name}")
        messagebox.showinfo("Export", "Spectrum exported successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SpectrometerApp(root)
    root.mainloop()
