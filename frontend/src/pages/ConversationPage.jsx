import { Box, Button, Container, TextField, Typography } from "@mui/material";
import TopAppBar from "components/TopAppBar";
import PATHS from "paths";
import { useEffect } from "react";
import { useLocation, useNavigate } from 'react-router-dom';

function ConversationPage() {
    const location = useLocation();
    const navigate = useNavigate();

    // Extract interviewType from location state
    const interviewType = location.state?.interviewType;

    useEffect(() => {
        // Check if interviewType is not set and navigate
        if (!interviewType) {
            navigate(PATHS.HOME);
        }
    }, [interviewType, navigate]);

    // If interviewType is not set, you can return null or a loading indicator
    // This will handle the case where the state hasn't been set yet
    if (!interviewType) {
        return null; // or some loading indicator
    }


    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" sx={{ mt: '3%', textAlign: 'center' }}>
                <Typography variant="h1">{interviewType.name} Interview</Typography>
                <Typography variant="subtitle1">{interviewType.description}</Typography>
                <div>
                    <Typography variant="h3">Transcript:</Typography>
                    <div id="interviewerTextbox" sx={{
                        maxHeight: '150px',
                        width: '50%',
                        margin: 'auto',
                        overflowY: 'auto',
                        whiteSpace: 'pre-wrap',
                        border: 1,
                        borderColor: 'grey.300',
                        p: 1,
                    }}></div>
                    <Typography variant="h3" id="turnAlert">Interviewers Turn</Typography>
                </div>
                <TextField
                    id="userInput"
                    placeholder="Type something..."
                    multiline
                    rows={5}
                    sx={{
                        width: '50%',
                        height: '150px',
                        resize: 'both',
                        mb: 1,
                        overflow: 'auto',
                    }}
                />
                <Box sx={{ mt: 6, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button variant="contained" id="sendTextButton">Send</Button>
                    <Button variant="contained" id="interruptInterviewerButton" sx={{ backgroundColor: 'orange', '&:hover': { backgroundColor: 'darkorange' } }}>Interrupt</Button>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button variant="contained" color="success" id="startInterviewButton">Start Interview</Button>
                    <Button variant="contained" color="error" id="stopInterviewButton">Stop Interview</Button>
                </Box>
            </Container>
        </>
    );
}

export default ConversationPage;
