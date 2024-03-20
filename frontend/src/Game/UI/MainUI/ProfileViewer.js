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

    const getCitiesPositions = async() => {
        /*get the list of all the requests to join the alliance*/
        try {
            axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/cityManager/cities_user`)
            console.log(response.data)
            setCitiesList(response.data)
        }
        catch(e) {setCitiesList([])}
    }

    return (
        <>
            <div className="profile_viewer">
                <h1>Username: {userInfo.username}</h1>

                <div style={{"width":"15%", "height": "100%", "marginLeft": "1vw"}} >
                    <ul>
                        <div className="profile_viewer_category_button" onClick={() => {setSelectedCategory("Cities"); getCitiesPositions();}}>Cities</div>
                        <div className="profile_viewer_category_button" onClick={() => setSelectedCategory("Armies")}>Armies</div>
                    </ul>

                </div>

                {selectedCategory === "Cities" &&
                    <div className="profile_viewer_list absolute" style={{"overflow-y": "scroll", "width":"80%", "height": "80%", "scrollbar-width:": "none"}} >
                        {citiesList.map((c, index) => <ProfileListEntry key={index} text={`city ${c.id} on ${c.planet_name}`} type={"City"} x={c.x} y={c.y}/>)}
                    </div>

                }

            </div>

        </>
    )
}

export default ProfileViewer