import {useEffect, useState, Suspense, useRef} from "react"
import axios from 'axios'
import PlanetViewer from "./PlanetViewer/PlanetViewer"
import GalaxyViewer from "./GalaxyViewer/GalaxyViewer"
import UI from "./UI/UI"
import {ViewModeContext, View} from "./Context/ViewModeContext"
import ProfileViewer from "./UI/ProfileViewer/ProfileViewer";
import {RiArrowLeftSLine} from "react-icons/ri";
import {IoMdPlanet} from "react-icons/io";
import {UserInfoContext} from "./Context/UserInfoContext"

import {PlanetListContext} from "./Context/PlanetListContext"
import {useSelector, useDispatch} from 'react-redux'

const Game = () => {
    const [isAuth, setIsAuth] = useState(false)
    const [userInfo, setUserInfo] = useState(null)
    const [viewMode, setViewMode] = useState(View.PlanetView)
    const [planetList, setPlanetList] = useState([{"id": 1, "name": "Terra"}])
    const [planetListIndex, setPlanetListIndex] = useState(0)

    const resources = useSelector((state) => state.resources.resources)

    /*
    * Use a websocket to realtime update information about the maintenance of an army
    * */
    const [maintenanceWebsocket, setMaintenanceWebsocket] = useState(null);
    const isConnected = useRef(false);

    /*
    * To be able to simulate the change of maintenance live, will retrieve the maintenance rate and
    * mimic this on the frontend
    * */
    const [maintenanceCost, setMaintenanceCost] = useState([]);
    const [maintenanceCheckable, setMaintenanceCheckable] = useState(false);
    useEffect(() => {
        if (isConnected.current) return

        isConnected.current = true;

        const webSocket = new WebSocket(`${process.env.REACT_APP_BACKEND_PATH_WEBSOCKET}/logic/maintenance`,
            `${localStorage.getItem('access-token')}`);
        setMaintenanceWebsocket(webSocket);

        webSocket.onopen = () => {
            webSocket.send(
                JSON.stringify(
                    {
                        type: "get_maintenance_cost",
                    }))
        }

    }, []);

    /*make sure we wait a given time before being able to check the maintenance (to prevent high traffic usage)*/
    const checkable_maintenance = async(delay) => {
        await new Promise((resolve) => setTimeout(resolve, delay))
        setMaintenanceCheckable(true)
        check_maintenance()
    }

    const check_maintenance = async() =>{
        if (!maintenanceCheckable){return}

        let enough = true;
        maintenanceCost.forEach((element) => {
            if (resources[element[0]] <= 0){
                enough = false
            }
        })

        if (enough){return}
        maintenanceWebsocket.send(
        JSON.stringify(
            {
                type: "get_maintenance_cost",
        }))

    }

    /*
    * Handle maintenance websocket actions
    * */
    useEffect(() => {
        if (!maintenanceWebsocket) return;

        if (!isConnected.current) return

        maintenanceWebsocket.onmessage = (event) => {
            let data = JSON.parse(event.data)
            if (data.type === "update_cost") {
                setMaintenanceCost(data.maintenance_cost)
                checkable_maintenance(data.checkin)
            }

        };

        return () => {
            maintenanceWebsocket.close();
        };
    }, [maintenanceWebsocket]);

    const authenticate = async () => {
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/auth/me`)
            if (response.status === 200) {
                setIsAuth(true)
                setUserInfo(response.data)
            }
        } catch (error) {
            setIsAuth(false)
        }
    }

    const setPlanetListToDefault = async () => {
        setPlanetList([{"id": 1, "name": "Terra"}])
    }

    const getAllPlanets = async () => {
        /*retrieve a list of planet id's and planet names to switch between them*/
        try {
            /*Make sure the user sees the right planets*/
            const response2 = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/spawn`)

            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/planet/planets/private`)
            if (response.data.length > 0) setPlanetList(response.data)
            else await setPlanetListToDefault()

            changePlanetId(response2.data.planet_id);

        } catch (error) {
            await setPlanetListToDefault()
        }
    }

    const changePlanetId = (planetId) => {
        const newIndex = planetList.findIndex(planet => planet.id === planetId);
        if (newIndex !== -1) {
            setPlanetListIndex(newIndex);
        } else {
            console.error("Planet with the given ID not found.");
        }
    };


    useEffect(() => {
        authenticate()
        getAllPlanets()
    }, [])
    return (<div className="h-screen bg-gray-900">
        <UserInfoContext.Provider value={[userInfo, setUserInfo]}>
            <ViewModeContext.Provider value={[viewMode, setViewMode]}>
                <PlanetListContext.Provider value={[planetList, setPlanetList]}>

                    {userInfo && <Suspense fallback={<h1>Loading...</h1>}>
                        <UI/>
                        {viewMode === View.PlanetView &&
                            <>
                                <div onClick={() => setViewMode(View.GalaxyView)}
                                     className="fixed text-5xl z-10 transition ease-in-out hover:scale-150 hover:translate-x-5 hover:translate-y-1 duration-300 flex">
                                    <RiArrowLeftSLine className="basis-1/4"/>
                                    <IoMdPlanet/>
                                </div>
                                <PlanetViewer key={planetList[planetListIndex].id}
                                              planetName={planetList[planetListIndex].name}
                                              planetId={planetList[planetListIndex].id}
                                              planetListIndex={[planetListIndex, setPlanetListIndex]}/>
                            </>
                        }

                        {viewMode === View.GalaxyView &&
                            <GalaxyViewer setViewMode={setViewMode} planetListIndex={[planetListIndex, setPlanetListIndex]} changePlanetId={changePlanetId}/>
                        }

                        {viewMode === View.ProfileView &&
                            <ProfileViewer changePlanetByID={changePlanetId}/>
                        }

                    </Suspense>
                    }


                    {!userInfo && !isAuth && <h1>Not authenticated</h1>}

                </PlanetListContext.Provider>
            </ViewModeContext.Provider>
        </UserInfoContext.Provider>
    </div>)
}
export default Game