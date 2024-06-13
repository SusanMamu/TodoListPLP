import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Registration from './components/Registration';
import Dashboard from './components/Dashboard';
import TaskForm from './components/TaskForm';
import EditTaskForm from './components/EditTaskForm';
import OTPPage from './components/OTPPage'; // Ensure this import is correct
import './index.css'

function App() {
    return (
        <Router>
            <Routes>
                <Route index path="/login" element={<Login />} />
                <Route path="/register" element={<Registration />} />
                <Route exact path="/" element={<Dashboard />} />
                <Route exact path="/add-task" element={<TaskForm />} />
                <Route exact path="/edit-task/:id" element={<EditTaskForm />} />
                <Route exact path="/otp-verification" element={<OTPPage />} /> {/* Added OTP verification route */}
            </Routes>
        </Router>
    );
}

export default App;
