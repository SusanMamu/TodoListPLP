import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function OTPPage() {
    const [otp, setOtp] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        setOtp(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/verifyotp/', { otp }); // Adjust the endpoint as per your backend
            // Assuming a successful OTP verification redirects to the dashboard
            navigate('/dashboard');
        } catch (error) {
            setError('Invalid OTP. Please try again.');
            console.error('OTP verification error:', error);
        }
    };

    return (
        <div className='main-container'>
            <h2>OTP Verification</h2>
            <form onSubmit={handleSubmit}>
                <div className='form-group'>
                    <label>Enter OTP</label>
                    <input
                        type="text"
                        name="otp"
                        value={otp}
                        onChange={handleChange}
                        maxLength="4"
                        pattern="\d{4}"
                        required
                        placeholder="1234"
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button className='submit-btn' type="submit">Verify OTP</button>
            </form>
        </div>
    );
}

export default OTPPage;
