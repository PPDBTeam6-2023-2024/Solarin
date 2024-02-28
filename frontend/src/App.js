import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from './Login/Login'
import Game from './Game/Game'
function App() {  
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />}/>
        <Route path="/game" element={<Game />}/>
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
