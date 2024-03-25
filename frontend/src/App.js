import './App.css';
import PlanetSVG from './Game/PlanetViewer/PlanetSVG';
import { MapInteractionCSS } from 'react-map-interaction';
import { useState } from 'react';


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
const data = generateData(10,10);


function App() {  
    const [mapState, setMapState] = useState({
      scale: 1,
      translation: {x: 0, y: 0},
  });
  
  return (
    <MapInteractionCSS
              value={mapState}
              onChange={(value) => setMapState(value)}
              minScale={1}
              maxScale={5}
              translationBounds={{
                  xMin: 1920 - mapState.scale * 1920,
                  xMax: 0,
                  yMin: 1080 - mapState.scale * 1080,
                  yMax: 0,
              }}
          >
          <PlanetSVG data={data} />
      </MapInteractionCSS>
  );
}

export default App;