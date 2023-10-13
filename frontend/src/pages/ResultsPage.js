import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Typography, Card, CardContent, Button } from '@mui/material';
import TopAppBar from "../components/TopAppBar";

function ResultsPage() {
    const [showInfo, setShowInfo] = useState(false);

    const location = useLocation();
    const subjects = location.state ? location.state.subjects : [];

    const materialColors = [
        'primary.main',
        'secondary.main',
        'error.main',
        'warning.main',
        'info.main',
        'success.main'
    ];

    const getRandomMaterialColor = () => {
        return materialColors[Math.floor(Math.random() * materialColors.length)];
    };

    const subjectInfo = [
        {
            title: "History",
            description: "Travel back in time to understand the events that shaped our world. A-Level History enhances research, critical thinking, and storytelling abilities, allowing you to analyse historical events from multiple perspectives. Dive into ancient civilizations, explore the intricacies of world wars, and prepare for careers as historians, educators, or curators preserving our shared heritage."
        },
        {
            title: "Art and Design",
            description: "Unleash your creativity and artistic expression. A-Level Art and Design foster visual thinking, creativity, and self-expression, allowing you to leave your mark on the world as an artist, graphic designer, or architect. Explore various mediums, from traditional painting to digital design, and learn how your artistic talents can shape industries, landscapes, and experiences in today's visually driven society."
        },
        {
            title: "Modern Languages",
            description: "Immerse yourself in the richness of language and culture. A-Level Modern Languages offer fluency, cultural appreciation, and global communication skills, crucial in our interconnected world. From becoming a global business leader to bridging diplomatic relations or helping people connect across borders, mastering a language opens doors to diverse opportunities."
        },
        {
            title: "Maths",
            description: "A-Level Mathematics will immerse you in the world of numbers, calculus, and problem-solving. Develop analytical skills, logical thinking, and mathematical precision. Ideal for students with a knack for problem-solving, aspiring engineers, economists, and data scientists."
        },
        {
            title: "Chemistry",
            description: "Explore the fundamental principles governing chemical processes at the atomic and molecular level. A-level Chemistry provides rigorous training in analytical and experimental techniques, equipping you for careers as chemists in research and development, pharmaceutical scientists involved in drug discovery, or environmental scientists focused on sustainability and pollution control. Your proficiency in chemistry will be invaluable in solving real-world challenges and contributing to scientific advancements."
        },
        {
            title: "Physics",
            description: "Dive deep into the laws governing space, gain insights into the behaviour of particles and the forces that shape our world, both macroscopically and at the quantum level. This course not only sharpens your problem-solving skills but also nurtures analytical thinking as you tackle complex phenomena. With A-Level Physics as your foundation, you'll be well-prepared for exciting career paths in physics research, engineering, space exploration, or emerging fields like quantum computing, where your understanding of the fundamental laws of nature will drive innovation and discovery."
        },
        {
            title: "Biology",
            description: "In A-Level Biology, you will study the intricacies of living organisms, genetics, and ecosystems. The curriculum emphasizes practical experimentation and observational skills development. With a foundation in A-Level Biology, you'll be well-prepared to pursue careers in fields such as biology research, medicine, environmental conservation, or even biotechnology, where your understanding of life's intricacies will drive meaningful contributions to science and healthcare."
        },
        {
            title: "English Lit",
            description: "Journey through the rich tapestry of human storytelling, examining the profound themes that transcend time and culture. This course sharpens your ability to critically dissect literature, fostering a deep appreciation for the power of words. As you explore the works of literary giants, you'll not only refine your analytical skills but also develop a keen insight into human nature, making it an ideal foundation for careers in literature, journalism, publishing, or any field where effective communication is paramount."
        },
        {
            title: "Geography",
            description: "In A-Level Geography, you'll delve into the dynamic relationship between human societies and the environment, exploring topics like sustainable development, climate change, and urbanization. This course equips you with valuable fieldwork experience, fostering a deep understanding of the world's diverse ecosystems and cultures. Aspiring geographers often find rewarding careers in environmental consultancy, disaster management, or shaping sustainable urban landscapes, where their expertise in analysing complex global challenges is in high demand."
        }
    ];

    return (
        <>
            <TopAppBar/>
            <Container component="main" maxWidth="md" style={{ padding: '20px' }}>
                <Typography variant="h4" gutterBottom style={{ marginBottom: '20px' }}>
                    Recommended Subjects
                </Typography>
                {subjects.length ? (
                    subjects.map((subject, index) => (
                        <Card key={index} sx={{ marginBottom: '20px', backgroundColor: getRandomMaterialColor() }}>
                            <CardContent>
                                <Typography variant="h6" style={{ color: '#fff' }}>
                                    {subject}
                                </Typography>
                            </CardContent>
                        </Card>
                    ))
                ) : (
                    <Typography variant="subtitle1" color="textSecondary">
                        No recommendations available
                    </Typography>
                )}
                <Button variant="contained" onClick={() => setShowInfo(prev => !prev)}>
                    {showInfo ? 'Hide' : 'Show'} More Info About Subjects
                </Button>
                {showInfo && (
                    <div style={{ marginTop: '20px' }}>
                        {subjectInfo.map((info, index) => (
                            <Card key={index} style={{ marginBottom: '20px' }}>
                                <CardContent>
                                    <Typography variant="h6">
                                        {info.title}
                                    </Typography>
                                    <Typography variant="body1">
                                        {info.description}
                                    </Typography>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                )}
            </Container>
        </>
    );
}

export default ResultsPage;
