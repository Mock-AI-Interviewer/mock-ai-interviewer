import { Button, Container, FormControl, InputLabel, MenuItem, Select, TextareaAutosize } from "@mui/material";
import InterviewTypeCard from 'components/InterviewTypeCard';
import TopAppBar from "components/TopAppBar";
import PATHS from "paths";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const EXAMPLE_ENDPOINT = "https://example.com/interviews";
const mockInterviewTypes = [
    {
        name: "Competancy",
        short_description: "Competency-Based Interview",
        description: "In the Competency-Based Interview, candidates are assessed based on their past experiences and behaviors. Expect questions focused on key competencies such as teamwork, leadership, problem-solving, and technical skills. Candidates should be prepared to share specific examples from their past work that demonstrate these competencies.",
        image: "https://skillmetrics.net/wp-content/uploads/2021/09/depositphotos_45105951-stock-illustration-competence-concept-1.jpg",
        job_description: "Job Title: System Architect. Job Description: We are seeking an experienced System Architect to design and implement information systems that support our business goals. In this role, your primary responsibility will be to ensure the stability, integrity, and efficient operation of the information systems that support core organizational functions. Responsibilities include analyzing system requirements and ensuring that systems will be securely integrated with current applications; identifying, designing, and implementing technological solutions to meet business needs; working with a team of IT professionals and developers to produce new systems; ensuring consistent system documentation; and maintaining a high level of system architecture and infrastructure design. During the competency-based interview, we will assess your problem-solving skills, analytical thinking, technical expertise, communication skills, and ability to work in a team. Requirements: Proven experience as a System Architect or similar role; deep understanding of system architecture and design; experience with hardware and software systems; proficiency in programming languages and database management; strong analytical and problem-solving skills. Preferred Qualifications: Master’s degree in Computer Science or related field; professional certification in system architecture. Benefits: Competitive salary, health benefits, retirement plan, and opportunities for professional development. Application Instructions: If you are a strategic thinker, effective communicator, and experienced in system architecture, you are encouraged to apply.",
        init_prompt: "You are conducting a Competency-Based Interview for a [Job Title]. Your role is to assess the candidate's suitability for the position by exploring their past experiences and behaviors in professional settings. Ask the candidate questions about their problem-solving abilities, teamwork, leadership, and technical skills. After each response, provide feedback or follow-up questions to delve deeper into their competencies. Ensure the conversation is interactive and informative.",
    },
    {
        name: "Coding",
        short_description: "Coding Interview",
        description: "The Coding Interview evaluates the candidate's programming abilities and problem-solving skills. Candidates will be given coding problems to solve, typically focusing on algorithms, data structures, and logical thinking. Proficiency in a specific programming language may be required, and candidates should be prepared to explain their code and thought process.",
        image: "https://cdn.stackoverflow.co/images/jo7n4k8s/production/fb5b6974753c66ad9c51da025e715370a09f6531-2560x1344.jpg?w=1200&h=630&auto=format&dpr=2",
        job_description: "",
        init_prompt: "You are a senior software engineer conducting a coding interview. Your task is to evaluate the candidate's programming skills, problem-solving abilities, and understanding of algorithms and data structures. Present the candidate with coding challenges and ask them to write solutions in a specified programming language. After they respond, discuss their approach, suggest improvements, and ask follow-up questions to assess their depth of knowledge.",
    },
    {
        name: "Product Sense",
        short_description: "Product Sense Interview",
        description: "In a Product Sense Interview, the focus is on the candidate's understanding and intuition about product design and development. Candidates will discuss their approach to product-related scenarios, demonstrating their user empathy, creativity, and ability to balance user needs with business objectives. Expect questions about product strategy, design decisions, and problem-solving in a product context.",
        image: "https://www.productplan.com/uploads/2018/08/product-development.png",
        job_description: "",
        init_prompt: "You are conducting a Product Sense Interview for a product management role. Your objective is to understand the candidate's product intuition, user empathy, and strategic thinking. Present scenarios or problems related to product development and ask how they would approach these challenges. Discuss their responses, probing for insights into their decision-making process, creativity, and ability to balance user needs with business objectives.",
    },
];


function InterviewPage() {
    const navigate = useNavigate();
    const [interviewer, setInterviewer] = useState('');
    const [interviewTypes, setInterviewTypes] = useState([]);
    const [selectedInterviewType, setSelectedInterviewType] = useState(null);
    const [showJobDescription, setShowJobDescription] = useState(false);
    const [jobDescription, setJobDescription] = useState('');

    useEffect(() => {
        // Replace the actual fetch call with a mock response
        setInterviewTypes(mockInterviewTypes);
    }, []);

    // TODO uncomment this code when the backend is ready
    // useEffect(() => {
    //     fetch(EXAMPLE_ENDPOINT)
    //         .then(response => response.json())
    //         .then(data => setInterviewTypes(data))
    //         .catch(error => console.error(error));
    // }, []);

    const handleStartInterview = () => {
        navigate(PATHS.CONVERSATION, {
            state: {
                interviewType: selectedInterviewType,
                jobDescription: jobDescription
            }
        });
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
                <div style={{ borderTop: '2px solid #eee', margin: '20px 0' }}></div>
                <Button variant="contained" color="success" size="large" onClick={handleStartInterview} disabled={!selectedInterviewType}>
                    Start Interview
                </Button>
            </Container>
        </>
    );
}

export default InterviewPage;
