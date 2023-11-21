import { Box, Button, Container, Divider, TextField, Typography } from "@mui/material";
import { config } from 'appConfig';
import TopAppBar from "components/TopAppBar";
import TranscriptBox from "components/TranscriptBox";
import PATHS from "paths";
import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';

function ConversationPage({ user_id = 1, enableAudioInput = false, enableAudioOutput = true }) {
    const { state } = useLocation();
    const navigate = useNavigate();
    const [userInput, setUserInput] = useState('');
    const [turnAlert, setTurnAlert] = useState("Interviewer's Turn");
    const [messages, setMessages] = useState([]);
    const [recording, setRecording] = useState(false);
    const recorderRef = useRef(null);
    const [isRecorderLoaded, setIsRecorderLoaded] = useState(false);
    const sendIntervalRef = useRef(null);
    const webSocketRef = useRef(null); // Ref to store the WebSocket instance
    const WEB_SOCKET_ENDPOINT = `${config.backendApiWebsocketUrl}/conversation/response`
    const WEB_SOCKET_FULL_URL = `${WEB_SOCKET_ENDPOINT}?user_id=${user_id}&enable_audio_input=${enableAudioInput}&enable_audio_output=${enableAudioOutput}`;
    const AUDIO_MESSAGE = "audio"
    const TEXT_MESSAGE = "text"
    const STOP_MESSAGE = "STOP_MESSAGE";


    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048; // You can adjust this value
    analyser.connect(audioContext.destination);
    const audioQueue = [];
    let isPlaying = false;
    let bufferThreshold = 1; // Number of chunks to buffer before playing
    let isBuffering = true; // New flag to manage the buffering state
    let nextTime = 0; // Tracks when the next audio chunk should start.

    // Extract interviewType from location state
    const interviewType = state?.interviewType;


    const addMessage = (newMessage) => {
        setMessages(prevMessages => [...prevMessages, newMessage]);
    };

    useEffect(() => {
        // Check if interviewType is not set and navigate
        if (!interviewType) {
            navigate(PATHS.HOME);
        }
    }, [interviewType, navigate]);

    // Use useEffect to log messages when they change
    useEffect(() => {
        console.log(messages);
    }, [messages]);

    useEffect(() => {
        const script = document.createElement('script');
        script.src = "https://cdnjs.cloudflare.com/ajax/libs/recorderjs/0.1.0/recorder.js";
        script.onload = () => setIsRecorderLoaded(true);
        document.body.appendChild(script);
    }, []);

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
            if (parsed_data.type === AUDIO_MESSAGE && enableAudioOutput) {
                receiveAudio(parsed_data.data);
            } else if (parsed_data.type === TEXT_MESSAGE) {
                receiveText(parsed_data.data);
            } else if (parsed_data.type === STOP_MESSAGE) {
                receiveStop();
            }
        };

        console.log('Creating WebSocket: new WebSocket', ws);
        return ws;
    };

    const receiveAudio = (encodedAudioData) => {
        audioQueue.push(encodedAudioData);
        if (!isPlaying) {
            playAudioQueue(); // Try to play the queue if not already playing
        }
    };

    const sendAudioChunk = () => {
        if (recorderRef.current && webSocketRef.current && webSocketRef.current.readyState === WebSocket.OPEN) {
            recorderRef.current.exportWAV(blob => {
                webSocketRef.current.send(blob);
                recorderRef.current.clear(); // Clear the recorder's buffer after sending
            }, 'audio/wav');
        }
    };

    async function playAudioQueue() {
        // Start playing if we've reached the buffer threshold or if we're already playing and more data is available
        if ((isBuffering && audioQueue.length >= bufferThreshold) || (!isBuffering && audioQueue.length > 0)) {
            if (isBuffering) {
                isBuffering = false; // Stop buffering once we start playing
            }
            while (audioQueue.length > 0) {
                isPlaying = true;
                const audioData = audioQueue.shift(); // Get the first chunk in the queue
                await playAudioChunk(audioData);
            }
            isPlaying = false; // Set to false when the queue is empty
        }
    }

    async function playAudioChunk(encodedAudioData) {
        try {
            // Step 1: Decode Base64 string to binary data
            const binaryData = atob(encodedAudioData);

            // Step 2: Convert binary data to ArrayBuffer
            const length = binaryData.length;
            const buffer = new ArrayBuffer(length);
            const view = new Uint8Array(buffer);
            for (let i = 0; i < length; i++) {
                view[i] = binaryData.charCodeAt(i);
            }

            const decodedData = await audioContext.decodeAudioData(buffer);
            const source = audioContext.createBufferSource();
            source.buffer = decodedData;
            source.connect(analyser);
            source.connect(audioContext.destination);

            // Schedule playback to ensure smooth transition between chunks
            const currentTime = audioContext.currentTime;
            const startOffset = nextTime > currentTime ? nextTime : currentTime;
            source.start(startOffset);
            nextTime = startOffset + source.buffer.duration; // Schedule the next chunk

            // Return a promise that resolves when the audio finishes playing
            return new Promise(resolve => source.onended = resolve);
        } catch (e) {
            console.error('Error decoding audio data:', e);
        }
    }

    function initializeRecording() {
        if (!isRecorderLoaded) {
            console.error("Recorder.js is not loaded yet.");
            return;
        }
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const audioContext = new AudioContext();
                const source = audioContext.createMediaStreamSource(stream);

                recorderRef.current = new window.Recorder(source, { numChannels: 1 });
                recorderRef.current.record();
                setRecording(true);

                // Set up an interval to send audio chunks
                sendIntervalRef.current = setInterval(sendAudioChunk, 1000); // Adjust interval as needed
            })
            .catch(error => {
                console.error('Error accessing microphone:', error);
            });
    }

    function stopRecording() {
        if (recorderRef.current) {
            clearInterval(sendIntervalRef.current); // Clear the interval
            recorderRef.current.stop();
            sendAudioChunk(); // Send the last chunk of audio

            // Delayed sending of the "recording_stopped" message
            setTimeout(() => {
                webSocketRef.current.send("recording_stopped");
                console.log('Sent text');
            }, 1000); // Wait for 1 second before sending the message

            setRecording(false);
        }
    }

    const receiveText = (data) => {
        console.log('Recieved message', data);
        addMessage({ user: 'Interviewer', text: data });
    };
    const receiveStop = () => {
        console.log("Recieved stop message");
        setTurnAlert("Your Turn")
    };

    const sendText = () => {
        // Update the interviewer textbox content
        addMessage({ user: 'You', text: userInput });

        // Here you'll call your backend functions
        sendTextMessage(userInput);
        sendStopMessage();
        setTurnAlert("Interviewer's Turn");

        // Clear the user input field
        setUserInput('');
    };

    const sendTextMessage = (text) => {
        const textMessage = {
            type: "text",
            data: text
        };
        const messageString = JSON.stringify(textMessage);
        webSocketRef.current.send(messageString);
        console.log('Sent message', messageString);
    };

    const sendStopMessage = () => {
        const stopMessage = {
            type: STOP_MESSAGE,
            data: ""
        };
        const messageString = JSON.stringify(stopMessage);
        webSocketRef.current.send(messageString);
        console.log('Sent message', messageString);
    };

    const stopWebSocket = () => {
        webSocketRef.current.close();
    };

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
        drawVisual();
    };

    const handleInterruptInterviewer = async () => {
        sendStopMessage();
        setTurnAlert("Your Turn");
    };

    const toggleRecording = () => {
        if (!recording) {
            initializeRecording();
        } else {
            stopRecording();
        }
    };

    function drawVisual() {
        // Draw Waveform
        requestAnimationFrame(drawVisual);

        const dataArray = new Uint8Array(analyser.fftSize);
        analyser.getByteTimeDomainData(dataArray);

        const canvas = document.getElementById('visualizer');
        const context = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        context.fillStyle = 'rgba(255, 255, 255, 0.5)'; // Background color
        context.fillRect(0, 0, width, height);

        context.lineWidth = 2;
        context.strokeStyle = 'rgb(0, 0, 0)'; // Waveform color

        context.beginPath();

        const sliceWidth = width * 1.0 / dataArray.length;
        let x = 0;

        for (let i = 0; i < dataArray.length; i++) {

            const v = dataArray[i] / 128.0; // Normalize byte value to [0, 1]
            const y = v * height / 2;

            if (i === 0) {
                context.moveTo(x, y);
            } else {
                context.lineTo(x, y);
            }

            x += sliceWidth;
        }

        context.lineTo(canvas.width, canvas.height / 2);
        context.stroke();
    }

    // function drawVisual() {
    //     // Draw Pulsating Circle
    //     requestAnimationFrame(drawVisual);

    //     const dataArray = new Uint8Array(analyser.frequencyBinCount);
    //     analyser.getByteFrequencyData(dataArray);

    //     // Simple example: draw a circle that changes size with the audio
    //     const canvas = document.getElementById('visualizer');
    //     const context = canvas.getContext('2d');

    //     const radius = dataArray.reduce((sum, value) => sum + value, 0) / dataArray.length;
    //     context.clearRect(0, 0, canvas.width, canvas.height);
    //     context.beginPath();
    //     context.arc(canvas.width / 2, canvas.height / 2, radius, 0, 2 * Math.PI);
    //     context.fill();
    // }


    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" sx={{ mt: '3%', textAlign: 'center' }}>
                <Typography variant="h1">{interviewType.name} Interview</Typography>
                <Typography variant="subtitle1">{interviewType.description}</Typography>
                <Divider sx={{ mt: 2, mb: 2 }} />
                <canvas id="visualizer" width="800px" height="200px"></canvas>

                {/* <div>
                    <Typography variant="h6">Transcript:</Typography>
                    <div ref={interviewerTextboxRef} id="interviewerTextbox" sx={{
                        maxHeight: '150px',
                        width: '50%',
                        margin: 'auto',
                        overflowY: 'auto',
                        whiteSpace: 'pre-wrap',
                        border: 1,
                        borderColor: 'grey.300',
                        p: 1,
                    }}>
                        {interviewerText}
                    </div>
                </div> */}
                <Divider sx={{ mt: 2, mb: 2 }} />
                <Typography variant="h6" id="turnAlert"> {turnAlert} </Typography>
                <TextField
                    id="userInput"
                    placeholder="Type something..."
                    multiline
                    rows={5}
                    value={userInput}
                    onChange={e => setUserInput(e.target.value)}
                    sx={{
                        width: '50%',
                        height: '150px',
                        resize: 'both',
                        mb: 1,
                        overflow: 'auto',
                    }}
                />
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 1 }}>
                <Button onClick={toggleRecording} variant="contained" color="success" id="recordButton">
                    {recording ? 'Stop Recording' : 'Start Recording'}
                </Button>
                </Box>
                <Box sx={{ mt: 6, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button onClick={handleSendText} variant="contained" id="sendTextButton" >Send</Button>
                    <Button onClick={handleInterruptInterviewer} variant="contained" id="interruptInterviewerButton" sx={{ backgroundColor: 'orange', '&:hover': { backgroundColor: 'darkorange' } }}>Interrupt</Button>
                </Box>
                <Box sx={{ mt: 1, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button onClick={handleStartInterview} variant="contained" color="success" id="startInterviewButton">Start Interview</Button>
                    <Button onClick={handleStopInterview} variant="contained" color="error" id="stopInterviewButton">Stop Interview</Button>
                </Box>
                {/* <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button onClick={toggleRecording} variant="contained" color="success" id="recordButton">{recording ? 'Stop Recording' : 'Start Recording'}</Button>
                </Box> */}

                <TranscriptBox messages={messages} isOpen={true} />
            </Container>
        </>
    );
}

export default ConversationPage;
