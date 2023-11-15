import { Container } from "@mui/material";
import React from "react";
import TopAppBar from "components/TopAppBar";

function HomePage() {
    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="md" style={{ marginTop: '3%', textAlign: 'center' }}>
                <h1>Mock AI Interviewer</h1>
                <br />
                <br />
            </Container>
        </>
    );
}

export default HomePage;