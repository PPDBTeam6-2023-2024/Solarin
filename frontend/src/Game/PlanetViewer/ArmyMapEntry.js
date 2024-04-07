
function ArmyMapEntry(props) {

    return (
        <img key={props.index} src={props.army.src} alt="army" className="transition-all ease-linear" style={{...props.army.style, left: `${props.army.curr_x * 100}%`, top: `${props.army.curr_y * 100}%`}}
                         onClick={props.onClick} {...{ "test": "1" }} index={props.index} image_type={"army"}/>


    )
}
export default ArmyMapEntry