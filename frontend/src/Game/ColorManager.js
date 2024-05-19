
import {useContext, useEffect, useState} from "react";
import {PrimaryContext, SecondaryContext, TertiaryContext, TextColorContext} from "./Context/ThemeContext";
import axios from "axios";

function ColorManager({children}) {
    /**
    * This Component makes sure that all the child components have access, using a context
    * to the theme colors used to manage UI theme colors
    * */

    /*
     * these 4 states exist to be able to change the UI colors
     * */
    const [primaryColor, setPrimaryColor] = useState("#c88018")
    const [secondaryColor, setSecondaryColor] = useState("#c53520")
    const [tertiaryColor, setTertiaryColor] = useState("#fbfbfb")
    const [textColor, setTextColor] = useState("#ffffff")

    /*
    * Retrieve the colors from the backend
    * */
    useEffect(() => {
        const getColors = async() => {
            axios.defaults.headers.common = await {'Authorization': `Bearer ${localStorage.getItem('access-token')}`, "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"}
            const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/logic/colors`)
            if (response.data === null){return}
            /*
             * Store the values into the stats
             */
            setPrimaryColor(response.data.primary_color);
            setSecondaryColor(response.data.secondary_color);
            setTertiaryColor(response.data.tertiary_color);
            setTextColor(response.data.text_color);
        }

        getColors();
    }, []);
    console.log("set colors")
    return (

        <div className="h-screen bg-gray-900"
            style={{
                '--primaryColor': primaryColor,
                '--secundaryColor': secondaryColor,
                "--tertiaryColor": tertiaryColor,
                "--textColor": textColor,
            }}>
            {/*The default css color variables have been set*/}

            {/*Make it possible to access the colors using contexts*/}
            <PrimaryContext.Provider value={[primaryColor, setPrimaryColor]}>
            <SecondaryContext.Provider value={[secondaryColor, setSecondaryColor]}>
            <TertiaryContext.Provider value={[tertiaryColor, setTertiaryColor]}>
            <TextColorContext.Provider value={[textColor, setTextColor]}>
                {children}
            </TextColorContext.Provider>
            </TertiaryContext.Provider>
            </SecondaryContext.Provider>
            </PrimaryContext.Provider>
        </div>
    )
}

export default ColorManager;