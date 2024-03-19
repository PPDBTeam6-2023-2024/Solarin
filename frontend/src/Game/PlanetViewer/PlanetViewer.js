import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";
import PlanetSVG from "./PlanetSVG";


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

function PlanetViewer(props) {
    return (
        <>
        <div className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex">
            <RiArrowLeftSLine className="transition ease-in-out hover:scale-150"/>
            <h1>{props.planetName}</h1>
            <RiArrowRightSLine className="transition ease-in-out hover:scale-150"/>
        </div>
        <div style={{position:"relative", height:"100vh", width: "100vw"}}>
            <PlanetSVG data={generateData(2, 2)}/>
        </div>
        </>
    );
}

export default PlanetViewer;
