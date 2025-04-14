import { useState } from "react";
import { loginUser } from "../api";

function Login(){
    const [form, setForm] = useState({email: '', password: ''});
    const [msg, setMsg] = useState('');

    const handleChange= (e) => setForm({...form, [e.target.name]: e.target.value});
    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const res = await loginUser(form);
            localStorage.setItem('token', res.data.access);
            setMsg('Login successful');
        }catch(err){
            setMsg(err.response?.data?.msg || 'Login Failed');
        }
    };

    return(
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input name = 'email' placeholder="Email" onChange={handleChange} required/>
                <input name = 'password' placeholder="Password" onChange={handleChange} required/>
                <button type="submit">Login</button>
            </form>
            <p>{msg}</p>
        </div>
    );
}

export default Login;
