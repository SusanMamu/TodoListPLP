import axios from 'axios';

// Set the base URL for the backend API
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1'
; // Adjust as needed

// Create an Axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Login function
export const login = async (credentials) => {
    const response = await api.post('/login', credentials);
    return response.data;
};

// Register function
export const register = async (userData) => {
    const response = await api.post('/register', userData);
    return response.data;
};

// Fetch tasks function
export const fetchTasks = async () => {
    const response = await api.get('/tasks');
    return response.data;
};

// Add task function
export const addTask = async (taskData) => {
    const response = await api.post('/tasks', taskData);
    return response.data;
};

// Update task function
export const updateTask = async (taskId, taskData) => {
    const response = await api.put(`/tasks/${taskId}`, taskData);
    return response.data;
};

// Delete task function
export const deleteTask = async (taskId) => {
    const response = await api.delete(`/tasks/${taskId}`);
    return response.data;
};
