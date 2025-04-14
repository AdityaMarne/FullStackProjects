import {useState} from 'react';
import axios from 'axios';

function ForgetPassword() {
    const [email, setEmail] = useState('');
    const [msg, setMsg] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            await axios.post('http://localhost:5000/auth/request-password-reset', { email });
            setMsg("If email exists, reset link sent.")
        }catch{
            setMsg("Something went wrong");
        }
    };

    return(
        <div>
            <h2>Forget Password</h2>
            <form onSubmit={handleSubmit}>
                <input type='email' placeholder='Enter your email' onChange={(e) => setEmail(e.target.value)} required/>
                <button type="submit">Send Reset Link</button>
            </form>
            <p>{msg}</p>
        </div>
    );
}

export default ForgetPassword;
