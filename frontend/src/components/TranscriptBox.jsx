import { Button, Collapse, Paper, Typography } from '@mui/material';
import { useEffect, useRef, useState } from 'react';

const TranscriptBox = (
    {
        messages,
        maxHeight = 100,
        maxWidth = "50%",
        backgroundColor = "white",
        isOpen = false
    }
) => {
    const [open, setOpen] = useState(isOpen);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        if (open) {
            scrollToBottom();
        }
    }, [messages, open]);

    return (
        <div style={{ maxWidth: maxWidth, margin: "auto", backgroundColor: backgroundColor, padding: '10px' }}>
            <Button onClick={() => setOpen(!open)} style={{ marginBottom: '10px' }}>
                {open ? 'Hide Transcript' : 'Show Transcript'}
            </Button>
            <Paper style={{ maxHeight: open ? maxHeight : 0, overflow: 'auto', padding: open ? '10px' : 0, backgroundColor: 'transparent' }}>
                <Collapse in={open}>
                    {messages.map((message, index) => (
                        <Typography key={index} variant="body1" style={{ margin: '5px 0' }}>
                            <strong>{message.user}: </strong>{message.text}
                        </Typography>
                    ))}
                    <div ref={messagesEndRef} />
                </Collapse>
            </Paper>
        </div>
    );
};

export default TranscriptBox;
