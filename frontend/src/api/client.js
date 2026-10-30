import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000', // Match localhost instead of 127.0.0.1
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

export default api;