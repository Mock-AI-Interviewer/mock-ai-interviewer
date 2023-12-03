import { Button, Container, Divider, FormControl, InputLabel, MenuItem, Select, TextareaAutosize } from "@mui/material";
import { config } from 'appConfig';
import InterviewTypeCard from 'components/InterviewTypeCard';
import TopAppBar from "components/TopAppBar";
import PATHS from "paths";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";


function InterviewPage() {
    const navigate = useNavigate();
    const [interviewer, setInterviewer] = useState('');
    const [interviewTypes, setInterviewTypes] = useState([]);
    const [selectedInterviewType, setSelectedInterviewType] = useState(null);
    const [showJobDescription, setShowJobDescription] = useState(false);
    const [jobDescription, setJobDescription] = useState('');
    const LIST_INTERVIEW_TYPES_ENDPOINT = `${config.backendApiUrl}/interview/types`
    const INITIALISE_INTERVIEW_ENDPOINT = `${config.backendApiUrl}/interview/initialise`

    useEffect(() => {
        // Replace the actual fetch call with a mock response
        listInterviewTypes();
    }, []);

    const listInterviewTypes = () => {
        fetch(LIST_INTERVIEW_TYPES_ENDPOINT, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json()) // Parsing the JSON response
            .then(data => {
                setInterviewTypes(data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }


    const initialiseInterview = () => {
        const body = {
            interview_type: {
                ...selectedInterviewType,
                "job_description": jobDescription
            },
            user_id: "1", // TODO: Replace with actual user id
            interviewer: interviewer,
        };
        console.log(body);
        console.log(`Sending request with body: ${JSON.stringify(body)}`);
        fetch(INITIALISE_INTERVIEW_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        })
            .then(response => response.json()) // Parsing the JSON response
            .then(data => {
                navigate(PATHS.CONVERSATION, {
                    state: {
                        interviewType: selectedInterviewType,
                        interviewId: data.interview_id,
                    }
                });
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }


    const handleConfigureInterview = () => {
        initialiseInterview();
    };

    const handleInterviewTypeClick = (interviewType) => {
        console.log(interviewType)
        setSelectedInterviewType(interviewType);
    };

    const toggleJobDescription = () => {
        setShowJobDescription(!showJobDescription);
    };

    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" style={{ marginTop: '3%', textAlign: 'center' }}>
                <h1>Configure Interview</h1>
                <div style={{ margin: '20px' }}>
                    <h2>Select Interview Type</h2>
                    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}>
                        {interviewTypes.map(interviewType => (
                            <InterviewTypeCard
                                key={interviewType.name}
                                interviewType={interviewType}
                                selectedInterviewType={selectedInterviewType}
                                handleInterviewTypeClick={handleInterviewTypeClick}
                                selected={selectedInterviewType === interviewType}
                                onClick={() => handleInterviewTypeClick(interviewType)}
                            />
                        ))}
                    </div>
                </div>
                <div style={{ margin: '20px' }}>
                    <h2>Select Interviewer</h2>
                    <FormControl variant="outlined" style={{ minWidth: 200 }}>
                        <InputLabel id="interviewer-label">Interviewer</InputLabel>
                        <Select
                            labelId="interviewer-label"
                            id="interviewer"
                            value={interviewer}
                            onChange={(event) => setInterviewer(event.target.value)}
                            label="Interviewer"
                        >

                            <MenuItem value="Male">Male</MenuItem>
                            <MenuItem value="Female">Female</MenuItem>
                        </Select>
                    </FormControl>
                </div>
                <div style={{ margin: '20px' }}>
                    <h2>Extras</h2>
                    <Button variant="outlined" onClick={toggleJobDescription}>
                        {showJobDescription ? 'Hide Job Description' : 'Add Job Description'}
                    </Button>
                    {showJobDescription && (
                        <TextareaAutosize
                            minRows={5}
                            style={{ width: '100%', marginTop: '10px' }}
                            placeholder="Paste the job description here"
                            value={jobDescription}
                            onChange={(e) => setJobDescription(e.target.value)}
                        />
                    )}
                </div>
                <Divider style={{ margin: '20px' }} />
                <Button variant="contained" color="success" size="large" sx={{ mb: 10 }} onClick={handleConfigureInterview} disabled={!selectedInterviewType}>
                    Configure Interview
                </Button>
            </Container>
        </>
    );
}

export default InterviewPage;
