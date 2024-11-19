import React from 'react';

interface Props {}

const LoginPage = ({}: Props) => {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Handle form submission logic here
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <label>Username:</label> {/* updated from "Email:" to "Username:" */}
        <input type="text" name="username" />
        <br />
        <label>Password:</label>
        <input type="password" name="password" />
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default LoginPage;
