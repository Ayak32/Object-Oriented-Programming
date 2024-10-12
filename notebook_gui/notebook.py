from note import Note

class Notebook:
    """Represent a collection of notes that can be tagged,
    modified, and searched."""

    def __init__(self):
        """Initialize a notebook with an empty list."""
        self._notes = []
        self._last_id = 0

    def new_note(self, memo, tags=""):
        """Create a new note and add it to the list."""
        self._last_id += 1
        n = Note(memo, self._last_id, tags)
        self._notes.append(n)
        return n

    def _find_note(self, note_id):
        """Locate the note with the given id."""
        for note in self._notes:
            if note.id_matches(note_id):
                return note
        return None

    def modify_memo(self, note_id, memo):
        """Find the note with the given id and change its
        memo to the given value."""
        note = self._find_note(note_id)
        print(note)
        if note:
            note.update_memo(memo)
            return True
        return False

    def modify_tags(self, note_id, tags):
        """Find the note with the given id and change its
        tags to the given value."""
        note = self._find_note(note_id)
        if note:
            note.update_tags(tags)
            return True
        return False

    def search(self, filter):
        """Find all notes that match the given filter
        string."""
        return [note for note in self._notes if note.match(filter)]

    def all_notes(self):
        """Returns all notes in the notebook"""

        # could be sorted as below, or organized some other way
        return sorted(self._notes)