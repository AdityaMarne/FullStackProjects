import React from 'react';
import axios from 'axios';

function ContactList({ contacts, fetchContacts, setEditingContact }) {
  const deleteContact = async (id) => {
    if (window.confirm('Are you sure you want to delete this contact?')) {
      await axios.delete(`http://localhost:5000/contacts/${id}`);
      fetchContacts();
    }
  };

  return (
    <table border="1" width="100%">
      <thead>
        <tr>
          <th>Name</th>
          <th>Phone</th>
          <th>Email</th>
          <th>Address</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {contacts.map(contact => (
          <tr key={contact.id}>
            <td>{contact.name}</td>
            <td>{contact.phone}</td>
            <td>{contact.email}</td>
            <td>{contact.address}</td>
            <td>
              <button onClick={() => setEditingContact(contact)}>Edit</button>
              <button onClick={() => deleteContact(contact.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default ContactList;
