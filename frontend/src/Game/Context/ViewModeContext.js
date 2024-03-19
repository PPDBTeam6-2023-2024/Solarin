import React from "react";

// enum
const View = {
    GalaxyView: "GalaxyView",
    PlanetView: "PLanetView",
    CityView: "CityView",
    ProfileView: "ProfileView"

}

const ViewModeContext = React.createContext();

export {ViewModeContext, View}

