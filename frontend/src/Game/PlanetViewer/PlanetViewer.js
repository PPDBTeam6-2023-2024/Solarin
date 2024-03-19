import { RiArrowLeftSLine, RiArrowRightSLine } from "react-icons/ri";
import PlanetSVG from "./PlanetSVG";


function PlanetViewer(props) {
    return (
        <>
        <div className="bg-gray-800 mx-auto w-2/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl justify-between items-center flex">
            <RiArrowLeftSLine className="transition ease-in-out hover:scale-150"/>
            <h1>{props.planetName}</h1>
            <RiArrowRightSLine className="transition ease-in-out hover:scale-150"/>
        </div>
        <PlanetSVG data={props.data}/>
        </>
    );
}

export default PlanetViewer;
