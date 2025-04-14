import { useEffect, useState } from 'react';
import { getProtected } from '../api';

function Dashboard() {
  const [msg, setMsg] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) return setMsg('Not logged in');

    getProtected(token)
      .then((res) => setMsg(res.data.msg))
      .catch(() => setMsg('Unauthorized'));
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>{msg}</p>
    </div>
  );
}

export default Dashboard;
