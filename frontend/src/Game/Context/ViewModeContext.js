import React from "react";

/**
 * Context to access which view is currently active
 * */

/*
* Enumeration of views
* */
const View = {
    GalaxyView: "GalaxyView",
    PlanetView: "PLanetView",
    CityView: "CityView",
    ProfileView: "ProfileView"
}

const ViewModeContext = React.createContext();

export {ViewModeContext, View}

