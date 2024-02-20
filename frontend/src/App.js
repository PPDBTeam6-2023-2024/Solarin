import './App.css';
import { useEffect } from 'react';

function App() {
  useEffect(() => {
      document.title = "Solarin";
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
