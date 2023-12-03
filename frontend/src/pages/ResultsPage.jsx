import { Box, CircularProgress, Container, Grid, Typography, useMediaQuery, useTheme, Card, CardContent } from "@mui/material";
import TopAppBar from "components/TopAppBar";
import PATHS from "paths";
import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { config } from 'appConfig';
import { styled } from '@mui/material/styles';

function ResultsPage() {
    const { state } = useLocation();
    const interviewId = state?.interviewId;
    const [loading, setLoading] = useState(true);
    const [interviewResults, setInterviewResults] = useState({});
    const INTERVIEW_RESULTS_ENDPOINT = `${config.backendApiUrl}/interview/session/${interviewId}/review`
    const navigate = useNavigate();

    const theme = useTheme();
    const matches = useMediaQuery(theme.breakpoints.up('md'));

    useEffect(() => {
        if (!interviewId) {
            navigate(PATHS.HOME);
        }
    }, [interviewId, navigate]);

    useEffect(() => {
        fetch(INTERVIEW_RESULTS_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => response.json())
            .then(data => {
                setInterviewResults(data.review);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching interview results:', error);
                setLoading(false);
            });
    }, [interviewId]);

    // Styled Score Circle
    const ScoreCircle = styled(Box)(({ theme }) => ({
        width: 200,
        height: 200,
        borderRadius: '50%',
        backgroundColor: theme.palette.primary.main,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        color: theme.palette.primary.contrastText,
        fontSize: '3rem',
        animation: 'scorePulse 2s infinite',
        '@keyframes scorePulse': {
            '0%': { transform: 'scale(1)' },
            '50%': { transform: 'scale(1.1)' },
            '100%': { transform: 'scale(1)' },
        }
    }));

    const LoadingComponent = () => (
        <Grid container style={{ height: '100%' }} justifyContent="center" alignItems="center">
            <Grid item>
                <CircularProgress size={100} />
                <Typography variant="h6" style={{ marginTop: '1em' }}>Loading Interview Results...</Typography>
            </Grid>
        </Grid>
    );

    return (
        <>
            <TopAppBar />
            <Container component="main" maxWidth="lg" style={{
                height: 'calc(100vh - 64px)',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                textAlign: 'center'
            }}>
                {loading ? (
                    <LoadingComponent />
                ) : (
                    <Box display="flex" flexDirection={matches ? "row" : "column"} alignItems="center" justifyContent="center" style={{ width: '100%' }}>

                        <Box style={{ textAlign: 'center', margin: '2em 0', flex: 1 }}>
                            <Typography variant="h4" style={{ marginBottom: '1em' }}>Interview Results</Typography>
                            <ScoreCircle>
                                {interviewResults.score}
                            </ScoreCircle>
                            <Card variant="outlined" style={{ marginTop: '2em' }}>
                                <CardContent>
                                    <Typography variant="body1">{interviewResults.feedback}</Typography>
                                </CardContent>
                            </Card>
                        </Box>
                    </Box>
                )}
            </Container>
        </>
    );
}

export default ResultsPage;
