import axios from 'axios';

// Create a central axios instance pointing to our environment API URL
const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request Interceptor: Automatically attach JWT Bearer token if available
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token'); // Or whatever key your auth uses
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;