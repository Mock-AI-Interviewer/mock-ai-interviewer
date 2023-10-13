import React, { useState } from "react";
import { Button, TextField, FormControl, InputLabel, Select, MenuItem, Container } from "@mui/material";

import axios from "axios";
import { BASE_API_ENDPOINT } from "../config";
import HomeButton from "../components/HomeButton";
import ErrorMessage from "../components/ErrorMessage";
import SuccessMessage from "../components/SuccessMessage";
import TopAppBar from "../components/TopAppBar";

function RegisterPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const [role, setRole] = useState("normal");
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);

    const handleRegister = async () => {
        setError(null);
        setSuccess(null);
        try {
            const response = await axios.post(`${BASE_API_ENDPOINT}/auth/register`, {
                email,
                password,
                is_active: true,
                is_superuser: false,
                is_verified: false,
                name,
                role
            }, {
                headers: {
                    "Content-Type": "application/json"
                }
            });
            console.log(response.data);
            if(response.status === 201) {
                setSuccess('Registration successful!, Please login to continue');
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
                    <h1>Register</h1>
                    <TextField label="Name" variant="outlined" margin="normal" fullWidth onChange={e => setName(e.target.value)} />
                    <TextField label="Email" variant="outlined" margin="normal" fullWidth onChange={e => setEmail(e.target.value)} />
                    <TextField label="Password" variant="outlined" margin="normal" fullWidth type="password" onChange={e => setPassword(e.target.value)} />
                    <FormControl variant="outlined" margin="normal" fullWidth>
                        <InputLabel>Role</InputLabel>
                        <Select value={role} label="Role" onChange={e => setRole(e.target.value === "Student" ? "normal" : "advisor")}>
                            <MenuItem value="normal">Student</MenuItem>
                            <MenuItem value="advisor">Advisor</MenuItem>
                        </Select>
                    </FormControl>
                    <Button variant="contained" color="primary" onClick={handleRegister}>Register</Button>
                </div>
                {error && <ErrorMessage message={error} style={{ marginTop: '20px' }} />}
                {success && <SuccessMessage message={success} />} {/* Display the success message when present */}
            </Container>
        </>

    );
}

export default RegisterPage;
