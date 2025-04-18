import { useParams } from 'react-router-dom';
import { useEffect, useState } from 'react';
import axios from 'axios';

function EmailVerification() {
  const { token } = useParams();
  const [msg, setMsg] = useState('Verifying...');

  useEffect(() => {
    axios
      .get(`http://localhost:5000/auth/verify-email/${token}`)
      .then((res) => setMsg(res.data.msg))
      .catch((err) => setMsg(err.response?.data?.msg || 'Verification failed'));
  }, [token]);

  return (
    <div>
      <h2>Email Verification</h2>
      <p>{msg}</p>
    </div>
  );
}

export default EmailVerification;
