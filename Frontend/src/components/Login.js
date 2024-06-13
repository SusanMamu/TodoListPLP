import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';

function Login() {
    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/login/', formData); // Adjust the endpoint as per your backend
            // Store authentication token in local storage
            localStorage.setItem('token', response.data.token);
            // Redirect to OTP verification page
            navigate('/otp-verification');
        } catch (error) {
            console.error('Login error:', error);
            // Handle login error (e.g., display error message)
        }
    };

    return (
        <div className='main-container'>
            <h2 className='login-header'>Login</h2>
            <form onSubmit={handleSubmit}>
                <div className='form-group'>
                    <label>Username</label>
                    <input type="text" name="username" value={formData.username} onChange={handleChange} required />
                </div>
                <div className='form-group'>
                    <label>Password</label>
                    <input type="password" name="password" value={formData.password} onChange={handleChange} required />
                </div>
                <button className='submit-btn' type="submit">Login</button>
            </form>
            <p>Don't have an account? <Link className='register-link' to="/register">Register here</Link></p> {/* Link to the registration page */}
        </div>
    );
}

export default Login;
