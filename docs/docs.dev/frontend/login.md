# Login Page

## Overview
The user is able to sign up, sign in, and sign out.

## Technologies used
- ReactJS
 - react-animated-css
 - ParticlesJS
 - react-router-dom
- Axios
- TailwindCSS

## Description
The login page is decorated with an interactive particles background. 
The user needs to type in his username, email, and password to sign up but the email will not be checked for the sign in.
When a user signs up successfully, It will also directly let the user log in.

<br>![alt text](../images/login.png)

After successfully signing in the access token will be stored in the local storage, and a clickable play button will appear along with a sign out button.
The sign out button does nothing more than remove the access token from the local storage. 

<br>![alt text](../images/logged_in.png)

## Potential Issues
Of course, if the backend is down then the user will not be able to sign in or sign up through the frontend.
