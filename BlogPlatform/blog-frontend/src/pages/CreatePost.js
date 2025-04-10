import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../styles/createPost.css';

const CreatePost = ({ token }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [tags, setTags] = useState([]);
    const [selectedTags, setSelectedTags] = useState([]);
    const [newTag, setNewTag] = useState('');
    const [message, setMessage] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchTags = async () => {
            try {
                const response = await axios.get('http://localhost:5000/tags/all', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                setTags(response.data);
            } catch (error) {
                setMessage('Error fetching tags');
            }
        };

        fetchTags();
    }, [token]);

    const handleTagSelect = (tagId) => {
        if (selectedTags.includes(tagId)) {
            setSelectedTags(selectedTags.filter(id => id !== tagId));
        } else {
            setSelectedTags([...selectedTags, tagId]);
        }
    };

    const handleNewTag = async () => {
        if (!newTag.trim()) {
            setMessage('Tag name cannot be empty');
            return;
        }

        try {
            setIsLoading(true);
            const response = await axios.post(
                'http://localhost:5000/tags/create', 
                { name: newTag },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            setMessage(response.data.message);
            setNewTag('');
            
            const updatedTags = await axios.get('http://localhost:5000/tags/all', {
                headers: { Authorization: `Bearer ${token}` }
            });
            setTags(updatedTags.data);
        } catch (error) {
            setMessage(error.response?.data?.message || 'Error creating new tag');
        } finally {
            setIsLoading(false);
        }
    };

    const handleCreate = async (e) => {
        e.preventDefault();
        if (!title.trim() || !content.trim()) {
            setMessage('Title and content are required');
            return;
        }

        try {
            setIsLoading(true);
            const response = await axios.post('http://localhost:5000/blog/create', {
                title,
                content,
                tags: selectedTags
            }, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            setMessage(response.data.message);
            // Clear form on successful creation
            setTitle('');
            setContent('');
            setSelectedTags([]);
        } catch (error) {
            setMessage(error.response?.data?.message || 'Error creating post');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="create-post-container">
            <div className="create-post-card">
                <h2 className="create-post-title">Create New Post</h2>
                
                <form onSubmit={handleCreate} className="create-post-form">
                    <div className="form-group">
                        <label htmlFor="title" className="form-label">Post Title</label>
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
                            rows="8"
                            required
                        />
                    </div>
                    
                    <div className="form-group">
                        <label className="form-label">Tags</label>
                        <div className="tags-container">
                            {tags.map((tag) => (
                                <label key={tag.id} className="tag-item">
                                    <input
                                        type="checkbox"
                                        checked={selectedTags.includes(tag.id)}
                                        onChange={() => handleTagSelect(tag.id)}
                                        className="tag-checkbox"
                                    />
                                    <span className="tag-name">{tag.name}</span>
                                </label>
                            ))}
                        </div>
                        
                        <div className="new-tag-container">
                            <label className="form-label">Create New Tag</label>
                            <div className="new-tag-input-group">
                                <input
                                    type="text"
                                    value={newTag}
                                    onChange={(e) => setNewTag(e.target.value)}
                                    className="form-input"
                                    placeholder="Enter new tag name"
                                />
                                <button 
                                    type="button" 
                                    onClick={handleNewTag}
                                    className="tag-button"
                                    disabled={isLoading}
                                >
                                    {isLoading ? 'Adding...' : 'Add Tag'}
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <button 
                        type="submit" 
                        className="create-post-button"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Publishing...' : 'Publish Post'}
                    </button>
                    
                    {message && (
                        <div className={`message ${message.includes('success') ? 'success' : 'error'}`}>
                            {message}
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
};

export default CreatePost;