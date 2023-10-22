import React from 'react';
import { Alert } from '@mui/material';

function ErrorMessage({ message }) {
    return (
        <Alert severity="error" style={{ marginTop: '10px' }}>
            {message}
        </Alert>
    );
}

export default ErrorMessage;
