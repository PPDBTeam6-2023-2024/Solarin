import {useContext} from "react";
import {UserInfoContext} from "../Context/UserInfoContext";

function CityMapEntry(props) {
    const [userInfo, setUserInfo] = useContext(UserInfoContext);

    const is_owner = +(userInfo.id === props.city.controlled_by);
    return (
        <img key={props.index} src={props.city.src} alt="city" style={props.city.style} onClick={props.onClick} index={props.city.id} image_type={"city"} is_owner={is_owner}/>
    )
}
export default CityMapEntry