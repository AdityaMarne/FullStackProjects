import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ContactForm({ fetchContacts, editingContact, setEditingContact }) {
  const [form, setForm] = useState({ name: '', phone: '', email: '', address: '' });

  useEffect(() => {
    if (editingContact) {
      setForm(editingContact);
    }
  }, [editingContact]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingContact) {
      await axios.put(`http://localhost:5000/contacts/${editingContact.id}`, form);
      setEditingContact(null);
    } else {
      await axios.post('http://localhost:5000/contacts', form);
    }
    setForm({ name: '', phone: '', email: '', address: '' });
    fetchContacts();
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
      <input name="name" placeholder="Name" value={form.name} onChange={handleChange} required />
      <input name="phone" placeholder="Phone" value={form.phone} onChange={handleChange} required />
      <input name="email" placeholder="Email" value={form.email} onChange={handleChange} required />
      <input name="address" placeholder="Address" value={form.address} onChange={handleChange} required />
      <button type="submit">{editingContact ? 'Update' : 'Add'} Contact</button>
    </form>
  );
}

export default ContactForm;
