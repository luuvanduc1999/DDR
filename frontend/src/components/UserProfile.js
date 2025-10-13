import React, { useEffect, useState } from 'react';
import authService from '../services/authService';

const UserProfile = ({ onLogout }) => {
    const [userInfo, setUserInfo] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchUserInfo = async () => {
            try {
                const data = await authService.getUserInfo();
                setUserInfo(data);
            } catch (err) {
                setError('Failed to fetch user information');
            }
        };

        fetchUserInfo();
    }, []);

    const handleLogout = () => {
        authService.logout();
        onLogout();
    };

    if (error) {
        return <div className="error-message">{error}</div>;
    }

    if (!userInfo) {
        return <div>Loading...</div>;
    }

    return (
        <div className="profile-container">
            <h2>User Profile</h2>
            <div className="user-info">
                <p><strong>Username:</strong> {userInfo.username}</p>
                <p><strong>Email:</strong> {userInfo.email}</p>
                {/* Add more user information fields as needed */}
            </div>
            <button onClick={handleLogout}>Logout</button>
        </div>
    );
};

export default UserProfile;