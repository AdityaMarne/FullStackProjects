import React, { useState, useEffect } from 'react';
import axios from 'axios';
import PostItem from './PostItem';
import LoadingIndicator from './LoadingIndicator';
import MessageBox from './MessageBox';
import { Link } from 'react-router-dom';
import '../styles/blogPostList.css';

const BlogPostList = ({ token }) => {
    const [posts, setPosts] = useState([]);
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');
    const [sortOption, setSortOption] = useState('newest');

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await axios.get('http://localhost:5000/blog/all', {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                });
                setPosts(response.data);
            } catch (error) {
                setMessage(error.response?.data?.message || 'Error fetching posts');
            } finally {
                setLoading(false);
            }
        };

        fetchPosts();
    }, [token]);

    const handleDelete = async (postId) => {
        if (!window.confirm('Are you sure you want to delete this post?')) return;
        
        try {
            await axios.delete(`http://localhost:5000/blog/delete/${postId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setPosts(posts.filter((post) => post.id !== postId));
            setMessage('Post deleted successfully');
        } catch (error) {
            setMessage(error.response?.data?.message || 'Error deleting post');
        }
    };

    const handleFeature = async (postId) => {
        try {
            await axios.put(`http://localhost:5000/blog/feature/${postId}`, {}, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setMessage('Post featured successfully!');
            setPosts(
                posts.map(post =>
                    post.id === postId ? { ...post, featured: true } : post
                )
            );
        } catch (error) {
            setMessage(error.response?.data?.message || 'Error featuring post');
        }
    };

    const filteredPosts = posts.filter(post => 
        post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        post.content.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const sortedPosts = [...filteredPosts].sort((a, b) => {
        if (sortOption === 'newest') {
            return new Date(b.createdAt) - new Date(a.createdAt);
        } else if (sortOption === 'oldest') {
            return new Date(a.createdAt) - new Date(b.createdAt);
        } else if (sortOption === 'featured') {
            return (b.featured ? 1 : 0) - (a.featured ? 1 : 0);
        }
        return 0;
    });

    return (
        <div className="blog-post-list-container">
            <div className="blog-post-list-header">
                <h2 className="blog-post-list-title">Blog Posts</h2>
                <div className="controls">
                    <div className="search-container">
                        <input
                            type="text"
                            placeholder="Search posts..."
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                            className="search-input"
                        />
                    </div>
                    <div className="sort-container">
                        <select
                            value={sortOption}
                            onChange={(e) => setSortOption(e.target.value)}
                            className="sort-select"
                        >
                            <option value="newest">Newest First</option>
                            <option value="oldest">Oldest First</option>
                            <option value="featured">Featured First</option>
                        </select>
                    </div>
                    <Link to="/create" className="create-post-button">
                        Create New Post
                    </Link>
                </div>
            </div>

            {message && <MessageBox message={message} type={message.includes('success') ? 'success' : 'error'} />}

            {loading ? (
                <LoadingIndicator />
            ) : (
                <div className="post-list">
                    {sortedPosts.length > 0 ? (
                        sortedPosts.map((post) => (
                            <PostItem
                                key={post.id}
                                post={post}
                                onDelete={handleDelete}
                                onFeature={handleFeature}
                                token={token}
                            />
                        ))
                    ) : (
                        <div className="no-posts-message">
                            {searchTerm ? 'No posts match your search' : 'No posts available'}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default BlogPostList;