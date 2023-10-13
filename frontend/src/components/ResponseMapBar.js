import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { RESPONSE_MAPPINGS } from '../utilities/responseMapping';  // Adjust the path according to your project structure
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles({
    card: {
        borderRadius: '15px',
        display: 'flex',
        justifyContent: 'space-around',
        alignItems: 'center',
        background: '#f7f7f7',
    },
    legendItem: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
    },
});

function ResponseMapBar() {
    const classes = useStyles();

    return (
        <Card className={classes.card} style={{backgroundColor: "lightgrey"}}>
            <CardContent>
                {Object.entries(RESPONSE_MAPPINGS).map(([key, value]) => (
                    <div key={key} className={classes.legendItem}>
                        <Typography variant="body2">{key}:{value}</Typography>
                    </div>
                ))}
            </CardContent>
        </Card>
    );
}

export default ResponseMapBar;
