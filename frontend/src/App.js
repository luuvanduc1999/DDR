import React, { useState, useEffect } from 'react';
import './App.css';
import Login from './components/Login';
import UserProfile from './components/UserProfile';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const user = localStorage.getItem('user');
    if (user) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    setIsAuthenticated(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Admin Site</h1>
      </header>
      <main>
        {!isAuthenticated ? (
          <Login onLoginSuccess={handleLoginSuccess} />
        ) : (
          <UserProfile onLogout={handleLogout} />
        )}
      </main>
    </div>
  );
}

export default App;
