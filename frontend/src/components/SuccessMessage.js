import React from 'react';
import { Alert } from '@mui/material';

function SuccessMessage({ message }) {
    return (
        <Alert severity="success" style={{ marginTop: '10px' }}>
            {message}
        </Alert>
    );
}

export default SuccessMessage;
