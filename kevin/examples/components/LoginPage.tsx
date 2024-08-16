import React from 'react';

interface LoginFormProps {
  onLogin: (event: React.FormEvent<HTMLFormElement>) => void;
}

const LoginPage = ({ onLogin }: LoginFormProps) => {
  const handleLoginSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    onLogin(event);
  };

  return (
    <div className="login-container">
      <form onSubmit={handleLoginSubmit}>
        <label>Email:</label>
        <input type="email" name="email" />
        <br />
        <label>Password:</label>
        <input type="password" name="password" />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
