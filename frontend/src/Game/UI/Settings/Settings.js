import WindowUI from "../WindowUI/WindowUI"
import {useContext, useState} from "react";
import "./Settings.css"
import { SketchPicker } from 'react-color'
import {PrimaryContext, SecondaryContext, TertiaryContext} from "../../Context/ThemeContext";
import Tooltip from "@mui/material/Tooltip";

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

                        {/*Display the button to make the changes permanent*/}
                        <Tooltip title={`Keep the changes the next time you open the game`}>
                        <div style={{"display": "inline-block"}}>
                            <button> Apply Changes Permanently</button>
                        </div>
                        </Tooltip>
                    </div>


                </WindowUI>
            }
        </>
    )
}

export default Settings