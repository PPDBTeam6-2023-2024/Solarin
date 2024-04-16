import './ProfileViewer.css'
import React, {useContext, useState} from "react";
import {UserInfoContext} from "../../Context/UserInfoContext"
import axios from "axios";
import ProfileListEntry from "./ProfileListEntry";
import PoliticsMenu from "./PoliticsMenu";

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
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
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
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/armies_user`)
            setArmiesList(response.data)
        } catch (e) {
            setArmiesList([])
        }
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
                                                                        planet_id={c.planet_id}/>)}
                    </div>
                }

                {/*When armies tab selected, display a list of armies owner by the user*/}
                {selectedCategory === "Armies" &&
                    <div className="profile_viewer_list absolute"
                         style={{"overflowY": "scroll", "width": "80%", "height": "80%", "scrollbarWidth:": "none"}}>
                        {armiesList.map((c, index) => <ProfileListEntry key={index} text={`army ${c.id}`} type={"Army"}
                                                                        x={c.x} y={c.y}
                                                                        changePlanet={props.changePlanetByID}
                                                                        planet_id={c.planet_id}/>)}
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