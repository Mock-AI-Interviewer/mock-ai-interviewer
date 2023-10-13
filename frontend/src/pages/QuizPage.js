import React, {useEffect, useState} from 'react';
import {Button, Container, FormControl, FormControlLabel, Radio, RadioGroup, Typography} from '@mui/material';
import axios from 'axios';
import {BASE_API_ENDPOINT} from '../config';
import {useNavigate} from 'react-router-dom';
import ErrorMessage from '../components/ErrorMessage';
import TopAppBar from "../components/TopAppBar";
import ResponseMapBar from "../components/ResponseMapBar";

// The quiz ID to use for the quiz
const QUIZ_ID = 4;
function QuizPage() {
    const [quizId, setQuizId] = useState(null);
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState({});
    const [started, setStarted] = useState(false);
    const [error, setError] = useState(null);
    const [isSubmitEnabled, setIsSubmitEnabled] = useState(false);
    const [formKey, setFormKey] = useState(0);
    const history = useNavigate();

    useEffect(() => {
        // Check if all questions have been answered
        if (questions.length > 0 && Object.keys(responses).length === questions.length) {
            setIsSubmitEnabled(true);
        } else {
            setIsSubmitEnabled(false);
        }
    }, [responses, questions]);

    const startQuiz = async () => {
        setError(null);
        try {
            const {data} = await axios.get(`${BASE_API_ENDPOINT}/quizzes/${QUIZ_ID}`);
            const latestQuizId = data.quiz_id;
            setQuizId(latestQuizId);

            const quizData = await axios.get(`${BASE_API_ENDPOINT}/quizzes/${latestQuizId}`);
            setQuestions(quizData.data.questions);
            setStarted(true);
        } catch (error) {
            setError(error.message || 'An error occurred while fetching quiz data');
        }
    };

    const handleSubmit = async () => {
        setError(null);
        try {
            const questionResponses = Object.keys(responses).map(key => ({
                question_id: parseInt(key),
                response_id: responses[key]
            }));
            const {data} = await axios.post(`${BASE_API_ENDPOINT}/users/me/quiz_attempts`, {
                quiz_id: quizId,
                question_responses: questionResponses
            });
            history('/results', {state: {subjects: data.subjects}});
        } catch (error) {
            if (error.response.status === 401) {
                setError('You must be logged in to submit quiz responses');
            }
            else {
                setError(error.message || 'An error occurred while submitting quiz responses');
            }
        }
    };

    const handleChange = (questionId, value) => {
        setResponses(prev => ({
            ...prev,
            [questionId]: value
        }));
    };

    const resetForm = () => {
        setResponses({});
        setError(null);
        setFormKey(prevKey => prevKey + 1); // Increment form key to reset RadioGroup components
    };


    return (
        <>
            <TopAppBar/>
            <Container component="main" maxWidth="md" style={{marginTop: '8%', textAlign: 'center'}}>
                {!started ? (
                    <Button variant="contained" color="primary" onClick={startQuiz}
                            style={{fontSize: 'large', padding: '10px 20px'}}>Start Quiz</Button>
                ) : (
                    <div>
                        <Typography variant="h4" gutterBottom style={{marginBottom: '20px'}}>
                            Quiz Time!
                        </Typography>
                        <Typography variant="h6" gutterBottom>
                            Please answer the questions on using the scale below:
                        </Typography>
                        <ResponseMapBar />
                        <br/>
                        {questions.map(question => (
                            <FormControl component="fieldset" key={question.question_id} style={{ marginBottom: '20px', textAlign: 'center' }}>
                                <div style={{ marginBottom: '10px', textAlign: 'center' }}>
                                    <Typography variant="subtitle1" gutterBottom style={{ display: 'inline-block', textAlign: 'center' }}>
                                        {question.question}
                                    </Typography>
                                </div>
                                <div style={{ display: 'flex', justifyContent: 'center' }}>
                                    <RadioGroup row onChange={(e) => handleChange(question.question_id, parseInt(e.target.value))} key={formKey}>
                                        {[1, 2, 3, 4, 5].map(val => (
                                            <FormControlLabel key={val} value={val.toString()} control={<Radio />} label={val.toString()} />
                                        ))}
                                    </RadioGroup>
                                </div>
                            </FormControl>
                        ))}

                        <br/>
                        <div style={{display: 'flex', justifyContent: 'space-between'}}>
                            <Button variant="contained" onClick={resetForm}
                                    style={{backgroundColor: '#f0ad4e', marginTop: '20px'}}>Reset</Button>
                            <Button variant="contained" color="primary" onClick={handleSubmit} disabled={!isSubmitEnabled}
                                    style={{marginTop: '20px'}}>Submit</Button>
                        </div>
                    </div>
                )}
                {error && <ErrorMessage message={error} style={{marginTop: '20px'}}/>}
                <br/>
                <br/>
            </Container>
        </>
    );
}

export default QuizPage;
