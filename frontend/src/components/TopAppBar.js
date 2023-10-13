import React, { useState, useEffect } from 'react';
import { AppBar, Toolbar, Typography, Button } from '@mui/material';
import axios from 'axios';
import { BASE_API_ENDPOINT } from '../config';
import Logout from './Logout';
import HomeButton from './HomeButton';
import ProfileButton from './ProfileButton';
import {checkLoginStatus} from "../utilities/checkLoginStatus";

function TopAppBar() {
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        checkLoginStatus(setIsLoggedIn)
    }, []);

    return (
        <AppBar position="static" style={{ backgroundColor: '#3f51b5', marginBottom: '20px' }}>
            <Toolbar>
                <HomeButton style={{marginRight: '20px'}}/>
                <Typography variant="h6" style={{ flex: 1 }}>
                    Quiz App - Enhance Your Knowledge
                </Typography>
                {isLoggedIn && (
                    <>
                        <Typography variant="subtitle1" style={{ marginRight: '20px' }}>
                            Logged in
                        </Typography>
                        <ProfileButton style={{marginRight:"10px"}}/>
                        <Logout />

                    </>
                )}
            </Toolbar>
        </AppBar>
    );
}

export default TopAppBar;
