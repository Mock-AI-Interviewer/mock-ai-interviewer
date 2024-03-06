import { Box, Button, Container, Divider, TextField, Typography } from "@mui/material";
import { config } from 'appConfig';
import TopAppBar from "components/TopAppBar";
import TranscriptBox from "components/TranscriptBox";
import PATHS from "paths";
import { useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from 'react-router-dom';

function ConversationPage({ user_id = 1, enableAudioInput = true, enableAudioOutput = true }) {
    const { state } = useLocation();
    const { interviewType, interviewId } = state;
    const navigate = useNavigate();
    const [userInput, setUserInput] = useState('');
    const TURN_INTERVIEWER = "Interviewer's Turn";
    const TURN_CANDIDATE = "Your Turn";
    const [turnAlert, setTurnAlert] = useState(TURN_INTERVIEWER);
    const [messages, setMessages] = useState([]);
    const [recording, setRecording] = useState(false);
    const recorderRef = useRef(null);
    const [isRecorderLoaded, setIsRecorderLoaded] = useState(false);
    const [isInterviewStarted, setIsInterviewStarted] = useState(false);
    const sendIntervalRef = useRef(null);
    const webSocketRef = useRef(null);
    const analyserRef = useRef(null);
    const audioContextRef = useRef(null);
    const canvasRef = useRef(null);
    const animationFrameIdRef = useRef(null);
    const WEB_SOCKET_ENDPOINT = `${config.backendApiWebsocketUrl}/interview/${interviewId}/response`
    const WEB_SOCKET_FULL_URL = `${WEB_SOCKET_ENDPOINT}?user_id=${user_id}&enable_audio_input=${enableAudioInput}&enable_audio_output=${enableAudioOutput}`;
    const START_INTERVIEW_ENDPOINT = `${config.backendApiUrl}/interview/session/${interviewId}/start`
    const STOP_INTERVIEW_ENDPOINT = `${config.backendApiUrl}/interview/session/${interviewId}/end`
    const AUDIO_MESSAGE = "audio"
    const TEXT_MESSAGE = "text"
    const STOP_MESSAGE = "STOP_MESSAGE";


    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 2048; // You can adjust this value
    analyser.connect(audioContext.destination);
    const audioQueue = [];
    let isPlaying = false;
    let bufferThreshold = 0; // Number of chunks to buffer before playing
    let isBuffering = true; // New flag to manage the buffering state
    let nextTime = 0; // Tracks when the next audio chunk should start.


    const addMessage = (newMessage) => {
        setMessages(prevMessages => [...prevMessages, newMessage]);
    };

    useEffect(() => {
        // Check if interviewType is not set and navigate
        if (!interviewType || !interviewId) {
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
            playAudioQueue();
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
        else {
            console.log(`Buffering audio... (Queue length: ${audioQueue.length})`);
        }
    }

    function binaryStringToHex(str) {
        const byteArray = new Uint8Array(str.length);
        for (let i = 0; i < str.length; i++) {
            byteArray[i] = str.charCodeAt(i);
        }
        return Array.from(byteArray).map(byte => byte.toString(16).padStart(2, '0')).join('');
    }

    async function playAudioChunk(encodedAudioData) {
        // Step 1: Decode Base64 string to binary data
        const binaryData = atob(encodedAudioData);
        try {
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
            const hexData = binaryStringToHex(binaryData);
            console.log('Audio data:', hexData);
        }
    }

    function initializeRecording() {
        if (!isRecorderLoaded) {
            console.error("Recorder.js is not loaded yet.");
            return;
        }
        
        navigator.mediaDevices.getUserMedia({ audio: true })
            .then(stream => {
                if (!audioContextRef.current) {
                    audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)();
                }

                if (!analyserRef.current) {
                    analyserRef.current = audioContextRef.current.createAnalyser();
                    analyserRef.current.fftSize = 2048;
                }

                const source = audioContextRef.current.createMediaStreamSource(stream);
                source.connect(analyserRef.current);

                recorderRef.current = new window.Recorder(source, { numChannels: 1 });
                recorderRef.current.record();
                requestAnimationFrame(drawVisual);
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

            cancelAnimationFrame(animationFrameIdRef.current);
            clearCanvas();
            
            setRecording(false);
        }
    }

    function clearCanvas() {
        const canvas = canvasRef.current;
        const canvasCtx = canvas.getContext('2d');
        canvasCtx.clearRect(0, 0, canvas.width, canvas.height);
    }

    const receiveText = (data) => {
        console.log('Recieved message', data);
        addMessage({ user: 'Interviewer', text: data });
    };
    const receiveStop = () => {
        console.log("Recieved stop message");
        setTurnAlert(TURN_CANDIDATE)
    };

    const sendText = () => {
        // Update the interviewer textbox content
        addMessage({ user: 'You', text: userInput });

        // Here you'll call your backend functions
        sendTextMessage(userInput);
        sendStopMessage();
        setTurnAlert(TURN_INTERVIEWER);

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
        setIsInterviewStarted(false);
        sendStopMessage();
        stopInterview();
        stopWebSocket();
        setIsInterviewStarted(false);
        navigate(PATHS.RESULTS, {
            state: {
                interviewId: interviewId
            }
        });
    };

    function stopInterview() {
        fetch(STOP_INTERVIEW_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json()) // Parsing the JSON response
            .then(data => {
                console.log('Success:', data); // Handle the response data
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const handleStartInterview = async () => {
        if (audioContext.state === 'suspended') {
            await audioContext.resume();
        }
        setIsInterviewStarted(true);
        startInterview()
        webSocketRef.current = createWebSocket();
        drawVisual();
    };

    function startInterview() {
        fetch(START_INTERVIEW_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json()) // Parsing the JSON response
            .then(data => {
                console.log('Success:', data); // Handle the response data
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }

    const handleInterruptInterviewer = async () => {
        sendStopMessage();
        setTurnAlert(TURN_CANDIDATE);
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
        let canvas;
        let dataArray;

        if(turnAlert===TURN_INTERVIEWER)
        {
            canvas = document.getElementById('visualizer')
            dataArray = new Uint8Array(analyser.fftSize);
            analyser.getByteTimeDomainData(dataArray);
        }
        else if(turnAlert===TURN_CANDIDATE)
        {
            canvas = canvasRef.current;
            const bufferLength = analyserRef.current.fftSize;
            dataArray = new Uint8Array(bufferLength);
            analyserRef.current.getByteTimeDomainData(dataArray);
        }
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
    
    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" sx={{ mt: '3%', textAlign: 'center' }}>
                <Typography variant="h1">{interviewType.name} Interview</Typography>
                <Typography variant="subtitle1">{interviewType.description}</Typography>
                <Divider sx={{ mt: 2, mb: 2 }} />
                <canvas id="visualizer" width="800px" height="200px"></canvas>
                <canvas ref={canvasRef} id="visualizer2" width="800" height="200"></canvas>
                <Divider sx={{ mt: 2, mb: 2 }} />
                <Typography variant="h6" id="turnAlert"> {turnAlert} </Typography>


                {enableAudioInput === false && (
                    <>
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
                        <Box sx={{ mt: 6, display: 'flex', justifyContent: 'center', gap: 1 }}>
                            <Button onClick={handleSendText} variant="contained" id="sendTextButton">Send</Button>
                        </Box>
                    </>
                )}
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    {isInterviewStarted && (
                        <Button
                            onClick={toggleRecording}
                            variant="contained"
                            disabled={turnAlert !== TURN_CANDIDATE} // Disable button if it's not user's turn
                            sx={{
                                borderRadius: '50%',
                                width: 100,
                                height: 100,
                                backgroundColor: recording ? 'red' : 'green',
                                color: 'white',
                                '&:hover': {
                                    backgroundColor: recording ? 'darkred' : 'darkgreen',
                                }
                            }}
                            id="recordButton"
                        >
                            {recording ? 'Stop' : 'Record'}
                        </Button>
                    )}
                </Box>
                {isInterviewStarted && (
                    <>
                        <Box sx={{ mt: 6, display: 'flex', justifyContent: 'center', gap: 1 }}>
                            <Button onClick={handleInterruptInterviewer} variant="contained" id="interruptInterviewerButton" sx={{ backgroundColor: 'orange', '&:hover': { backgroundColor: 'darkorange' } }}>Interrupt</Button>
                        </Box>
                    </>
                )}
                <Box sx={{ mt: 1, display: 'flex', justifyContent: 'center', gap: 1 }}>
                    <Button
                        onClick={isInterviewStarted ? handleStopInterview : handleStartInterview}
                        variant="contained"
                        color={isInterviewStarted ? "error" : "success"}
                        sx={isInterviewStarted ? {} : {
                            padding: '15px 30px',
                            fontSize: '1.2rem',
                            backgroundColor: '#4caf50',
                            '&:hover': {
                                backgroundColor: '#43a047', 
                            },
                            borderRadius: '20px',
                            boxShadow: '0px 0px 10px rgba(0,0,0,0.2)',
                        }}
                        id={isInterviewStarted ? "stopInterviewButton" : "startInterviewButton"}
                    >
                        {isInterviewStarted ? "Stop Interview" : "Start Interview"}
                    </Button>
                </Box>
                <TranscriptBox messages={messages} isOpen={true} />
            </Container>
        </>
    );
}

export default ConversationPage;
