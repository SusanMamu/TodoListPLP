import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function RegistrationForm() {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        is_verified: true
    });

    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/users/', formData); // Adjust the endpoint as per your backend
            console.log('Registration successful:', response.data);
            // Redirect to login page after successful registration
            navigate('/login');
        } catch (error) {
            console.error('Registration failed:', error.response ? error.response.data : error.message);
            // Display error message to the user
        }
    };

    return (
        <div className='main-container'>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="username" placeholder="Username" value={formData.username} onChange={handleChange} required />
                <br></br>
                <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
                <br></br>
                <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
                <br></br>
                <input type="text" name="first_name" placeholder="First Name" value={formData.first_name} onChange={handleChange} />
                <br></br>
                <input type="text" name="last_name" placeholder="Last Name" value={formData.last_name} onChange={handleChange} />
                <br></br>
                <button className='submit-btn' type="submit">Register</button>
            </form>
        </div>
    );
}

export default RegistrationForm;
