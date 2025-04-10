import React, {useEffect, useState} from "react";
import axios from "axios";
import '../styles/TaskList.css'
function TaskList() {
    const [tasks, setTasks] = useState([]);

    useEffect( () => {
        axios.get("http://localhost:5000/tasks").then(res => {
            setTasks(res.data);
        });
    }, [])

    const toggleComplete = (id, completed) => {
        axios.put(`http://localhost:5000/tasks/${id}`, {completed: !completed}).then(() => {
            window.location.reload();
        });
    };

    const deleteTask = (id) => {
        axios.delete(`http://localhost:5000/tasks/${id}`).then(() => {
          window.location.reload();
        });
      };

      return (
        <table>
            <thead>
                <tr>
                    <th>Task</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {tasks.map(task => (
                    <tr key={task.id}>
                        <td
                            onClick={() => toggleComplete(task.id, task.completed)}
                            style={{ textDecoration: task.completed ? 'line-through' : 'none' }}
                            className={`task-list-item ${task.completed ? 'completed' : ''}`}
                        >
                            {task.title}
                        </td>
                        <td>
                            <button onClick={() => deleteTask(task.id)}>Delete</button>
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );    
}

export default TaskList;
