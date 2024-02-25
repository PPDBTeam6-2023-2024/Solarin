import './App.css';
import { useEffect, useState } from 'react';
import axios from 'axios';
import qs from 'qs'
import ParticlesApp from './Particles.js'
function App() {  
  const [isSignIn, setIsSignIn] = useState(true)
  const [signError, setSignError] = useState(null)


  document.title = "Solarin"
  const handleSubmit = async(event) => {
    event.preventDefault()
      let username = event.target.username.value
      let password = event.target.password.value
      let email = event.target.email.value
      if(isSignIn) {
        axios.post(`${process.env.REACT_APP_BACKEND_PATH}/auth/token`, qs.stringify({
          "username": email,
          "password": password 
        }), 
        { 
          headers: {
            'content-type': 'application/x-www-form-urlencoded',
            'accept': 'application/json',
          },
        }).then(response => {
            console.log(response)
        })
        .catch(error => {
            setSignError(error.response.data.detail)
        })
      }
      else {
        axios.post(`${process.env.REACT_APP_BACKEND_PATH}/auth/add_user`, JSON.stringify({
          "email": email,
          "username": username,
          "password": password 
        }), 
        { 
          headers: {
            'content-type': 'application/json',
            'accept': 'application/json',
          },
        }).then(response => {
            if(response.status == 200) {
               
            }
        })
        .catch(error => {
            setSignError(error.response.data.detail)
        })
      }
  }
  return (
    <div className="App">
          <ParticlesApp></ParticlesApp>
        <div className="min-h-screen flex justify-center text-center z-10">
        <div className="mt-20">
        <h1 className="text-9xl">SOLARIN</h1>
        
    <div className="sm:mx-auto sm:w-full sm:max-w-sm">
  </div>

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
        <input type="submit" onClick={() => setIsSignIn(true)}value="Sign In" className="justify-center rounded-md bg-transparent hover:bg-white hover:text-black px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-white-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white-600"/>
        <input type="submit" onClick={() => setIsSignIn(false)}value="Sign Up" className="justify-center rounded-md bg-transparent hover:bg-white hover:text-black px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-white-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white-600"/>
      </div>
    </form>
    <h4 className="text-red-500">{signError}</h4>
  </div>
        <button className="mt-10 bg-transparent hover:bg-white text-white-700 font-semibold hover:text-black py-6 px-20 border border-white-500 rounded text-5xl">
        PLAY
        </button>
        </div>
    </div>
    </div>
  );
}

export default App;
