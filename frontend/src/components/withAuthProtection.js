import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {checkLoginStatus} from "../utilities/checkLoginStatus";

export function withAuthProtection(WrappedComponent) {
    return function (props) {
        const [isLoggedIn, setIsLoggedIn] = useState(null);
        const navigate = useNavigate();

        useEffect(() => {
            checkLoginStatus(setIsLoggedIn);
        }, []);

        if (isLoggedIn === null) {
            return null; // or return a loader
        }

        if (!isLoggedIn) {
            navigate('/login'); // or wherever your login route is
            return null;
        }

        return <WrappedComponent {...props} />;
    };
}
