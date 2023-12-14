import AudioRecorderPage from "pages/AudioRecorderPage";
import ConversationPage from "pages/ConversationPage";
import InterviewPage from "pages/InterviewPage";
import ResultsPage from "pages/ResultsPage";
import AdminPage from "pages/AdminPage";
import PATHS from "paths";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";

function App() {
    return (
        <Router>
            <Routes>
                <Route path={PATHS.HOME} element={<HomePage />} />
                <Route path={PATHS.AUDIO_RECORDER} element={<AudioRecorderPage />} />
                <Route path={PATHS.INTERVIEW} element={<InterviewPage />} />
                <Route path={PATHS.CONVERSATION} element={<ConversationPage />} />
                <Route path={PATHS.RESULTS} element={<ResultsPage />} />
                <Route path={PATHS.ADMIN} element={<AdminPage />} />
            </Routes>
        </Router>
    );
}

export default App;
