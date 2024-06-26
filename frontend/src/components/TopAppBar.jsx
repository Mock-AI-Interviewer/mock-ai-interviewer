import PsychologyIcon from '@mui/icons-material/Psychology';
import { AppBar, ButtonBase, Toolbar, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom'; // Import useNavigate hook for navigation

function TopAppBar() {
    const navigate = useNavigate();

    const handleHomeClick = () => {
        navigate('/'); // Update this with your home route
    };

    return (
        <AppBar position="static" color="transparent" style={{ marginBottom: '20px' }}>
            <Toolbar>
                <ButtonBase onClick={handleHomeClick} style={{ display: 'flex', alignItems: 'center' }}>
                    <PsychologyIcon fontSize="large" /> {/* Custom AI icon */}
                    <Typography variant="h5" style={{ fontWeight: 300, marginLeft: '10px' }}>
                        Mock AI Interviewer
                    </Typography>
                </ButtonBase>
                {/* Removed HomeButton, since home navigation is now integrated with icon and text */}
            </Toolbar>
        </AppBar>
    );
}

export default TopAppBar;
