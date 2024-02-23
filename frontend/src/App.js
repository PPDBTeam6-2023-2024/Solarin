import './App.css';
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [msg, setMsg] = useState('Pending...');
  useEffect(() => {
      document.title = "Solarin";
      axios.get(`${process.env.REACT_APP_BACKEND_PATH}/hello`).then((response) => {
        setMsg(response.data.message);
      })
  });
  
  return (
    <div className="App">
      <header className="App-header">
      <h1 className="text-5xl">SOLARIN</h1>
      <h3>{msg}</h3>
      </header>
    </div>
  );
}

export default App;
