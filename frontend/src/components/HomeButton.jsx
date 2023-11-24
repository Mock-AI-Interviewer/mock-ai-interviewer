import React from "react";
import { Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import HomeIcon from "@mui/icons-material/Home";
import PATHS from "paths";

function HomeButton(props) {
    const navigate = useNavigate();

    const handleHomeClick = () => {
        navigate(PATHS.HOME);
    };

    return (
        <Button variant="contained" startIcon={<HomeIcon />} color="primary" style={{ margin: '10px 0' }} onClick={handleHomeClick} {...props}>
            Home
        </Button>
    );
}

export default HomeButton;
