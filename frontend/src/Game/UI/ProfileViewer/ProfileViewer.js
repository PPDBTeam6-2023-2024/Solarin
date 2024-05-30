import './ProfileViewer.css'
import React, {useContext, useState} from "react";
import {UserInfoContext} from "../../Context/UserInfoContext"
import axios from "axios";
import ProfileListEntry from "./ProfileListEntry";
import PoliticsMenu from "./PoliticsMenu";
import Tooltip from "@mui/material/Tooltip";
import generalsJson from "../ArmyViewer/generals.json";
import {getCityImage} from "../../PlanetViewer/CityViewer/GetCityImage";
import {GetImagePath} from "./../../PlanetViewer/PlanetSVG"
function ProfileViewer(props) {

    /*Get access to the user Information*/
    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    /*
    * Indicates which category is currently selected
    * */
    const [selectedCategory, setSelectedCategory] = useState("");

    /*
    * Stores the list of cities owned by the user
    * */
    const [citiesList, setCitiesList] = useState([]);

    /*
    * Stores the list of armies owned by the user
    * */
    const [armiesList, setArmiesList] = useState([]);

    /*
    * Retrieve the cities from backend (owned by the user)
    * */
    const getCitiesPositions = async () => {
        /*get the list of all the requests to join the alliance*/
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/cities_user`)
            setCitiesList(response.data)
        } catch (e) {
            setCitiesList([])
        }
    }

    /*
    * Retrieve the armies from backend (owned by the user)
    * */
    const getArmiesPositions = async () => {
        /*get the list of all the requests to join the alliance*/
        try {
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/armies_user`)
            console.log("resp", response)
            setArmiesList(response.data)
        } catch (e) {
            setArmiesList([])
        }
    }

    /*
    * In the list view, we will pass popup widgets that w=ill be added to the list
    * */
    const getArmyPopups = (elem) =>{


        const popups = []
        if (elem.general !== null){
            {/*Display the general icon when the army has a general*/}
            const general = (<Tooltip title={`general ${elem.general.name} is assigned to this army`}>
                                <img style={{"width": "6vw", "height": "8vw"}}
                                     src={(`/images/general_images/${generalsJson[elem.general.name]["icon"]}`)}
                                             draggable={false}
                                             unselectable="on"/>
                            </Tooltip>);
            popups.push(general)
        }

        if (elem.city !== null){
            {/*Display the city icon when the army is in a city*/}
            const city = (<Tooltip title={`Army is in city ${elem.city} with city rank ${elem.city_rank}`}>
                                <img style={{"width": "8vw", "height": "8vw"}}
                                     src={getCityImage(elem.city_rank)}
                                             draggable={false}
                                             unselectable="on"/>
                            </Tooltip>);
            popups.push(city)

        }

        return popups

    }

    const getCityPopups = (elem) =>{
        const popups = []
        const city_rank = (<Tooltip title={`City rank ${elem.rank}`}>
                                <img style={{"width": "8vw", "height": "8vw"}}
                                     src={getCityImage(elem.rank)}
                                             draggable={false}
                                             unselectable="on"/>
                            </Tooltip>);

        popups.push(city_rank)

        const region_type = (<Tooltip title={`Region Type: ${elem.region_type}`}>
                                <img style={{"width": "8vw", "height": "8vw", "borderRadius": "50%"}}
                                     src={GetImagePath(elem.region_type)}
                                             draggable={false}
                                             unselectable="on"/>
                            </Tooltip>);

        popups.push(region_type)
        return popups
    }

    return (
        <>
            <div className="profile_viewer">
                <h1>Username: {userInfo.username}</h1>

                {/*list of buttons on the left: cities and armies (category tabs)*/}
                <div style={{"width": "15%", "height": "100%", "marginLeft": "1vw"}}>
                    <ul>
                        <div className="profile_viewer_category_button" onClick={() => {
                            setSelectedCategory("Cities");
                            getCitiesPositions();
                        }}>Cities
                        </div>
                        <div className="profile_viewer_category_button" onClick={() => {
                            setSelectedCategory("Armies");
                            getArmiesPositions();
                        }}>Armies
                        </div>
                        <div className="profile_viewer_category_button" onClick={() => {
                            setSelectedCategory("Politics");
                            getArmiesPositions();
                        }}>Politics
                        </div>
                    </ul>

                </div>

                {/*When cities tab selected, display a list of cities owner by the user*/}
                {selectedCategory === "Cities" &&
                    <div className="profile_viewer_list absolute"
                         style={{"overflowY": "scroll", "width": "80%", "height": "80%", "scrollbarWidth:": "none"}}>
                        {citiesList.map((c, index) => <ProfileListEntry key={index}
                                                                        text={`city ${c.id} on ${c.planet_name}`}
                                                                        type={"City"} x={c.x} y={c.y}
                                                                        changePlanet={props.changePlanetByID}
                                                                        planet_id={c.planet_id} popups={getCityPopups(c)}/>)}
                    </div>
                }

                {/*When armies tab selected, display a list of armies owner by the user*/}
                {selectedCategory === "Armies" &&
                    <div className="profile_viewer_list absolute"
                         style={{"overflowY": "scroll", "width": "80%", "height": "80%", "scrollbarWidth:": "none"}}>
                        {armiesList.map((c, index) => <ProfileListEntry key={index} text={`army ${c.id}`} type={"Army"}
                                                                        x={c.x} y={c.y}
                                                                        changePlanet={props.changePlanetByID}
                                                                        planet_id={c.planet_id} popups={getArmyPopups(c)}/>)}
                    </div>
                }

                {/*When politics tab selected, display the politics menu*/}
                {selectedCategory === "Politics" &&
                    <div className="profile_viewer_list absolute"
                         style={{"overflowY": "scroll", "width": "80%", "height": "80%", "scrollbarWidth:": "none"}}>
                        <PoliticsMenu/>
                    </div>}

            </div>

        </>
    )
}

export default ProfileViewer