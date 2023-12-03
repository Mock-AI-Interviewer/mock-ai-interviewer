import React from 'react';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';
import { styled } from '@mui/material/styles';

const StyledSnackbar = styled(Snackbar)(({ theme }) => ({
    // Add custom styles here
}));

const Alert = styled(MuiAlert)(({ theme }) => ({
    // Add custom styles for the alert
}));

function ErrorSnackbar({ open, handleClose, errorMessage }) {
    return (
        <StyledSnackbar
            open={open}
            autoHideDuration={6000}
            onClose={handleClose}
            anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        >
            <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
                {errorMessage}
            </Alert>
        </StyledSnackbar>
    );
}

export default ErrorSnackbar;
