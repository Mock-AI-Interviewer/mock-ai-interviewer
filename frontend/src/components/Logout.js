import React from 'react';
import { Button } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const history = useNavigate();

    const handleLogout = async () => {
        try {
            await axios.post('http://localhost:8000/auth/jwt/logout');
            localStorage.removeItem('userEmail');
            history('/');
        } catch (error) {
            console.error('Error logging out', error);
        }
    };

    return (
        <Button variant="contained" color="secondary" onClick={handleLogout}>Logout</Button>
    );
}

export default Logout;
