import { Container } from "@mui/material";
import React, { useState, useEffect } from 'react';
import TopAppBar from "components/TopAppBar";
import { config } from 'appConfig';

function AudioRecorderPage() {
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [audioURL, setAudioURL] = useState(null);
    const [websocket, setWebsocket] = useState(null);
    const [chunks, setChunks] = useState([]);
    const [websocketEndpoint, setWebsocketEndpoint] = useState(`${config.backendApiWebsocketUrl}/ws/audio`);
    const [receivedText, setReceivedText] = useState('');
    const [liveUpdate, setLiveUpdate] = useState(''); // State for live update
    const [chunkCount, setChunkCount] = useState(0); // State to track the chunk count
    const [audioChunks, setAudioChunks] = useState([]);
    const [isPlaying, setIsPlaying] = useState(false); // State to control audio playback


    // Handle WebSocket initialization
    useEffect(() => {
        const ws = new WebSocket(websocketEndpoint);

        ws.onopen = () => {
        console.log('WebSocket Connected');
        ws.binaryType = 'blob';
        setWebsocket(ws);
        };

        ws.onclose = () => {
        console.log('WebSocket Disconnected');
        setWebsocket(null);
        };

        ws.onerror = (error) => {
            console.error('WebSocket Error:', error);
        };
    }, [websocketEndpoint]);

    useEffect(() => {
        if (recording && websocket) {
        initializeRecording();
        } else {
        stopRecording();
        }
    }, [recording, websocket]);

    useEffect(() => {
        if (websocket) {
        websocket.onmessage = (event) => {
            const data = event.data;
            console.log('Received data:', data);
            // Check if the received data is an audio chunk
            if (data instanceof Blob) {
            setAudioChunks((prevChunks) => [...prevChunks, data]);

            } else {
            console.log('Received text data:', data);
            }
            setLiveUpdate('Chunk sent to server ' + (chunkCount + 1)); // Increment chunk count
            setChunkCount(chunkCount + 1); // Update chunk count
        };
        }
    }, [websocket, chunkCount]);

    const initializeRecording = () => {
        navigator.mediaDevices
        .getUserMedia({ audio: true })
        .then((stream) => {
            const mediaRecorder = new MediaRecorder(stream, { timeslice: 1000 });
    
            mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                const chunk = event.data; // Capture the chunk
                chunks.push(chunk);
    
                if (websocket) {
                console.log('Sending message:', chunk);
                // Send the captured chunk to the WebSocket server
                websocket.send(chunk);
                }
            }
            };
    
            mediaRecorder.onstop = () => {
            // Handle the stop event
            const audioBlob = new Blob(chunks, { type: 'audio/wav' });
            const url = URL.createObjectURL(audioBlob);
            setAudioURL(url);
            };
    
            mediaRecorder.start(1000);
            setMediaRecorder(mediaRecorder);
        })
        .catch((error) => {
            console.error('Error accessing microphone:', error);
            setRecording(false);
        });
    };
    

    const stopRecording = () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        const audioBlob = new Blob(chunks, { type: 'audio/wav' });
        const url = URL.createObjectURL(audioBlob);
        setAudioURL(url);
        setChunks([]); // Clear the chunks array
        
        }
    };

    const toggleRecording = () => {
        setRecording(!recording);
    };

    return (
        <>
            <TopAppBar />
            <Container component="audio-recorder-container" maxWidth="md" style={{ marginTop: '3%', textAlign: 'center' }}>
            <header>
          <p>Record and play audio below:</p>
        </header>
            <main>
            <button onClick={toggleRecording}>
                {recording ? 'Stop Recording' : 'Start Recording'}
            </button>
            {audioURL && (
                <>
                <audio controls src={audioURL} />
                <button onClick={() => setAudioURL(null)}>Clear Audio</button>
                </>
            )}
            <div>
                <strong>Received Text:</strong>
                <div>{receivedText}</div>
            </div>
            <div>{liveUpdate}</div> {/* Display live update */}
            </main>
            </Container>
        </>
    );
}

export default AudioRecorderPage;