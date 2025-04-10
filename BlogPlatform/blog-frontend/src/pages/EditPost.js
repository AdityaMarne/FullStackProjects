import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, useNavigate } from 'react-router-dom';
import '../styles/editPost.css';

const EditPost = ({ token }) => {
    const { postId } = useParams();
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        title: '',
        content: ''
    });
    const [message, setMessage] = useState({ text: '', type: '' });
    const [isLoading, setIsLoading] = useState(true);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        const fetchPost = async () => {
            try {
                const { data } = await axios.get(`http://localhost:5000/blog/${postId}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setFormData({ title: data.title, content: data.content });
                setMessage({ text: '', type: '' });
            } catch (error) {
                setMessage({
                    text: error.response?.data?.message || 'Error fetching post',
                    type: 'error'
                });
            } finally {
                setIsLoading(false);
            }
        };

        fetchPost();
    }, [postId, token]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsSubmitting(true);

        try {
            const { data } = await axios.put(
                `http://localhost:5000/blog/update/${postId}`,
                formData,
                { headers: { Authorization: `Bearer ${token}` } }
            );
            
            setMessage({
                text: data.message || 'Post updated successfully!',
                type: 'success'
            });
            
            setTimeout(() => navigate('/posts'), 1500);
        } catch (error) {
            setMessage({
                text: error.response?.data?.message || 'Error updating post',
                type: 'error'
            });
        } finally {
            setIsSubmitting(false);
        }
    };

    if (isLoading) {
        return (
            <div className="edit-post-container">
                <div className="loading-spinner"></div>
            </div>
        );
    }

    return (
        <div className="edit-post-container">
            <div className="edit-post-card">
                <h2 className="edit-post-title">Edit Post</h2>
                
                {message.text && (
                    <div className={`alert-message ${message.type}`}>
                        {message.text}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="edit-post-form">
                    <div className="form-group">
                        <label htmlFor="title" className="form-label">Title</label>
                        <input
                            id="title"
                            type="text"
                            name="title"
                            value={formData.title}
                            onChange={handleChange}
                            className="form-input"
                            placeholder="Enter post title"
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label htmlFor="content" className="form-label">Content</label>
                        <textarea
                            id="content"
                            name="content"
                            value={formData.content}
                            onChange={handleChange}
                            className="form-textarea"
                            placeholder="Write your post content here..."
                            rows="10"
                            required
                        />
                    </div>
                    
                    <div className="form-actions">
                        <button 
                            type="submit" 
                            className="submit-button"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Updating...' : 'Update Post'}
                        </button>
                        <button 
                            type="button" 
                            className="cancel-button"
                            onClick={() => navigate('/posts')}
                            disabled={isSubmitting}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default EditPost;