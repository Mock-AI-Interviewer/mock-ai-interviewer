import React, { useState, useEffect } from "react";
import {Button, Container} from "@mui/material";
import { Link } from "react-router-dom";
import QuizIcon from '@mui/icons-material/Quiz';
import TopAppBar from "../components/TopAppBar";
import {checkLoginStatus} from "../utilities/checkLoginStatus";

function HomePage() {
    const [isLoggedIn, setIsLoggedIn] = useState(null);

    useEffect(() => {
        checkLoginStatus(setIsLoggedIn);
    }, []);

    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="md" style={{marginTop: '3%', textAlign: 'center'}}>
                <h1>Welcome to the A-Level Recommendation Quiz</h1>
                <img src={require("../assets/girl-reading-book.png")} alt="Girl Reading Book" className="homePageImage"/>
                <div className="homePageText">
                    <h3>Unlock Your Potential and Make Informed Choices</h3>
                    <p>
                        Choosing the right A-Level subjects is one of the most pivotal decisions you'll make on your educational journey.
                        For millions of students in the UK, this choice can be both daunting and uncertain.
                        We understand the significance of this decision, and we're here to make it easier for you!
                    </p>

                    <h3>Introducing Your A-Level Matching Tool</h3>
                    <p>
                        Our innovative web application is designed to empower GCSE students like you when navigating the A-Level selection process.
                        We offer a comprehensive solution to help you make informed choices about your future. Here's how it works:
                    </p>
                    <ol>
                        <li><b>Questionnaire:</b> Consisting of a series of 10 statements, assign a score to each statement depending on whether you agree or disagree. Answer honestly to gain accurate results.</li>
                        <li><b>Tailored Recommendations:</b> Our advanced algorithm takes your ranked statements and suggests A-Level subjects that align with your unique profile. It's like having a personal academic advisor right at your fingertips.</li>
                        <li><b>Set up a meeting with an academic advisor:</b> Set up a one-to-one meeting with a trained advisor to discuss your results and get the guidance you need to excel in your chosen A-Level subjects and confidently stride towards your higher education goals.</li>
                    </ol>

                    <h3>Why Facilitating Subjects Matter</h3>
                    <p>
                        Choosing facilitating subjects during your A-Levels opens up a world of opportunities.
                        These subjects are not just stepping-stones to a wide array of degree courses but also offer versatile career prospects.
                        Russell Group universities value them highly, making them a smart choice for your academic future.
                        That is why we have decided to focus on matching you to facilitating subjects, with 8 out of 9 subjects falling into this category.
                    </p>

                    <h3>Start Your Journey Today</h3>
                    <p>
                        Don't let uncertainty hold you back. Our A-Levels matching tool is here to help you pave the way to success… you just need to take the first step.
                        Your future is in your hands, and we're here to guide you along the way!
                    </p>
                </div>

                {isLoggedIn === false && (
                    <div style={{ margin: '20px 0' }}>
                        <Button variant="contained" color="primary" style={{ margin: '10px' }} component={Link} to="/login">
                            Login
                        </Button>
                        <Button variant="contained" color="secondary" style={{ margin: '10px' }} component={Link} to="/register">
                            Register
                        </Button>
                    </div>
                )}
                <Button variant="contained" startIcon={<QuizIcon />} component={Link} to="/quiz">
                    Take the Quiz
                </Button>
                <br/>
                <br/>
            </Container>
        </>
    );
}

export default HomePage;