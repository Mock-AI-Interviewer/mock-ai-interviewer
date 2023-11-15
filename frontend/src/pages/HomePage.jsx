import { Button, Container } from "@mui/material";
import TopAppBar from "components/TopAppBar";
import PATHS from "paths";
import { useNavigate } from "react-router-dom";

function HomePage() {
    const navigate = useNavigate();
    const getStarted = () => {
        navigate(PATHS.INTERVIEW);
    };


    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="md" style={{ marginTop: '3%', textAlign: 'center' }}>
                <h1>Mock AI Interviewer</h1>
                <br />
                <br />
                <Button variant="contained" onClick={getStarted}>Get Started</Button>
            </Container>
        </>
    );
}

export default HomePage;