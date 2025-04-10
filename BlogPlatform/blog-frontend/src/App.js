// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;

import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import CreatePost from './pages/CreatePost';
import BlogPostList from './pages/BlogPostList';
import EditPost from './pages/UpdatePost';
import './App.css';

const NavBar = ({ setToken }) => (
  <nav className="navbar">
    <div className="navbar-brand">Blog App</div>
    <div className="navbar-links">
      <Link to="/posts" className="nav-link">View Posts</Link>
      <Link to="/create" className="nav-link">Create Post</Link>
      <button 
        className="logout-btn"
        onClick={() => { 
          setToken(null); 
          localStorage.removeItem('token'); 
        }}
      >
        Logout
      </button>
    </div>
  </nav>
);

const SideBar = () => (
  <aside className="sidebar">
    <h3>Menu</h3>
    <Link to="/create" className="sidebar-link">Create Post</Link>
    <Link to="/posts" className="sidebar-link">View Posts</Link>
  </aside>
);

const WelcomeScreen = () => (
  <div className="welcome-container">
    <h1>Welcome to the Blog App</h1>
    <p>Share your thoughts and ideas with the world</p>
    <div className="auth-buttons">
      <Link to="/register" className="auth-btn signup-btn">Sign Up</Link>
      <Link to="/login" className="auth-btn login-btn">Sign In</Link>
    </div>
  </div>
);

const App = () => {
  const [token, setToken] = useState(localStorage.getItem('token'));

  if (!token) {
    return (
      <Router>
        <div className="app">
          <Routes>
            <Route path="/" element={<WelcomeScreen />} />
            <Route path="/login" element={<Login setToken={setToken} />} />
            <Route path="/register" element={<Register setToken={setToken} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </Router>
    );
  }

  return (
    <Router>
      <div className="app">
        <NavBar setToken={setToken} />
        <div className="main-content">
          <SideBar />
          <div className="content">
            <Routes>
              <Route path="/" element={<Navigate to="/posts" />} />
              <Route path="/posts" element={<BlogPostList token={token} />} />
              <Route path="/create" element={<CreatePost token={token} />} />
              <Route path="/edit/:postId" element={<EditPost token={token} />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;