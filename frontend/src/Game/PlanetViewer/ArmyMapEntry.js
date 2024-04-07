import {useContext} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";

function ArmyMapEntry(props) {

    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const is_owner = +(userInfo.id === props.army.owner);
    return (
        <img key={props.index} src={props.army.src} alt="army" className="transition-all ease-linear" style={{...props.army.style, left: `${props.army.curr_x * 100}%`, top: `${props.army.curr_y * 100}%`}}
                         onClick={props.onClick} {...{ "test": "1" }} index={props.army.id} image_type={"army"} is_owner={is_owner}/>


    )
}
export default ArmyMapEntry