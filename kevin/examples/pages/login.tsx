import React from 'react';
import LoginForm from '../components/LoginPage'

const LoginPage = () => {
  const handleLogin = (event: React.FormEvent<HTMLFormElement>) => {
    // Handle login logic here, for example:
    console.log('Handling login...');
  };

  return (
    <div>
      <h1>Login Page</h1>
      <LoginForm onLogin={handleLogin} />
    </div>
  );
};

export default LoginPage;
