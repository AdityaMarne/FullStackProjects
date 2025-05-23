import axios from 'axios';

const API = axios.create({
  baseURL: 'http://localhost:5000',
});

export const registerUser = (data) => API.post('/auth/register', data);
export const loginUser = (data) => API.post('/auth/login', data);
export const getProtected = (token) =>
  API.get('/auth/protected', {
    headers: { Authorization: `Bearer ${token}` },
  });
