import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import axios from 'axios';
import '../styles/updatePost.css';

const UpdatePost = ({ token }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const { postId } = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchPostData = async () => {
            setIsLoading(true);
            try {
                const response = await axios.get(`http://localhost:5000/blog/${postId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setTitle(response.data.title);
                setContent(response.data.content);
            } catch (error) {
                setMessage(error.response?.data?.message || 'Error fetching post data');
            } finally {
                setIsLoading(false);
            }
        };

        fetchPostData();
    }, [postId, token]);

    const handleUpdate = async (e) => {
        e.preventDefault();
        if (!title.trim() || !content.trim()) {
            setMessage('Title and content are required');
            return;
        }

        try {
            setIsLoading(true);
            await axios.put(
                `http://localhost:5000/blog/update/${postId}`,
                { title, content },
                { headers: { Authorization: `Bearer ${token}` } }
            );

            setMessage('Post updated successfully!');
            setTimeout(() => navigate('/posts'), 1500);
        } catch (error) {
            setMessage(error.response?.data?.message || 'Error updating post');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="update-post-container">
            <div className="update-post-card">
                <h2 className="update-post-title">Edit Post</h2>
                
                {isLoading && !title ? (
                    <div className="loading-indicator">Loading post data...</div>
                ) : (
                    <form onSubmit={handleUpdate} className="update-post-form">
                        <div className="form-group">
                            <label htmlFor="title" className="form-label">Title</label>
                            <input
                                id="title"
                                type="text"
                                value={title}
                                onChange={(e) => setTitle(e.target.value)}
                                className="form-input"
                                placeholder="Enter post title"
                                required
                            />
                        </div>
                        
                        <div className="form-group">
                            <label htmlFor="content" className="form-label">Content</label>
                            <textarea
                                id="content"
                                value={content}
                                onChange={(e) => setContent(e.target.value)}
                                className="form-textarea"
                                placeholder="Write your post content here..."
                                rows="10"
                                required
                            />
                        </div>
                        
                        <div className="form-actions">
                            <button 
                                type="submit" 
                                className="update-button"
                                disabled={isLoading}
                            >
                                {isLoading ? 'Updating...' : 'Update Post'}
                            </button>
                            <button 
                                type="button" 
                                className="cancel-button"
                                onClick={() => navigate('/posts')}
                                disabled={isLoading}
                            >
                                Cancel
                            </button>
                        </div>
                        
                        {message && (
                            <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
                                {message}
                            </div>
                        )}
                    </form>
                )}
            </div>
        </div>
    );
};

export default UpdatePost;