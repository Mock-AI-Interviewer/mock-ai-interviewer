import { Button, Container, Typography, Box, useMediaQuery, useTheme } from "@mui/material";
import TopAppBar from "components/TopAppBar";
import PATHS from "paths";
import { useNavigate } from "react-router-dom";

function HomePage() {
    const navigate = useNavigate();
    const theme = useTheme();
    const matches = useMediaQuery(theme.breakpoints.up('md'));
    const getStarted = () => {
        navigate(PATHS.INTERVIEW);
    };

    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" style={{ 
                height: 'calc(100vh - 64px)', // Adjust for AppBar height
                display: 'flex',
                alignItems: 'center', // Vertical centering
                justifyContent: 'center', // Horizontal centering
                textAlign: 'center'
            }}>
                <Box display="flex" flexDirection={matches ? "row" : "column"} alignItems="center" justifyContent="center">
                    <Box flex={1} mb={matches ? 0 : 3}>
                        <Typography variant="h2" style={{ fontWeight: 600, marginBottom: '2%' }}>Mock AI Interviewer</Typography>
                        <Typography variant="h5" style={{ marginBottom: '4%' }}>Prepare for your next interview with AI-driven insights</Typography>
                        <Button variant="contained" onClick={getStarted} size="large" style={{ fontWeight: 700 }}>Get Started</Button>
                    </Box>
                    <Box flex={1} style={{ maxWidth: 400, maxHeight: 400, overflow: 'hidden' }}>
                        {/* Image here */}
                        <img src="https://img.freepik.com/free-vector/interview-concept-illustration_114360-1678.jpg?size=338&ext=jpg&ga=GA1.1.1826414947.1699488000&semt=ais" alt="AI Interviewer" style={{ width: '100%', height: 'auto', borderRadius: '8px' }} />
                    </Box>
                </Box>
            </Container>
        </>
    );
}

export default HomePage;
