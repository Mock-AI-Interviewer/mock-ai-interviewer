import React from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import PermContactCalendarIcon from '@mui/icons-material/PermContactCalendar';

function ProfileButton(props) {
    const navigate = useNavigate();

    const handleProfileClick = () => {
        navigate('/profile');
    };

    return (
        <Button variant="contained" startIcon={<PermContactCalendarIcon />} color="primary" style={{ margin: '10px 0' }} onClick={handleProfileClick} {...props}>
            Profile
        </Button>
    );
}

export default ProfileButton;
