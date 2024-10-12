import tkinter as tk

class SearchPopup(tk.Toplevel):
    """ A 'megawidget' for searching notes """

    def __init__(self, parent, notebook, **kwargs):
        super().__init__(parent, **kwargs) 

        self._notebook = notebook

        self._search_label = tk.Label(self, text="Search:")
        self._search_label.pack()
        self._search_entry = tk.Entry(self)
        self._search_entry.pack()

        self._enter_button = tk.Button(
            self, text="Enter", command=self._search_callback)
        self._enter_button.pack()

    def _search_callback(self):
        notes = self._notebook.search(self._search_entry.get())
        # could add better layout or functionality to clear this each time
        for note in notes:
            tk.Label(self, text=str(note)).pack()