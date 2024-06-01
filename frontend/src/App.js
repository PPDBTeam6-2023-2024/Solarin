import './App.css';
import {BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import Login from './Login/Login'
import Game from './Game/Game'
import GameOver from './Game/GameOver'

function App() {
    return (
        <div className="App">
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Login/>}/>
                    <Route path="/game" element={<Game/>}/>
                    <Route path="/game-over" element={<GameOver/>}/>
                    <Route path="*" element={<Navigate to="/"/>}/>
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
