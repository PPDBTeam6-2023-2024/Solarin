import './ProfileViewer.css'
import React, {useContext, useState} from "react";
import {ViewModeContext} from "../../Context/ViewModeContext";
import {UserInfoContext} from "../../Context/UserInfoContext"
import axios from "axios";
import Message from "../ChatMenu/Message";
import ProfileListEntry from "./ProfileListEntry";

function ProfileViewer() {

    const [userInfo, setUserInfo] = useContext(UserInfoContext)

    const [selectedCategory, setSelectedCategory] = useState("");

    const [citiesList, setCitiesList] = useState([]);
    const [armiesList, setArmiesList] = useState([]);

    const getCitiesPositions = async() => {
        /*get the list of all the requests to join the alliance*/
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/cities_user`)
            setCitiesList(response.data)
        }
        catch(e) {setCitiesList([])}
    }

    const getArmiesPositions = async() => {
        /*get the list of all the requests to join the alliance*/
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/armies_user`)
            setArmiesList(response.data)
        }
        catch(e) {setArmiesList([])}
    }

    return (
        <>
            <div className="profile_viewer">
                <h1>Username: {userInfo.username}</h1>

                <div style={{"width":"15%", "height": "100%", "marginLeft": "1vw"}} >
                    <ul>
                        <div className="profile_viewer_category_button" onClick={() => {setSelectedCategory("Cities"); getCitiesPositions();}}>Cities</div>
                        <div className="profile_viewer_category_button" onClick={() => {setSelectedCategory("Armies"); getArmiesPositions();}}>Armies</div>
                    </ul>

                </div>

                {selectedCategory === "Cities" &&
                    <div className="profile_viewer_list absolute" style={{"overflow-y": "scroll", "width":"80%", "height": "80%", "scrollbarWidth:": "none"}} >
                        {citiesList.map((c, index) => <ProfileListEntry key={index} text={`city ${c.id} on ${c.planet_name}`} type={"City"} x={c.x} y={c.y}/>)}
                    </div>
                }

                {selectedCategory === "Armies" &&
                    <div className="profile_viewer_list absolute" style={{"overflow-y": "scroll", "width":"80%", "height": "80%", "scrollbarWidth:": "none"}} >
                        {armiesList.map((c, index) => <ProfileListEntry key={index} text={`army ${c.id}`} type={"Army"} x={c.x} y={c.y}/>)}
                    </div>
                }

            </div>

        </>
    )
}

export default ProfileViewer