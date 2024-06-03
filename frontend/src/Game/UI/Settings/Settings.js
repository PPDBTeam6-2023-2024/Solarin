import WindowUI from "../WindowUI/WindowUI"
import {useContext, useEffect, useState} from "react";
import "./Settings.css"
import { SketchPicker } from 'react-color'
import {PrimaryContext, SecondaryContext, TertiaryContext, TextColorContext} from "../../Context/ThemeContext";
import Tooltip from "@mui/material/Tooltip";
import axios from "axios";

function Settings(props) {

    const pickerStyles = {
        default: {
            picker: {
                width: "15vw",
                height: "15vw",
                padding: "0",
                backgroundColor: "black"
            }
        }
    };

    const [primaryColor, setPrimaryColor] = useContext(PrimaryContext);
    const [secondaryColor, setSecondaryColor] = useContext(SecondaryContext);
    const [tertiaryColor, setTertiaryColor] = useContext(TertiaryContext);
    const [textColor, setTextColor] = useContext(TextColorContext);

    const sendColorUpdate = async () => {
        try {
            /*send a post request to try and create or join the alliance*/
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/logic/colors`,
                JSON.stringify({
                    "primary": primaryColor,
                    "secondary": secondaryColor,
                    "tertiary": tertiaryColor,
                    "text_color": textColor
                }),
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )

        } catch (e) {
            return ""
        }
    }

    const sendRestartUpdate = async () => {
        try {
            /*send a post request to try and create or join the alliance*/
            const response = await axios.post(`${process.env.REACT_APP_BACKEND_PATH}/logic/restart`,
                "",
                {
                    headers: {
                        'content-type': 'application/json',
                        'accept': 'application/json',
                    },
                }
            )

        } catch (e) {
            return ""
        }
    }


    const [initialClick, setInitialClick] = useState(true);
    

    useEffect(() => {
        /*Refresh information on change*/

        if (!props.viewSettings){return}

        if (initialClick){
            setInitialClick(false)
        }

        const handleClickOutside = event => {
            const {target} = event;
            const settingsElement = document.querySelector('.SettingsMenu');

            if (!initialClick && !(settingsElement.contains(target))) {

                props.onClose();
            }
        };
        document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [props.viewSettings, initialClick]);

    useEffect(() => {
        if (!props.viewSettings){setInitialClick(true)}
    }, [props.viewSettings])

    return (
        <>
            {props.viewSettings &&
                <WindowUI>
                    <div className="SettingsMenu">
                        {/*Give option for primary color*/}
                        <div className={"ColorSelector"}>
                            Primary Color
                            <SketchPicker styles={pickerStyles}
                            onChange={(color) => {setPrimaryColor(color.hex);}}
                            presetColors={[]}
                            color={primaryColor}
                            disableAlpha={true}
                            />
                        </div>

                        {/*Give option for secondary color*/}
                        <div className={"ColorSelector"}>
                            Secondary Color
                            <SketchPicker styles={pickerStyles}
                            onChange={(color) => {setSecondaryColor(color.hex);}}
                            presetColors={[]}
                            color={secondaryColor}
                            disableAlpha={true}
                            />
                        </div>

                        {/*Give option for Tertiary color*/}
                        <div className={"ColorSelector"}>
                            Tertiary Color
                            <SketchPicker styles={pickerStyles}
                            onChange={(color) => {setTertiaryColor(color.hex);}}
                            presetColors={[]}
                            color={tertiaryColor}
                            disableAlpha={true}
                            />
                        </div>

                        {/*Give option for Text color*/}
                        <div className={"ColorSelector"}>
                            Text Color
                            <SketchPicker styles={pickerStyles}
                            onChange={(color) => {setTextColor(color.hex);}}
                            presetColors={[]}
                            color={textColor}
                            disableAlpha={true}
                            />
                        </div>

                        {/*Display the button to make the changes permanent*/}

                        <div style={{"marginTop": "2vw", "display": "flex", "flexDirection": "row", "alignItems": "center",
                            "justifyContent": "center"}}>
                            <Tooltip title={`Keep the changes the next time you open the game`}>
                            <button onClick={() => {sendColorUpdate()}} > Apply Changes Permanently</button>
                            </Tooltip>
                        </div>
                        <div style={{"marginTop": "2vw", "display": "flex", "flexDirection": "row", "alignItems": "center",
                            "justifyContent": "center"}}>
                            <Tooltip title={`Reset the entire game for this player`}>
                            <button onClick={() => {sendRestartUpdate()}} > Restart Game</button>
                            </Tooltip>
                        </div>

                    </div>


                </WindowUI>
            }
        </>
    )
}

export default Settings