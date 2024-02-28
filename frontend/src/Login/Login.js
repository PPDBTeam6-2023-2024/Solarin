import { useEffect, useState } from 'react';
import axios from 'axios';
import qs from 'qs'
import ParticlesApp from './Particles.js'
import {Animated} from "react-animated-css";
import { useNavigate } from 'react-router-dom';
/**
 * The login and (currently) the home page
 * @returns app login/home component
 */
function Login() {  
  const [clickedSignIn, setClickedSignIn] = useState(true)
  const [signError, setSignError] = useState(null)
  const [isSignedIn, setIsSignedIn] = useState(false)

  const navigate = useNavigate()
  const onClickPlay = async() => {
    navigate("/game", {shallow: true})
  }

  const signOut = async() => {
    setIsSignedIn(false) 
    localStorage.clear()
  }

  useEffect(() => {
      const token = localStorage.getItem("access-token")
      if(token) setIsSignedIn(true)
  })

  /**
   * communicates with the backend to either sign in or sign up by sending post requests using axios
   * @param {*} event information filled in the form after clicking on sign in or sign up
   */
  const handleSubmit = async(event) => {
      await event.preventDefault()
      let username = event.target.username.value
      let password = event.target.password.value
      let email = event.target.email.value
      if(clickedSignIn) {
        try {
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/auth/token`, qs.stringify({
          "username": username,
          "password": password 
        }), 
        { 
          headers: {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
          },
        })
        if(response.status === 200) {
          setSignError(null)
          setIsSignedIn(true)
          localStorage.setItem("access-token", response.data.access_token)
          axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        }
        }
        catch(error) {
          setSignError(error.response.data.detail)
        }
      }
      else {
        try {
        const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/auth/add_user`, JSON.stringify({
          "email": email,
          "username": username,
          "password": password 
        }), 
        { 
          headers: {
            'content-type': 'application/json',
            'accept': 'application/json',
          },
        })
        if(response.status === 200) {
          setSignError(null)
        }
        }
        catch(error) {
          setSignError(error.response.data.detail)
        }
      }
  }
  return (
    <div className="App">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/3.5.2/animate.min.css"/> 
        <ParticlesApp></ParticlesApp>
        <div className="min-h-screen flex justify-center text-center z-10">
        <div className="mt-20">
        <Animated animationIn="fadeInDownBig" animationOut="fadeOut" isVisible={true}>
        <h1 className="text-9xl">SOLARIN</h1>
        </Animated>
        
    <div className="sm:mx-auto sm:w-full sm:max-w-sm">
  </div>
  <Animated animationIn="zoomIn" animationOut="fadeOut" isVisible={true}>
  { !isSignedIn &&
  <div className="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
    <form className="space-y-6" method="POST" onSubmit={handleSubmit}>
      <div className="grid gap-6 mb-6 md:grid-cols-2">
        <div className="mt-2">
          <label className="block text-sm font-medium leading-6 text-white-900">Username</label>
          <input id="username" type="text" name="username" required className="block w-full p-3 rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-white-400 focus:ring-2 focus:ring-inset focus:ring-white-600 sm:text-sm sm:leading-6"/>
        </div>
        <div className="mt-2">
          <label className="block text-sm font-medium leading-6 text-white-900">Email</label>
          <input id="email" type="email" name="email" required className="block w-full p-3 rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-white-400 focus:ring-2 focus:ring-inset focus:ring-white-600 sm:text-sm sm:leading-6"/>
        </div>
      </div>

      <div>
        <div>
          <label className="block text-sm font-medium leading-6 text-white-900">Password</label>
        </div>
        <div className="mt-2">
          <input id="password" name="password" type="password" required className="block w-full p-3 rounded-md border-0 py-1.5 text-black shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-white-400 focus:ring-2 focus:ring-inset focus:ring-white-600 sm:text-sm sm:leading-6"/>
        </div>
      </div>

      <div>
        <input type="submit" onClick={() => setClickedSignIn(true)}value="Sign In" className="justify-center rounded-md bg-transparent hover:bg-white hover:text-black px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-white-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white-600"/>
        <input type="submit" onClick={() => setClickedSignIn(false)}value="Sign Up" className="justify-center rounded-md bg-transparent hover:bg-white hover:text-black px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-white-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white-600"/>
      </div>
    </form>
    {signError && <h4 className="text-red-500">{signError}</h4>}
  </div>
  }
  </Animated>
  { isSignedIn &&
        <Animated animationIn="flipInY" animationOut="fadeOut" isVisible={true} animationInDuration={500}>
        <button onClick={onClickPlay} className="mt-10 bg-transparent hover:bg-white text-white-700 font-semibold hover:text-black py-6 px-20 border border-white-500 rounded text-5xl">
        PLAY
        </button>
        <br/>
        <button onClick={signOut} value="Sign Out" className="my-3 justify-center rounded-md bg-transparent hover:bg-white hover:text-black px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-white-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white-600">
        Sign out
        </button>
        </Animated>
  }
        </div>   
    </div>
    </div>
  );
}

export default Login;
