import React, {useState} from "react";
import axios from 'axios';
import '../styles/TaskForm.css'

function TaskForm(){
    const [title, setTitle] = useState("");

    const addTask = () => {
        axios.post('http://localhost:5000/tasks', {title}).then(() => {
            setTitle("");
            window.location.reload();
        });
    };

    return(
        <div>
            <input value={title} onChange={e => setTitle(e.target.value)}/>
            <button onClick={addTask}>Add</button>
        </div>
    );

}

export default TaskForm;