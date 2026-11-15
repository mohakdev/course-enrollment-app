"""Course Enrollment Management System — Batch 3.

RA2511033010071 Mohak Jain
RA2511033010072 Riddhi Singhal
RA2511033010073 Keshav Agarwal
"""
import json
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

import customtkinter as ctk

DATA_FILE = Path(__file__).with_name("enrollments.json")
COURSES = ["B.Tech CSE", "B.Tech ECE", "B.Tech Mechanical", "B.Tech Civil",
           "BCA", "MCA", "B.Sc Data Science", "MBA"]
MODES = ["Regular", "Online"]
SEM_MIN, SEM_MAX = 1, 8

ACCENT = ("#4F46E5", "#6366F1")
ACCENT_HOVER = ("#4338CA", "#4F46E5")
DANGER = ("#DC2626", "#EF4444")
DANGER_HOVER = ("#B91C1C", "#DC2626")
CARD = ("#FFFFFF", "#1E1F26")
BG = ("#EEF0F6", "#14151A")
MUTED = ("#6B7280", "#9CA3AF")


class EnrollmentApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Course Enrollment Management System")
        self.geometry("1080x640")
        self.minsize(960, 580)
        self.configure(fg_color=BG)
        self.records = self.load()

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_form()
        self.build_records()
        self.build_status()
        self.refresh_list()

    # ---------- persistence ----------
    def load(self):
        try:
            return json.loads(DATA_FILE.read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save(self):
        DATA_FILE.write_text(json.dumps(self.records, indent=2))

    # ---------- layout ----------
    def build_header(self):
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=24, pady=(20, 8))
        bar.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(bar, text="Course Enrollment",
                     font=ctk.CTkFont(size=26, weight="bold")).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(bar, text="Maintain student course enrollment details",
                     text_color=MUTED, font=ctk.CTkFont(size=13)).grid(row=1, column=0, sticky="w")
        self.theme_switch = ctk.CTkSwitch(bar, text="Dark mode", command=self.toggle_theme,
                                          progress_color=ACCENT)
        self.theme_switch.grid(row=0, column=1, rowspan=2, sticky="e")
        if ctk.get_appearance_mode() == "Dark":
            self.theme_switch.select()

    def card(self, row, col, **grid):
        frame = ctk.CTkFrame(self, fg_color=CARD, corner_radius=16)
        frame.grid(row=row, column=col, sticky="nsew", **grid)
        return frame

    def build_form(self):
        form = self.card(1, 0, padx=(24, 12), pady=8)
        form.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(form, text="Student details",
                     font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, sticky="w", padx=24, pady=(22, 12))

        def field(row, label):
            ctk.CTkLabel(form, text=label, text_color=MUTED,
                         font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=row, column=0, sticky="w", padx=24, pady=(8, 2))

        field(1, "STUDENT ID *")
        self.id_entry = ctk.CTkEntry(form, height=38, width=300,
                     placeholder_text="e.g. RA2511033010071")
        self.id_entry.grid(row=2, column=0, sticky="ew", padx=24)

        field(3, "STUDENT NAME *")
        self.name_entry = ctk.CTkEntry(form, height=38,
                     placeholder_text="Full name")
        self.name_entry.grid(row=4, column=0, sticky="ew", padx=24)

        field(5, "COURSE NAME")
        self.course_var = tk.StringVar(value=COURSES[0])
        ctk.CTkOptionMenu(form, variable=self.course_var, values=COURSES, height=38,
                          fg_color=ACCENT, button_color=ACCENT_HOVER,
                          button_hover_color=ACCENT_HOVER).grid(row=6, column=0, sticky="ew", padx=24)

        field(7, f"SEMESTER ({SEM_MIN}–{SEM_MAX})")
        self.sem_entry = ctk.CTkEntry(form, height=38,
                     placeholder_text=f"{SEM_MIN} to {SEM_MAX}")
        self.sem_entry.grid(row=8, column=0, sticky="ew", padx=24)

        field(9, "STUDY MODE")
        self.mode_var = tk.StringVar(value=MODES[0])
        modes = ctk.CTkFrame(form, fg_color="transparent")
        modes.grid(row=10, column=0, sticky="w", padx=24, pady=(4, 0))
        for i, m in enumerate(MODES):
            ctk.CTkRadioButton(modes, text=m, value=m, variable=self.mode_var,
                               fg_color=ACCENT, hover_color=ACCENT_HOVER).grid(row=0, column=i, padx=(0, 24))

        buttons = ctk.CTkFrame(form, fg_color="transparent")
        buttons.grid(row=11, column=0, sticky="ew", padx=24, pady=(26, 22))
        buttons.grid_columnconfigure((0, 1), weight=1)
        btn = dict(height=40, corner_radius=10, font=ctk.CTkFont(size=14, weight="bold"))
        ctk.CTkButton(buttons, text="Enroll", command=self.enroll, fg_color=ACCENT,
                      hover_color=ACCENT_HOVER, **btn).grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=4)
        ctk.CTkButton(buttons, text="Update", command=self.update_record, fg_color=ACCENT,
                      hover_color=ACCENT_HOVER, **btn).grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=4)
        ctk.CTkButton(buttons, text="Delete", command=self.delete, fg_color=DANGER,
                      hover_color=DANGER_HOVER, **btn).grid(row=1, column=0, sticky="ew", padx=(0, 6), pady=4)
        ctk.CTkButton(buttons, text="Clear", command=self.clear_form, fg_color="transparent",
                      border_width=2, border_color=MUTED, text_color=("gray20", "gray85"),
                      hover_color=("gray90", "gray25"), **btn).grid(row=1, column=1, sticky="ew", padx=(6, 0), pady=4)

    def build_records(self):
        panel = self.card(1, 1, padx=(12, 24), pady=8)
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(3, weight=1)

        top = ctk.CTkFrame(panel, fg_color="transparent")
        top.grid(row=0, column=0, sticky="ew", padx=24, pady=(22, 12))
        top.grid_columnconfigure(0, weight=1)
        self.count_label = ctk.CTkLabel(top, text="", font=ctk.CTkFont(size=17, weight="bold"))
        self.count_label.grid(row=0, column=0, sticky="w")

        search = ctk.CTkFrame(panel, fg_color="transparent")
        search.grid(row=1, column=0, sticky="ew", padx=24)
        search.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(search, height=38, placeholder_text="Search by Student ID")
        self.search_entry.grid(row=0, column=0, sticky="ew")
        self.search_entry.bind("<Return>", lambda _e: self.search())
        ctk.CTkButton(search, text="Search", width=100, height=38, command=self.search,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER).grid(row=0, column=1, padx=(8, 0))
        ctk.CTkButton(search, text="Show all", width=90, height=38, command=self.show_all,
                      fg_color="transparent", border_width=2, border_color=MUTED,
                      text_color=("gray20", "gray85"), hover_color=("gray90", "gray25")).grid(row=0, column=2, padx=(8, 0))

        self.header_label = ctk.CTkLabel(panel, text=self.row_text("ID", "NAME", "COURSE", "SEM", "MODE"),
                                         font=ctk.CTkFont(family="Menlo", size=12, weight="bold"),
                                         text_color=MUTED, anchor="w")
        self.header_label.grid(row=2, column=0, sticky="ew", padx=(34, 24), pady=(16, 4))

        box = ctk.CTkFrame(panel, corner_radius=12, fg_color=("#F6F7FB", "#17181E"))
        box.grid(row=3, column=0, sticky="nsew", padx=24, pady=(0, 22))
        box.grid_columnconfigure(0, weight=1)
        box.grid_rowconfigure(0, weight=1)
        self.listbox = tk.Listbox(box, font=("Menlo", 12), borderwidth=0, highlightthickness=0,
                                  activestyle="none", exportselection=False)
        self.listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        scroll = ctk.CTkScrollbar(box, command=self.listbox.yview)
        scroll.grid(row=0, column=1, sticky="ns", pady=10, padx=(0, 6))
        self.listbox.configure(yscrollcommand=scroll.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.style_listbox()

    def build_status(self):
        self.status = ctk.CTkLabel(self, text="Ready", anchor="w", text_color=MUTED,
                                   font=ctk.CTkFont(size=12))
        self.status.grid(row=2, column=0, columnspan=2, sticky="ew", padx=28, pady=(4, 14))

    # ---------- helpers ----------
    @staticmethod
    def row_text(sid, name, course, sem, mode):
        return f"{sid[:17]:<18}{name[:20]:<21}{course[:18]:<19}{sem:<5}{mode}"

    def style_listbox(self):
        dark = ctk.get_appearance_mode() == "Dark"
        self.listbox.configure(
            bg="#17181E" if dark else "#F6F7FB",
            fg="#E5E7EB" if dark else "#1F2937",
            selectbackground=ACCENT[1] if dark else ACCENT[0],
            selectforeground="#FFFFFF")

    def toggle_theme(self):
        ctk.set_appearance_mode("dark" if self.theme_switch.get() else "light")
        self.style_listbox()

    def notify(self, msg, ok=True):
        self.status.configure(text=msg, text_color=("#059669", "#34D399") if ok else DANGER)

    def refresh_list(self, ids=None):
        self.listbox.delete(0, tk.END)
        self.visible_ids = sorted(self.records) if ids is None else ids
        for sid in self.visible_ids:
            r = self.records[sid]
            self.listbox.insert(tk.END, self.row_text(sid, r["name"], r["course"], str(r["semester"]), r["mode"]))
        n = len(self.records)
        self.count_label.configure(text=f"Enrollment records  ·  {n}")

    def validate(self):
        sid, name, sem = (e.get().strip() for e in (self.id_entry, self.name_entry, self.sem_entry))
        if not sid:
            return self.fail("Student ID is mandatory.")
        if not name:
            return self.fail("Student Name is mandatory.")
        if not all(c.isalpha() or c in " .'-" for c in name):
            return self.fail("Student Name can contain letters and spaces only.")
        if not sem.isdigit() or not SEM_MIN <= int(sem) <= SEM_MAX:
            return self.fail(f"Semester must be a whole number from {SEM_MIN} to {SEM_MAX}.")
        return sid.upper(), {"name": name.title(), "course": self.course_var.get(),
                             "semester": int(sem), "mode": self.mode_var.get()}

    def fail(self, msg):
        self.notify(msg, ok=False)
        messagebox.showerror("Invalid input", msg, parent=self)
        return None

    def set_entry(self, entry, text):
        entry.delete(0, tk.END)
        if text:
            entry.insert(0, text)
        else:
            self.focus_set()  # lets the placeholder reappear

    def fill_form(self, sid):
        r = self.records[sid]
        self.set_entry(self.id_entry, sid)
        self.set_entry(self.name_entry, r["name"])
        self.course_var.set(r["course"])
        self.set_entry(self.sem_entry, str(r["semester"]))
        self.mode_var.set(r["mode"])

    # ---------- operations ----------
    def enroll(self):
        result = self.validate()
        if not result:
            return
        sid, data = result
        if sid in self.records:
            return self.fail(f"{sid} is already enrolled. Use Update to change it.")
        self.records[sid] = data
        self.save()
        self.refresh_list()
        self.clear_form()
        self.notify(f"Enrolled {data['name']} ({sid}) in {data['course']}.")

    def search(self):
        sid = self.search_entry.get().strip().upper()
        if not sid:
            return self.fail("Enter a Student ID to search.")
        if sid not in self.records:
            self.refresh_list([])
            return self.notify(f"No enrollment found for {sid}.", ok=False)
        self.refresh_list([sid])
        self.listbox.selection_set(0)
        self.fill_form(sid)
        self.notify(f"Found {sid}.")

    def show_all(self):
        self.set_entry(self.search_entry, "")
        self.refresh_list()
        self.notify("Showing all records.")

    def update_record(self):
        result = self.validate()
        if not result:
            return
        sid, data = result
        if sid not in self.records:
            return self.fail(f"{sid} is not enrolled. Use Enroll first.")
        self.records[sid] = data
        self.save()
        self.refresh_list()
        self.notify(f"Updated enrollment for {sid}.")

    def delete(self):
        sid = self.id_entry.get().strip().upper()
        if not sid:
            return self.fail("Enter or select a Student ID to delete.")
        if sid not in self.records:
            return self.fail(f"{sid} is not enrolled.")
        if not messagebox.askyesno("Delete enrollment", f"Delete the enrollment for {sid}?", parent=self):
            return
        del self.records[sid]
        self.save()
        self.refresh_list()
        self.clear_form()
        self.notify(f"Deleted enrollment for {sid}.")

    def clear_form(self):
        for e in (self.id_entry, self.name_entry, self.sem_entry):
            self.set_entry(e, "")
        self.course_var.set(COURSES[0])
        self.mode_var.set(MODES[0])
        self.listbox.selection_clear(0, tk.END)

    def on_select(self, _event):
        sel = self.listbox.curselection()
        if sel:
            self.fill_form(self.visible_ids[sel[0]])


if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    EnrollmentApp().mainloop()
