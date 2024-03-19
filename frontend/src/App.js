import './App.css';
import PlanetViewer from './Game/PlanetViewer/PlanetViewer';

function generateData(width, height) {
  const data = [];
  const cellWidth = 1 / width;
  const cellHeight = 1 / height;

  for (let i = 0; i < height; i++) {
    for (let j = 0; j < width; j++) {
      const x = Math.random() * cellWidth + j * cellWidth;
      const y = Math.random() * cellHeight + i * cellHeight;
      const types = ['type1', 'type2', 'type3']
      const regionType = types[Math.floor(Math.random()*types.length)];
      data.push({ x, y, regionType });
    }
  }

  return data;
}

function App() {  
  const data = generateData(5, 5);

  return (
    <div className="App">
      <PlanetViewer data={data} planetName="test"/>
    </div>
  );
}

export default App;
