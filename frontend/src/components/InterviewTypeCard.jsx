import { Button, Card, CardContent, CardMedia } from '@mui/material';

function InterviewTypeCard({ interviewType, handleInterviewTypeClick, selectedInterviewType }) {
    return (
        <Card key={interviewType.name} style={{ margin: '10px', width: '300px' }} onClick={() => handleInterviewTypeClick(interviewType)} raised={selectedInterviewType === interviewType}>
            <CardMedia component="img" height="140" image={interviewType.image} alt={interviewType.name} />
            <CardContent>
                <h3>{interviewType.name}</h3>
                <p>{interviewType.short_description}</p>
            </CardContent>
            <Button variant="contained" onClick={() => handleInterviewTypeClick(interviewType)} style={{ margin: '10px' }}>Select</Button>
        </Card>
    );
}

export default InterviewTypeCard;