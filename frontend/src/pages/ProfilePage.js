import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {Accordion, AccordionDetails, AccordionSummary, Button, Container, Typography} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import TopAppBar from "../components/TopAppBar";
import {RESPONSE_MAPPINGS} from '../utilities/responseMapping';
import {withAuthProtection} from "../components/withAuthProtection";

function ProfilePage() {
    const [bookedSlots, setBookedSlots] = useState([]);
    const [availableSlots, setAvailableSlots] = useState([]);
    const [selectedSlotId, setSelectedSlotId] = useState(null);
    const [quizHistory, setQuizHistory] = useState([]);
    const [questionMap, setQuestionMap] = useState({});

    useEffect(() => {
        const fetchBookedSlots = async () => {
            try {
                const {data} = await axios.get('http://localhost:8000/users/me/slots', {
                    headers: {'Accept': 'application/json'},
                });
                setBookedSlots(data);
            } catch (error) {
                console.error('Error fetching booked slots:', error);
            }
        };

        const fetchAvailableSlots = async () => {
            try {
                const {data} = await axios.get('http://localhost:8000/meetings/slots/', {
                    headers: {'Accept': 'application/json'},
                });
                setAvailableSlots(data);
            } catch (error) {
                console.error('Error fetching available slots:', error);
            }
        };

        const fetchQuizQuestions = async (quizId) => {
            try {
                const {data} = await axios.get(`http://localhost:8000/quizzes/${quizId}`, {
                    headers: {'Accept': 'application/json'},
                });

                const newQuestionMap = data.questions.reduce((acc, question) => {
                    acc[question.question_id] = question.question;
                    return acc;
                }, {});

                setQuestionMap(prev => ({...prev, ...newQuestionMap}));
            } catch (error) {
                console.error('Error fetching quiz questions:', error);
            }
        };

        const fetchQuizHistory = async () => {
            try {
                const {data} = await axios.get('http://localhost:8000/users/me/quiz_attempts', {
                    headers: {'Accept': 'application/json'},
                });

                setQuizHistory(data);

                const uniqueQuizIds = [...new Set(data.map(item => item.quiz_id))];
                uniqueQuizIds.forEach(quizId => fetchQuizQuestions(quizId));
            } catch (error) {
                console.error('Error fetching quiz history:', error);
            }
        };

        fetchBookedSlots();
        fetchAvailableSlots();
        fetchQuizHistory();
    }, []);

    const bookSlot = async () => {
        try {
            await axios.post(
                'http://localhost:8000/users/me/slots',
                JSON.stringify(selectedSlotId),
                {
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                }
            );
            window.location.reload();
        } catch (error) {
            console.error('Error booking slot:', error);
        }
    };

    return (
        <>
            <TopAppBar/>
            <Container component="main" maxWidth="md" style={{marginTop: '8%', textAlign: 'center'}}>
                <Typography variant="h2" gutterBottom style={{ marginBottom: '20px'}}>
                    Profile
                </Typography>
                <div style={{margin: '20px 0'}}>
                    <Typography variant="h5">Your Booked Sessions</Typography>
                    <p>
                        View and manage your upcoming one-to-one counselling sessions with our academic counsellors.
                        Our advisors are trained to discuss you’re A-level matching tool results, provide personalized
                        guidance, and set you on the path to academic success.
                    </p>
                    {bookedSlots.map((slot) => (
                        <Accordion key={slot.slot_id}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                <Typography>{new Date(slot.start_time).toLocaleString()}</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Typography>
                                    End Time: {new Date(slot.end_time).toLocaleString()} <br/>
                                    Advisor Name: {slot.advisor_name}
                                </Typography>
                            </AccordionDetails>
                        </Accordion>
                    ))}
                </div>

                <div style={{margin: '20px 0'}}>
                    <Typography variant="h5">Available Sessions</Typography>
                    {availableSlots.map((slot) => (
                        <Accordion key={slot.slot_id}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                <Typography>{new Date(slot.start_time).toLocaleString()}</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Typography>
                                    End Time: {new Date(slot.end_time).toLocaleString()} <br/>
                                    Advisor Name: {slot.advisor_name}
                                </Typography>
                            </AccordionDetails>
                            <Button variant="contained" color="primary" onClick={() => setSelectedSlotId(slot.slot_id)}>
                                Select
                            </Button>
                        </Accordion>
                    ))}
                    <Button variant="contained" color="primary" onClick={bookSlot} disabled={!selectedSlotId}
                            style={{marginTop: '20px'}}>
                        Book Selected Slot
                    </Button>
                </div>

                <div style={{margin: '20px 0'}}>
                    <Typography variant="h5">Quiz History</Typography>
                    {quizHistory.map((quiz) => (
                        <Accordion key={quiz.quiz_attempt_id}>
                            <AccordionSummary expandIcon={<ExpandMoreIcon/>}>
                                <Typography>
                                    Quiz Attempt ID: {quiz.quiz_attempt_id}, End
                                    Time: {new Date(quiz.end_time).toLocaleString()}
                                </Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Typography>
                                    Subjects: {quiz.subjects.join(', ')} <br/>
                                    Responses:
                                    <ul>
                                        {quiz.question_responses.map((response, index) => (
                                            <li key={index}>
                                                {questionMap[response.question_id] || 'Loading question...'}:
                                                {RESPONSE_MAPPINGS[response.response_id] || 'Invalid Response ID'}
                                            </li>
                                        ))}
                                    </ul>
                                </Typography>
                            </AccordionDetails>
                        </Accordion>
                    ))}
                </div>
            </Container>
        </>
    );
}

export default withAuthProtection(ProfilePage);
