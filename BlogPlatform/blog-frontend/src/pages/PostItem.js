import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/postItem.css';

const PostItem = ({ post, onDelete, onFeature }) => {
    const formatDate = (dateString) => {
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const truncateContent = (content, maxLength = 150) => {
        if (content.length <= maxLength) return content;
        return content.substring(0, maxLength) + '...';
    };

    return (
        <div className={`post-card ${post.featured ? 'featured' : ''}`}>
            {post.featured && <div className="featured-badge">Featured</div>}
            
            <div className="post-header">
                <h3 className="post-title">{post.title}</h3>
                <div className="post-meta">
                    <span className="post-author">By {post.author}</span>
                    <span className="post-date">{formatDate(post.created_at)}</span>
                </div>
            </div>
            
            <p className="post-content">{truncateContent(post.content)}</p>
            
            <div className="post-actions">
            <Link to={`/edit/${post.id}`} className="button edit-button">
                Edit
            </Link>
                <button 
                    onClick={() => onFeature(post.id)} 
                    className="action-button feature-button"
                >
                    {post.featured ? 'Unfeature' : 'Feature'}
                </button>
                <button 
                    onClick={() => {
                        if (window.confirm('Are you sure you want to delete this post?')) {
                            onDelete(post.id);
                        }
                    }} 
                    className="action-button delete-button"
                >
                    Delete
                </button>
            </div>
        </div>
    );
};

export default PostItem;