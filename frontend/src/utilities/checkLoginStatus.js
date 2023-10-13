import axios from 'axios';
import { BASE_API_ENDPOINT } from '../config';

export const checkLoginStatus = async (setIsLoggedInCallback) => {
    try {
        const response = await axios.get(`${BASE_API_ENDPOINT}/authenticated-route`, {
            withCredentials: true
        });
        if(response.status === 200) {
            setIsLoggedInCallback(true);
        } else {
            setIsLoggedInCallback(false);
        }
    } catch (error) {
        console.error(error);
        setIsLoggedInCallback(false);
    }
};