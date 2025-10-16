import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || '/api';

const login = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/users/login/`, {
            username,
            password
        }, {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        });
        if (response.data.token) {
            localStorage.setItem('user', JSON.stringify(response.data));
            // Set the token for all future requests
            axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`;
        }
        return response.data;
    } catch (error) {
        throw error;
    }
};

const logout = async () => {
    try {
        const user = JSON.parse(localStorage.getItem('user'));
        if (user && user.token) {
            await axios.post(`${API_URL}/users/logout/`, {}, {
                headers: {
                    'Authorization': `Token ${user.token}`
                }
            });
        }
    } finally {
        localStorage.removeItem('user');
        delete axios.defaults.headers.common['Authorization'];
    }
};

const getCurrentUser = () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.token) {
        return null;
    }
    return user;
};

const getUserInfo = async () => {
    const user = getCurrentUser();
    if (!user) {
        throw new Error('No authenticated user');
    }

    try {
        const response = await axios.get(`${API_URL}/users/${user.user_id}/`, {
            headers: {
                'Authorization': `Token ${user.token}`
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

// Add axios interceptor to handle authentication
axios.interceptors.request.use(
    (config) => {
        const user = getCurrentUser();
        if (user && user.token) {
            config.headers.Authorization = `Token ${user.token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);


const authService = {
    login,
    logout,
    getCurrentUser,
    getUserInfo
};

export default authService;