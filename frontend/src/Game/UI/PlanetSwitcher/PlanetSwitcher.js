import React, {useState, useContext} from 'react';

import {ViewModeContext, View} from "../../Context/ViewModeContext"
import WindowUI from '../WindowUI/WindowUI';
import {IoMdClose} from 'react-icons/io';

import {Resources} from '../ResourceViewer/ResourceViewer';
import {RiArrowLeftSLine, RiArrowRightSLine} from "react-icons/ri";
import {PlanetListContext} from "../../Context/PlanetListContext";



function PlanetSwitcher({planetIndex}) {
    /*This component displays The planet in the top and makes it possible to switch between planets*/

    const [planetList, setPlanetList] = useContext(PlanetListContext)

    const [hidePlanetSwitcherWindow, setHidePlanetSwitcherWindow] = useState(false)
    const [planetListIndex, setPlanetListIndex] = planetIndex
    return (
        <WindowUI hideState={hidePlanetSwitcherWindow} windowName="Planet Switcher">
            {/*Give the switcher a nice border*/}
            <div className='bg-gray-800 mx-auto w-3/12 py-3 fixed inset-x-0 top-5 z-10 border-2 border-white md:text-3xl'>

                {/*Make it possible to hide the component*/}
                <IoMdClose className="top-0 text-sm ml-1 absolute mt-1 left-0"
                           onClick={() => setHidePlanetSwitcherWindow(!hidePlanetSwitcherWindow)}/>


                <div className="justify-between items-center flex z-30">
                    {/*Display previous planet button*/}
                    <RiArrowLeftSLine className="transition ease-in-out hover:scale-150" onClick={() => {
                        /*
                        * Decrease the planet index by 1, if the index is < 1, do += planet size,
                        * to end up on the other side of the list and to give it a circular list effect
                        * */
                        let new_id = planetListIndex-1;
                        if (new_id < 0) {
                            new_id += planetList.length;
                        }
                        setPlanetListIndex(new_id)
                    }}/>
                    {/*Displays the planet name*/}
                    <h1>{planetList[planetListIndex].name}</h1>

                    {/*Display next planet button*/}
                    <RiArrowRightSLine className="transition ease-in-out hover:scale-150" onClick={() => {
                        /*
                        * Increase the planet index by 1, do a modulo operation with the length
                        * to create a circular list effect
                        * */
                        let new_id = planetListIndex + 1;
                        new_id = new_id % planetList.length;
                        setPlanetListIndex(new_id)
                    }}/>
                </div>
            </div>
        </WindowUI>
    )
}

export default PlanetSwitcher