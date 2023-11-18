import { Box, Button, Container, Divider, TextField, Typography } from "@mui/material";
import TopAppBar from "components/TopAppBar";
import { config } from 'appConfig';
import PATHS from "paths";
import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from 'react-router-dom';

function ConversationPage({ user_id = 1, enableAudioInput = false, enableAudioOutput = false }) {
    const { state } = useLocation();
    const navigate = useNavigate();
    const webSocketRef = useRef(null); // Ref to store the WebSocket instance
    const WEB_SOCKET_ENDPOINT = `${config.backendApiWebsocketUrl}/conversation/response`
    const WEB_SOCKET_FULL_URL = `${WEB_SOCKET_ENDPOINT}?user_id=${user_id}&enable_audio_input=${enableAudioInput}&enable_audio_output=${enableAudioOutput}`;

    // Extract interviewType from location state
    const interviewType = state?.interviewType;

    useEffect(() => {
        // Check if interviewType is not set and navigate
        if (!interviewType) {
            navigate(PATHS.HOME);
        }
    }, [interviewType, navigate]);


    if (!interviewType) {
        return null;
    }

    const createWebSocket = () => {
        if (webSocketRef.current != null) {
            return;
        }

        console.log('Creating WebSocket');
        const ws = new WebSocket(WEB_SOCKET_FULL_URL);
        ws.binaryType = 'arraybuffer';

        ws.onopen = (event) => {
            console.log('Connection opened', event);
        };

        ws.onerror = (event) => {
            console.error('WebSocket error observed:', event);
        };

        ws.onclose = (event) => {
            console.log('WebSocket is closed now.', event);
        };

        ws.onmessage = async (event) => {
            const parsed_data = JSON.parse(event.data);
            if (parsed_data.type === "audio" && enableAudioOutput) {
                receiveAudio(parsed_data.data);
            } else if (parsed_data.type === "text") {
                receiveText(parsed_data.data);
            } else {
                receiveStop();
            }
        };

        console.log('Creating WebSocket: new WebSocket', ws);
        return ws;
    };

    const receiveAudio = (data) => {};
    const receiveText = (data) => {};
    const receiveStop = () => {};
    const sendText = () => { /* ... */ };
    const sendStopMessage = () => { /* ... */ };
    const stopWebSocket = () => { /* ... */ };
    const updateTurnAlert = () => { /* ... */ };
    const audioContext = {/* ... */ }; // Assuming this is defined somewhere

    const handleSendText = async () => {
        sendText();
    };

    const handleStopInterview = () => {
        sendStopMessage();
        stopWebSocket();
    };

    const handleStartInterview = async () => {
        if (audioContext.state === 'suspended') {
            await audioContext.resume();
        }
        webSocketRef.current = createWebSocket();
    };

    const handleInterruptInterviewer = async () => {
        sendStopMessage();
        updateTurnAlert("Your Turn");
    };


    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" sx={{ mt: '3%', textAlign: 'center' }}>
                <Typography variant="h1">{interviewType.name} Interview</Typography>
                <Typography variant="subtitle1">{interviewType.description}</Typography>
                <Divider sx={{ mt: 2, mb: 2 }} />
                <div>
                    <Typography variant="h6">Transcript:</Typography>
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
                    <Typography variant="h6" id="turnAlert">Interviewers Turn</Typography>
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
                    <Button onClick={handleSendText} variant="contained" id="sendTextButton" >Send</Button>
                    <Button onClick={handleInterruptInterviewer} variant="contained" id="interruptInterviewerButton" sx={{ backgroundColor: 'orange', '&:hover': { backgroundColor: 'darkorange' } }}>Interrupt</Button>
                </Box>
                <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button onClick={handleStartInterview} variant="contained" color="success" id="startInterviewButton">Start Interview</Button>
                    <Button onClick={handleStopInterview} variant="contained" color="error" id="stopInterviewButton">Stop Interview</Button>
                </Box>
            </Container>
        </>
    );
}

export default ConversationPage;
