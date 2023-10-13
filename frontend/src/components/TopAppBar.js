import { AppBar, Toolbar, Typography } from '@mui/material';
import React from 'react';
import HomeButton from './HomeButton';

function TopAppBar() {

    return (
        <AppBar position="static" style={{ backgroundColor: '#3f51b5', marginBottom: '20px' }}>
            <Toolbar>
                <HomeButton style={{marginRight: '20px'}}/>
                <Typography variant="h6" style={{ flex: 1 }}>
                    Mock AI Interviewer - Enhance Your Knowledge
                </Typography>
            </Toolbar>
        </AppBar>
    );
}

export default TopAppBar;
