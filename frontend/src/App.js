import './App.css';
import { useEffect } from 'react';
import axios from 'axios';

function App() {
  useEffect(() => {
      document.title = "Solarin";
      axios.get(`${process.env.REACT_APP_BACKEND_PATH}/hello`).then((response) => {
        console.log(response.data.message);
      })
  });
  
  return (
    <div className="App">
      <header className="App-header">
      <h1 className="text-5xl">SOLARIN</h1>
      <h3>Hello World</h3>
      </header>
    </div>
  );
}

export default App;
