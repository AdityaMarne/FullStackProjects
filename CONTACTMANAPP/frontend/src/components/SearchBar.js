import React from 'react';

function SearchBar({ onSearch }) {
  return (
    <input
      type="text"
      placeholder="Search contacts..."
      onChange={(e) => onSearch(e.target.value)}
      style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
    />
  );
}

export default SearchBar;
