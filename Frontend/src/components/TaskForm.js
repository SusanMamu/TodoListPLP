import React, { useState } from 'react';
import axios from 'axios';
import { Paper, Stack, TextField, Typography, Button, MenuItem, Snackbar, Alert } from '@mui/material';

function AddTaskForm({ onClose }) {
    const [taskData, setTaskData] = useState({
        title: '',
        description: '',
        due_date: '',
        priority: 0,
        is_completed: false
    });

    const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setTaskData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/Tasks/', taskData); // Adjust the endpoint as per your backend
            if (response.data.status === 201) {
                setSnackbar({ open: true, message: 'Task added successfully', severity: 'success' });
                setTaskData({
                    title: '',
                    description: '',
                    due_date: '',
                    priority: 0,
                    is_completed: false
                });
                onClose();
            }
        } catch (error) {
            setSnackbar({ open: true, message: 'Error adding task', severity: 'error' });
            console.error('Error adding task:', error);
        }
    };

    const handleCloseSnackbar = () => {
        setSnackbar({ ...snackbar, open: false });
    };

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            minHeight: '100vh', // Full viewport height for central alignment
            padding: '50px', // Add some padding to avoid form touching the viewport edges
            boxSizing: 'border-box', // Ensure padding is included in the total width
        }}>
            <Paper style={{
                width: '50%',
                padding: '30px',
                borderRadius: '5px',
                marginBottom: '20px',
                maxHeight: '50vh', // Max height for the form
                overflowY: 'auto' // Scroll functionality
            }}>
                <form onSubmit={handleSubmit}>
                    <Stack spacing={2} sx={{ width: '100%' }}>
                        <Typography variant="h6" gutterBottom>
                            Add Task
                        </Typography>
                        <Typography variant="subtitle1" gutterBottom>
                            Title
                        </Typography>
                        <TextField
                            name="title"
                            placeholder="Title"
                            value={taskData.title}
                            onChange={handleChange}
                            fullWidth
                        />
                        <Typography variant="subtitle1" gutterBottom>
                            Description
                        </Typography>
                        <TextField
                            name="description"
                            placeholder="Description"
                            value={taskData.description}
                            onChange={handleChange}
                            fullWidth
                        />
                        <Typography variant="subtitle1" gutterBottom>
                            Due date
                        </Typography>
                        <TextField
                            type="date"
                            name="due_date"
                            value={taskData.due_date}
                            onChange={handleChange}
                            fullWidth
                        />
                        <Typography variant="subtitle1" gutterBottom>
                            Priority
                        </Typography>
                        <TextField
                            select
                            name="priority"
                            value={taskData.priority}
                            onChange={handleChange}
                            fullWidth
                        >
                            <MenuItem value={0}>Low</MenuItem>
                            <MenuItem value={1}>High</MenuItem>
                        </TextField>
                        <Typography variant="subtitle1" gutterBottom>
                            Status
                        </Typography>
                        <TextField
                            select
                            name="is_completed"
                            value={taskData.is_completed}
                            onChange={handleChange}
                            fullWidth
                        >
                            <MenuItem value={false}>Pending</MenuItem>
                            <MenuItem value={true}>Completed</MenuItem>
                        </TextField>
                    </Stack>
                    <Stack direction="row" spacing={2} sx={{ marginTop: '20px' }}>
                        <Button type="submit" variant="contained" color="primary" fullWidth>
                            Add Task
                        </Button>
                        <Button variant="outlined" color="secondary" fullWidth onClick={onClose}>
                            Cancel
                        </Button>
                    </Stack>
                </form>
            </Paper>
            <Snackbar
                open={snackbar.open}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
            >
                <Alert onClose={handleCloseSnackbar} severity={snackbar.severity} sx={{ width: '100%' }}>
                    {snackbar.message}
                </Alert>
            </Snackbar>
        </div>
    );
}

export default AddTaskForm;
