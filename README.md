# Course Enrollment Management System

A desktop app for maintaining student course enrollment records. It's built with Python and [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter), and it stores data in a local JSON file.

**Batch 3:** Mohak Jain, Riddhi Singhal, Keshav Agarwal

## Features

- **Enroll** a student with an ID, name, course, semester and study mode
- **Update** an existing enrollment
- **Delete** an enrollment, after asking for confirmation
- **Search** by Student ID (press Enter or click Search), or **Show all** records
- **Click a record** in the list to load it into the form for editing
- **Light and dark mode**: follows the system theme, with a toggle in the header
- **Status bar** that shows a green message on success and a red one on error
- **Persistence**: every change is saved to `enrollments.json` right away

## Getting started

Requirements: Python 3.8+ with Tkinter. Tkinter comes with the python.org installers. On Linux you may need `sudo apt install python3-tk`.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

If `enrollments.json` doesn't exist, the app creates it the first time you save a record.

## Project structure

```
course-enrollment-app/
├── app.py              # The whole application: UI, validation, persistence
├── requirements.txt    # customtkinter>=5.2
└── enrollments.json    # Data file (created at runtime, git-ignored)
```

## How the code works

Everything lives in one class, `EnrollmentApp`, which extends `ctk.CTk`, the main window.

### Configuration (top of `app.py`)

| Constant | Purpose |
|---|---|
| `DATA_FILE` | Path to `enrollments.json`, next to `app.py` |
| `COURSES` | Courses offered in the drop-down (B.Tech CSE/ECE/Mechanical/Civil, BCA, MCA, B.Sc Data Science, MBA) |
| `MODES` | Study modes: `Regular` and `Online` |
| `SEM_MIN`, `SEM_MAX` | Allowed semester range (1–8) |
| `ACCENT`, `DANGER`, `CARD`, `BG`, `MUTED` | Colour pairs written as `(light, dark)`. CustomTkinter picks one based on the current theme |

To add a course, a mode or a semester, change these constants. The UI picks up the change on its own.

### Data model

Records are kept in memory as a dict keyed by Student ID, and saved to disk in exactly the same shape:

```json
{
  "RA2511033010071": {
    "name": "Mohak Jain",
    "course": "B.Tech CSE",
    "semester": 3,
    "mode": "Regular"
  }
}
```

- `load()` reads the file. It returns `{}` if the file is missing or corrupt.
- `save()` writes the whole dict back, indented. It runs after every enroll, update and delete.

### Layout

The window uses a 2-column, 3-row grid:

```
┌────────────────────────────────────────────────────────┐
│ Header: title, subtitle, dark-mode switch   (row 0)    │
├──────────────────────┬─────────────────────────────────┤
│ Form card (col 0)    │ Records card (col 1, stretches) │
│  - Student ID        │  - record count                 │
│  - Student Name      │  - search box + Search/Show all │
│  - Course (menu)     │  - column header                │
│  - Semester          │  - scrollable Listbox           │
│  - Mode (radio)      │                                 │
│  - Enroll / Update   │                                 │
│  - Delete / Clear    │                                 │
├──────────────────────┴─────────────────────────────────┤
│ Status bar                                  (row 2)    │
└────────────────────────────────────────────────────────┘
```

Each part is built by its own method: `build_header()`, `build_form()`, `build_records()` and `build_status()`. The `card()` helper makes the rounded panels.

The record list is a plain `tk.Listbox` with a monospace font (Menlo). `row_text()` cuts each field to a fixed width and pads it, so the columns line up. CustomTkinter doesn't theme a plain Tk widget, so `style_listbox()` sets the listbox colours by hand whenever the theme changes.

### Validation (`validate()`)

The form is checked before every enroll or update:

1. Student ID is required. It is stored in **upper case**.
2. Student Name is required and may contain only letters, spaces and `. ' -`. It is stored in **Title Case**.
3. Semester must be a whole number from `SEM_MIN` to `SEM_MAX`.

If a check fails, `fail()` shows an error dialog, turns the status bar red and returns `None`. If all checks pass, `validate()` returns `(student_id, record_dict)`.

### Operations

| Method | Button | Behaviour |
|---|---|---|
| `enroll()` | Enroll | Validates the form and refuses an ID that already exists. Then saves, refreshes the list and clears the form |
| `update_record()` | Update | Validates the form and refuses an ID that doesn't exist. Then saves and refreshes the list |
| `delete()` | Delete | Reads the ID from the form, asks for confirmation, then removes the record and saves |
| `search()` | Search / Enter | Shows only the matching record, selects it and fills the form |
| `show_all()` | Show all | Clears the search and lists every record, sorted by ID |
| `clear_form()` | Clear | Resets every field to its default |
| `on_select()` | (click a row) | Loads the selected record into the form |

`refresh_list(ids=None)` redraws the listbox. It keeps `self.visible_ids` in the same order as the rows, so `on_select()` can map a clicked row index back to a Student ID, even when a search has filtered the list.

### Small details

- `set_entry()` clears an entry before filling it. When it clears a field, it moves focus away so the placeholder text shows again.
- `notify()` sets the status bar text, green for success and red for an error.
- At startup the app calls `ctk.set_appearance_mode("system")`, so the theme follows the OS.

## Limitations and ideas

- All data is in one local JSON file, so there is no multi-user access or concurrency control. SQLite would be the natural next step.
- You can't change a Student ID in place. Delete the record and enroll it again under the new ID.
- Search only matches the exact Student ID. Searching by name or course would be a useful addition.
- The listbox font is hard-coded to Menlo, a macOS font. Other systems fall back to their default font, so the columns may not line up perfectly.
