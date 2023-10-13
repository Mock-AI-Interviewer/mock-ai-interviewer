import React, { useState } from "react";
import { Button, TextField, Container } from "@mui/material";
import axios from "axios";
import Cookies from 'js-cookie';
import { BASE_API_ENDPOINT } from "../config";
import TopAppBar from '../components/TopAppBar'; // Import the TopAppBar component
import SuccessMessage from "../components/SuccessMessage";
import ErrorMessage from "../components/ErrorMessage";
import HomeButton from "../components/HomeButton";

function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleLogin = async () => {
        setError(null);
        setSuccess(null);
        try {
            const response = await axios.post(`${BASE_API_ENDPOINT}/auth/jwt/login`, `username=${email}&password=${password}`, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            if(response.status === 204) {
                setSuccess('Login successful!');
            }
        } catch (error) {
            setError(error.message);
            console.error(error);
        }
    };

    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="md" style={{ marginTop: '8%' }}>
                <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundColor: '#f7f7f7', padding: '20px', borderRadius: '10px' }}>
                    <h1>Login</h1>
                    <TextField label="Email" variant="outlined" margin="normal" fullWidth onChange={e => setEmail(e.target.value)} />
                    <TextField label="Password" variant="outlined" margin="normal" fullWidth type="password" onChange={e => setPassword(e.target.value)} />
                    <Button variant="contained" color="primary" onClick={handleLogin}>Login</Button>
                </div>
                {error && <ErrorMessage message={error} style={{ marginTop: '20px' }} />}
                {success && <SuccessMessage message={success} />} {/* Display the success message when present */}
            </Container>
        </>
    );
}

export default LoginPage;
