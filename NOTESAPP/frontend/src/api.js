const API_BASE = 'http://localhost:5000';

export async function fetchNotes() {
    const res = await fetch(`${API_BASE}/notes`);
    return res.json()
}

export async function createNote(note) {
    return fetch(`${API_BASE}/notes`,{
        method: 'POST',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(note)
    });
}

export async function updateNote(id, note) {
    return fetch(`${API_BASE}/note/${id}`,{
        method: 'PUT',
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(note)
    });
}

export async function deleteNote(id) {
    return fetch(`${API_BASE}/notes/${id}`,{
        method: 'DELETE'
    });
}
