import tkinter as tk
#from PIL import Image, ImageTk

from note_entry import NoteEntry



class NoteButton(tk.Frame):
    """ A custom widget that is associated with a Note object """

    def __init__(self, parent, note, **kwargs):
        super().__init__(parent, **kwargs) 
        self._note = note

        # At the moment there is only one button widget, so we could have
        # NoteButton extend tk.Button, but if you wanted to customize the
        # appearance further, for instance by adding this png of a note,
        # it would be useful being in a frame
        #photo = ImageTk.PhotoImage(Image.open("note.png"))
        self._edit_button = tk.Button(
            self, command=self._modify_note)
        self._edit_button.pack()
        self.update()


    def _modify_note(self):
        # self.master.master is the root in this case
        NoteEntry(self.master.master, self).grid(row=1, column=1)

    def update_memo(self, new_memo):
        "Update the memo on this NoteButton. Uses Note.update_memo behind the scenes."
        self._note.update_memo(new_memo)
        self.update()

    def update_tags(self, new_tags):
        "Update the tags on this NoteButton. Uses Note.update_tags behind the scenes."
        self._note.update_tags(new_tags)
        self.update()

    def update(self):
        """ Used to update this widget to display the current text of the
        associated note """
        self._edit_button.configure(text=str(self._note))

        