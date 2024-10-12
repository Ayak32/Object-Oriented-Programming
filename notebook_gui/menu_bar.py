import tkinter as tk
import pickle
from note import Note
from note_button import NoteButton
from note_entry import NoteEntry
from notebook import Notebook
from search_popup import SearchPopup


class NotebookGUI:
    """Display a menu and respond to choices when run."""

    def __init__(self):

        self._window = tk.Tk()
        self._window.title("MY NOTEBOOK")
        self._window.geometry("500x200")

        self._notebook = Notebook()
        self._options_frame = tk.Frame(self._window)
        self._menu = tk.Menu(self._window)
        file_menu = tk.Menu(self._menu, tearoff=0)
        note_menu = tk.Menu(self._menu, tearoff=0)

        file_menu.add_command(label="Save", command=self._save)
        file_menu.add_command(label="Load", command=self._load)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self._window.quit)
        note_menu.add_command(label="Search Notes", command=self._search_notes)
        note_menu.add_command(label="Add Note", command=self._add_note)
        self._menu.add_cascade(label="File", menu=file_menu)
        self._menu.add_cascade(label="Notes", menu=note_menu)


        self._list_frame = tk.Frame(self._window)
        self._list_frame.grid(row=2, column=1, columnspan=1, sticky="w")

        self._window.config(menu=self._menu)
        self._window.mainloop()

    def _search_notes(self):
        SearchPopup(self._window, self._notebook)

    def _add_note(self):
        nb = NoteButton(self._list_frame, self._notebook.new_note(""))
        nb.grid(row=1, column=1)  # Use grid for NoteButton as well if you're using grid for NoteEntry
        NoteEntry(self._window, nb).grid(row=1, column=2)

        
    def _save(self):
        with open("notebook_save.pickle", "wb") as f:
            pickle.dump(self._notebook, f)

    def _load(self):
        with open("notebook_save.pickle", "rb") as f:
            self._notebook = pickle.load(f)

        notes = self._notebook.all_notes()
        
        self._list_frame.destroy()
        self._list_frame = tk.Frame(self._window)
        self._list_frame.grid(row=2, column=1, columnspan=1, sticky="w")
        for n in notes:
            NoteButton(self._list_frame, n).pack()


if __name__ == "__main__":
    NotebookGUI()


