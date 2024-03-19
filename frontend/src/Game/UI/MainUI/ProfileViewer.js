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

    const getCitiesPositions = async(planetId) => {
        /*get the list of all the requests to join the alliance*/
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/cities?planet_id=${planetId}`)
            setCitiesList(response.data)

        }
        catch(e) {setCitiesList([])}
    }

    return (
        <>
            <div id="profile_viewer">
                <h1>Username: {userInfo.username}</h1>

                <div style={{"width":"9%", "height": "100%", "marginLeft": "5vw"}} >
                    <ul>
                        <div className="profile_viewer_category_button" onClick={() => {setSelectedCategory("Cities"); getCitiesPositions(1);}}>Cities</div>
                        <div className="profile_viewer_category_button" onClick={() => setSelectedCategory("Armies")}>Armies</div>
                    </ul>

                </div>

                {selectedCategory === "Cities" &&
                    <div className="profile_viewer_list absolute right-0" style={{"overflow-y": "scroll", "width":"80%", "height": "50vw", "scrollbar-width:": "none"}} >
                        {citiesList.map((c, index) => <ProfileListEntry key={index} text={`city ${c.id}`} type={"City"} x={c.x} y={c.y}/>)}
                    </div>

                }

            </div>

        </>
    )
}

export default ProfileViewer