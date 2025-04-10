// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import './App.css'; // ⬅️ Import this at the top
import { useEffect, useState } from 'react';
import { fetchNotes, createNote, deleteNote } from './api';
import ReactMarkdown from 'react-markdown';

function App() {
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState({ title: '', content: '', color: '#ffffff' });

  useEffect(() => {
    fetchNotes().then(setNotes);
  }, []);

  const handleCreate = async () => {
    await createNote(newNote);
    setNewNote({ title: '', content: '', color: '#ffffff' });
    fetchNotes().then(setNotes);
  };

  const handleDelete = async (id) => {
    await deleteNote(id);
    fetchNotes().then(setNotes);
  };

  return (
    <div className="container">
      <h2>Create Note</h2>
      <input
        type="text"
        value={newNote.title}
        placeholder="Title"
        onChange={e => setNewNote({ ...newNote, title: e.target.value })}
      />
      <textarea
        rows="5"
        value={newNote.content}
        placeholder="Markdown Content"
        onChange={e => setNewNote({ ...newNote, content: e.target.value })}
      />
      <input
        type="color"
        value={newNote.color}
        onChange={e => setNewNote({ ...newNote, color: e.target.value })}
      />
      <br />
      <button onClick={handleCreate}>Add Note</button>

      <h2>Notes</h2>
      {notes.map(note => (
        <div className="note" key={note.id} style={{ backgroundColor: note.color }}>
          <h3>{note.title}</h3>
          <ReactMarkdown>{note.content}</ReactMarkdown>
          <button onClick={() => handleDelete(note.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}

export default App;
