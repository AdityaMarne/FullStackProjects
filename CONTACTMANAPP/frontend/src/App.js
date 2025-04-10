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

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ContactList from './components/ContactList';
import ContactForm from './components/ContactForm';
import SearchBar from './components/SearchBar';
import './App.css';

function App() {
  const [contacts, setContacts] = useState([]);
  const [editingContact, setEditingContact] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const fetchContacts = async () => {
    const res = await axios.get('http://localhost:5000/contacts');
    setContacts(res.data);
  };

  useEffect(() => {
    fetchContacts();
  }, []);

  const handleSearch = async (term) => {
    setSearchTerm(term);
    if (term === '') {
      fetchContacts();
    } else {
      const res = await axios.get(`http://localhost:5000/search?q=${term}`);
      setContacts(res.data);
    }
  };

  return (
    <div className="container">
      <h1>Contact Manager</h1>
      <SearchBar onSearch={handleSearch} />
      <ContactForm
        fetchContacts={fetchContacts}
        editingContact={editingContact}
        setEditingContact={setEditingContact}
      />
      <ContactList
        contacts={contacts}
        fetchContacts={fetchContacts}
        setEditingContact={setEditingContact}
      />
    </div>
  );
}

export default App;
