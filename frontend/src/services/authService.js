import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || '/api';

const login = async (username, password) => {
    try {
        const response = await axios.post(`${API_URL}/login/`, {
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
        }
        return response.data;
    } catch (error) {
        throw error;
    }
};

const getUserInfo = async () => {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user || !user.token) {
        throw new Error('No authenticated user');
    }

    try {
        const response = await axios.get(`${API_URL}/user/`, {
            headers: {
                'Authorization': `Token ${user.token}`
            }
        });
        return response.data;
    } catch (error) {
        throw error;
    }
};

const logout = () => {
    localStorage.removeItem('user');
};

const authService = {
    login,
    logout,
    getUserInfo
};

export default authService;