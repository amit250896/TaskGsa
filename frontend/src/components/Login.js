import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios'

function Login() {

  const navigate = useNavigate()
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const [trigger , setTrigger ] = useState(false);
  const [usernameReg , setUsernameReg] = useState("");
  const [passwordReg , setPasswordReg] = useState("");



  const handleSubmit = (e) => {

    const config = {
      method: "post",
      url: "http://127.0.0.1:5000/api/auth/login",
      headers: {
        "Content-Type": "application/json",
        // Authorization: `Bearer ${getLocalStorageData("access_token")}`,
      },
      data: {username:username , password:password}
    };


    axios(config)
    .then(res => {
      window.location.replace("/dashboard")
    })
    .catch(err => alert(err))
  
  };

  const handleSubmitForReg = () => {

    const config = {
      method: "post",
      url: "http://127.0.0.1:5000/api/auth/register",
      headers: {
        "Content-Type": "application/json",
        // Authorization: `Bearer ${getLocalStorageData("access_token")}`,
      },
      data: {username:usernameReg , password:passwordReg}
    };


    axios(config)
    .then(res => {
      setTrigger(false)
    })
    .catch(err => alert(err))

  }

  return (
    <>
    <div>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Login</button>
      </form>
    </div>
    <p onClick={() => setTrigger(!trigger)}>register</p>

    {trigger && (
      <form onSubmit={handleSubmitForReg}>
      <input
        type="text"
        placeholder="Username"
        value={usernameReg}
        onChange={(e) => setUsernameReg(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={passwordReg}
        onChange={(e) => setPasswordReg(e.target.value)}
      />
      <button type="submit">Register</button>
    </form>
    ) }
    </>
  );
}

export default Login;
