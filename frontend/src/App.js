import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import AudioRecorderPage from "./pages/AudioRecorderPage";
function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/audio-recorder"  element={<AudioRecorderPage />} />
            </Routes>
        </Router>
    );
}

export default App;
