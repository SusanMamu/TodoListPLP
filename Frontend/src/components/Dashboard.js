import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
    TableContainer, 
    Table, 
    TableHead, 
    TableBody, 
    TableRow, 
    TableCell, 
    Modal, 
    Paper, 
    Typography, 
    Box, 
    Button,
    Snackbar
} from '@material-ui/core';
import AddTaskForm from './TaskForm';
import EditTaskForm from './EditTaskForm';
import { Container } from '@mui/material';

function Dashboard() {
    const [open, setOpen] = useState(false);
    const [tasks, setTasks] = useState([]);
    const [successMessage, setSuccessMessage] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [editModalOpen, setEditModalOpen] = useState(false);
    const [taskIdToEdit, setTaskIdToEdit] = useState(null);

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/api/v1/Tasks/');  // Adjust the endpoint as per your backend
            if (response.data.status === 200) {
                setSuccessMessage(response.data.message);
                setErrorMessage('');
                setTasks(response.data.entity);
            } else {
                setErrorMessage(response.data.message);
                setSuccessMessage('');
            }
        } catch (error) {
            console.error('Error fetching tasks:', error);
            if (error.response) {
                const errorMessage = error.response.data.message || 'Internal Server Error';
                setErrorMessage(errorMessage);
            } else {
                setErrorMessage('Network error. Please try again later.');
            }
        }
    };

    const getCurrentGreeting = () => {
        const currentTime = new Date();
        const currentHour = currentTime.getHours();
        if (currentHour < 12) {
            return 'Good Morning';
        } else if (currentHour < 18) {
            return 'Good Afternoon';
        } else {
            return 'Good Evening';
        }
    };

    const handleOpen = () => {
        setOpen(true);
    };

    const handleCloseModal = () => {
        setOpen(false);
    };

    const handleCloseSnackbar = () => {
        setSnackbarOpen(false);
    };

    const handleAddTask = async (taskData) => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/Tasks/', taskData);  // Adjust the endpoint as per your backend
            if (response.data.status === 200) {
                setSnackbarMessage(response.data.message);
                setSnackbarOpen(true);
                fetchTasks();
            } else {
                setErrorMessage(response.data.message);
            }
        } catch (error) {
            console.error('Error adding task:', error);
            if (error.response) {
                const errorMessage = error.response.data.message || 'Internal Server Error';
                setErrorMessage(errorMessage);
            } else {
                setErrorMessage('Network error. Please try again later.');
            }
        }
    };

    const handleEdit = (id) => {
        setTaskIdToEdit(id);
        setEditModalOpen(true);
    };

    const handleEditTask = () => {
        fetchTasks();
    };

    const handleCloseEditModal = () => {
        setEditModalOpen(false);
    };

    const handleDelete = async (id) => {
        try {
            const response = await axios.delete(`http://127.0.0.1:8000/api/v1/Tasks/${id}/`);  // Adjust the endpoint as per your backend
            if (response.data.status === 200) {
                setSnackbarMessage(response.data.message);
                setSnackbarOpen(true);
                fetchTasks();
            } else {
                setErrorMessage(response.data.message);
            }
        } catch (error) {
            console.error('Error deleting task:', error);
            if (error.response) {
                const errorMessage = error.response.data.message || 'Internal Server Error';
                setErrorMessage(errorMessage);
            } else {
                setErrorMessage('Network error. Please try again later.');
            }
        }
    };

    const handleLogout = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/logout/');  // Adjust the endpoint as per your backend
            if (response.data.status === 200) {
                setSuccessMessage(response.data.message);
                setErrorMessage('');
                // Perform any additional logout actions like clearing local storage, resetting state, etc.
                // For example, redirecting to login page after successful logout:
                // history.push('/login');
            } else {
                setErrorMessage(response.data.message);
                setSuccessMessage('');
            }
        } catch (error) {
            console.error('Error logging out:', error);
            if (error.response) {
                const errorMessage = error.response.data.message || 'Internal Server Error';
                setErrorMessage(errorMessage);
            } else {
                setErrorMessage('Network error. Please try again later.');
            }
        }
    };

    return (
        <Container component='main'>
            <Typography variant='h5' style={{textAlign:'center', margin:'10px', fontWeight: 'bold'}}>{`${getCurrentGreeting()}, welcome!`}</Typography>
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={6000}
                onClose={handleCloseSnackbar}
                message={snackbarMessage}
            />
            <Box sx={{ width: '50%', height: '50%', p: 2,marginBottom:'10px' }}>
                <Box sx={{ display: 'flex',  justifyContent: 'flex-start' , alignItems: 'center', p: 2 }}>
                    <Button variant='contained' color='primary' onClick={handleOpen}>ADD TASK</Button>
                    
                    <Modal
                        sx={modalStyles} 
                        open={open}
                        onClose={handleCloseModal}
                        aria-labelledby="modal-modal-title"
                        aria-describedby="modal-modal-description"
                    >
                        <AddTaskForm onClose={handleCloseModal} onAddTask={handleAddTask} />
                    </Modal>
                </Box>
                <TableContainer style={{ display: 'flex', margin: 'auto', width: '70%', background: '#bfd9c0', marginBottom: '30px' }}>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell style={{ fontWeight: 'bold', textTransform: 'uppercase', background: ' rgb(42, 79, 211)', color: 'white' }}>Task Title</TableCell>
                                <TableCell style={{ fontWeight: 'bold', textTransform: 'uppercase', background: ' rgb(42, 79, 211)', color: 'white' }}>Description</TableCell>
                                <TableCell style={{ fontWeight: 'bold', textTransform: 'uppercase', background: ' rgb(42, 79, 211)', color: 'white' }}>Due Date</TableCell>
                                <TableCell style={{ fontWeight: 'bold', textTransform: 'uppercase', background: ' rgb(42, 79, 211)', color: 'white' }}>Priority</TableCell>
                                <TableCell style={{ fontWeight: 'bold', textTransform: 'uppercase', background: ' rgb(42, 79, 211)', color: 'white' }}>Status</TableCell>
                                <TableCell style={{ fontWeight: 'bold', textTransform: 'uppercase', background: ' rgb(42, 79, 211)', color: 'white' }}>Action</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {tasks.map((task) => (
                                <TableRow key={task.id}
                                sx={{ bgcolor: task.highlighted ? '#d4d4d4' : 'inherit', cursor: 'pointer' }}
                                hover
                            >
                                    <TableCell>{task.title}</TableCell>
                                    <TableCell>{task.description}</TableCell>
                                    <TableCell>{task.due_date}</TableCell>
                                    <TableCell>{task.priority === 0 ? 'Low' : 'High'}</TableCell>
                                    <TableCell>{task.is_completed ? 'Completed' : 'Pending'}</TableCell>
                                    <TableCell style={{ display: 'flex', gap: '0.2em' }}>
                                        <Button variant='contained' color='primary' onClick={() => handleEdit(task.id)}>Edit</Button>
                                        <Button variant='outlined' style={{ background: '#a8030e', color: '#fff' }} onClick={() => handleDelete(task.id)}>Delete</Button>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </TableContainer>
                <Container component='footer' sx={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    textAlign: 'center',
                    fontWeight: 'bold',
                    marginBottom: '20px'
                }}>
                    &copy;2024, Susan Mamu, Professional FullStack Developer
                </Container>
            </Box>
            <Modal
                sx={modalStyles}
                open={editModalOpen}
                onClose={handleCloseEditModal}
                aria-labelledby="edit-task-modal-title"
                aria-describedby="edit-task-modal-description"
            >
                <EditTaskForm taskId={taskIdToEdit} onClose={handleCloseEditModal} onEditTask={handleEditTask} />
            </Modal>
        </Container>

        
    );
}

const modalStyles = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    maxWidth: '50%',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

export default Dashboard;