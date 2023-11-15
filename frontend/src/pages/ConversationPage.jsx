import { Container } from "@mui/material";
import TopAppBar from "components/TopAppBar";

function ConversationPage() {
    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="md" style={{ marginTop: '3%', textAlign: 'center' }}>
                <h1>Interview</h1>
            </Container>
        </>
    );
}

export default ConversationPage;