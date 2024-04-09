import {useContext} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";
import "./CityMapEntry.css"

function CityMapEntry(props) {
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const is_owner = +(userInfo.id === props.city.controlled_by);

     let cursor_style_class = "CityMapEntryPointer";

    if (props.decide_moving){
        if (!is_owner){
            // Display the attack cursor, when hovering on an enemy army when in decide moving mode
            cursor_style_class = 'CityMapEntryEnemy'
        }else{
            cursor_style_class = 'CityMapEntryEnter'
        }
    }


    return (
        <img className={`${cursor_style_class}`} key={props.index} src={props.city.src} alt="city" style={props.city.style} onClick={props.onClick} index={props.city.id} image_type={"city"} is_owner={is_owner}/>
    )
}
export default CityMapEntry