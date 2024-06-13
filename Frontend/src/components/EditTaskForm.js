import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
    TextField, 
    Button, 
    Paper, 
    Typography, 
    Stack, 
    MenuItem, 
    Snackbar, 
    Alert 
} from '@mui/material';

const EditTaskForm = ({ taskId, onClose, onEditTask }) => {
    const [taskData, setTaskData] = useState({
        title: '',
        description: '',
        due_date: '',
        priority: 0,
        is_completed: false
    });
    const [snackbar, setSnackbar] = useState({
        open: false,
        message: '',
        severity: 'success'
    });

    useEffect(() => {
        fetchTaskData();
    }, [taskId]);

    const fetchTaskData = async () => {
        try {
            const response = await axios.get(`http://127.0.0.1:8000/api/v1/Tasks/${taskId}/`); // Adjust the endpoint as per your backend
            if (response.status === 200) {
                setTaskData(response.data);
            } else {
                setSnackbar({
                    open: true,
                    message: 'Error fetching task data',
                    severity: 'error'
                });
            }
        } catch (error) {
            console.error('Error fetching task data:', error);
            setSnackbar({
                open: true,
                message: 'Error fetching task data. Please try again later.',
                severity: 'error'
            });
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setTaskData((prevData) => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.put(`http://127.0.0.1:8000/api/v1/Tasks/${taskId}/`, taskData); // Adjust the endpoint as per your backend
            if (response.status === 200) {
                setSnackbar({
                    open: true,
                    message: 'Task updated successfully',
                    severity: 'success'
                });
                onEditTask();
                onClose();
            } else {
                setSnackbar({
                    open: true,
                    message: 'Error updating task',
                    severity: 'error'
                });
            }
        } catch (error) {
            console.error('Error updating task:', error);
            setSnackbar({
                open: true,
                message: 'Error updating task. Please try again later.',
                severity: 'error'
            });
        }
    };

    const handleCloseSnackbar = () => {
        setSnackbar((prev) => ({ ...prev, open: false }));
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
                            Edit Task
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
                            Update
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
};

export default EditTaskForm;
