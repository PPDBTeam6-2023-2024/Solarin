import React, {useState, useContext } from 'react';
import "./ProfileButton.css"
import profile from "./../../Images/profile_images/profile_1.png"
import {ViewModeContext, View} from "../../Context/ViewModeContext"
import WindowUI from '../WindowUI/WindowUI';


const ProfileElement = (props) => {
    /**
     * create the visuals for the profile button
     * */
  return (
      <>
          <div className="profile_circle bottom-0 fixed transition ease-in-out" onClick={props.onProfileClick}>
              <div className="profile_background bottom-0 fixed">
                  <img src={profile} alt="profile_1" draggable="false"/>
              </div>
          </div>

      </>
  );
};


/*component to access the profile of a user*/
function ProfileButton() {
    const [viewMode, setViewMode] = useContext(ViewModeContext)
    const [LastViewMode, setLastViewMode] = useState(View.PlanetView)

    const onPressProfileButton = () => {

        if (viewMode !== View.ProfileView){
            /**
            * when profile menu is not open, we open it
            * */
            setLastViewMode(viewMode);
            setViewMode(View.ProfileView);
        }else{
            /**
             * Open the last view before we opened profile view
             * */
            setViewMode(LastViewMode);
        }
    }
    return(
        <WindowUI>
            <ProfileElement onProfileClick={onPressProfileButton}/>
            {/*Below is the bar we have which will contain all the resources*/}
            <div id="profile_bar" className="bottom-0 left-0 fixed"></div>
       </WindowUI>
    )


}

export default ProfileButton