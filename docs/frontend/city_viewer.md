# CityViewer Documentation

## Overview
CityViewer is a dynamic component within our game that provides an interactive visual representation of cities within a planet. 
It allows users to view and interact with the cities, offering an immersive experience in the game's environment.

## Technologies Used
- React.js: For building the interactive user interface.
- FastAPI: Backend API to handle requests and serve data.
- Axios: For making HTTP requests to the backend server.
- AG Grid: To display detailed information about buildings within a city.
- React Hooks: Utilize state and lifecycle features in functional components.

## Description
The CityViewer component integrates various functionalities, including displaying cities on a planet, showing building details within a city, and updating information in real-time. 
It uses a combination of custom React hooks, state management, and external libraries to achieve an interactive user experience.

### Key Features
- **Planet Map**: Displays an interactive map of a planet with cities marked on it.
- **City Selection**: Clicking on a city brings up the CityManager, a detailed view showing information about buildings within the selected city. Naturally, users can only view open the CityManager by clicking on one of their own cities.
- **Dynamic Building and Troop Data**: The CityManager fetches and displays building and troop data dynamically from the backend, updating in real-time as changes occur.
- **Building Details**: Within the CityManager, users can view specific details about each building, such as type, rank, and function.
- **Army Management**: Users can view and interact with their city's army, offering strategic insights and actions.
- **Upgrade System**: Buildings can now be upgraded, enhancing their rank and capabilities.
- **Resource Collection**: Enables users to collect resources from production buildings, crucial for urban and military development.
- **Building Construction**: Users can construct new buildings, expanding their city's capabilities.
- 
### Implementation Details
- **Fetching Cities**: Uses a custom `getCities` function that makes an API call to fetch cities based on the planet ID. It dynamically generates clickable city images on the map based on the fetched data.
- **CityManager Integration**: Once a city is clicked, the CityManager component is rendered, providing a detailed view of the city's buildings. This integration allows users to interact with individual buildings and gain insights into their status and attributes.
- **Building Data**: The CityManager uses `getBuildings` to fetch building information for the selected city. It displays this data in an AG Grid, providing a sortable and interactive table of building details.
- **UpgradeButtonComponent**: Facilitates upgrading buildings, interfacing with backend services to update and retrieve the latest upgrade costs and statuses.
- **ResourceButtonComponent**: Allows users to collect resources from specific buildings, integrating real-time data updates to increases in resources stored in production buildings overtime.
- **CurrentBuildingGrid**: Provides a UI for managing current buildings, including an interface for upgrading buildings, collecting resources and managing the troops in a city.
- **NewBuildingGrid**: Provides a UI for constructing new buildings, reflecting real-time updates on construction feasibility based on available resources.
- **ArmyGrid**: Displays information about the city's army, including troop types, ranks, and sizes, allowing users to make informed strategic decisions.

## Additional Information
- **City Images**: The appearance of city images can be customized based on city attributes (e.g., rank) using the `getCityImage` function.
- **Building Images**: The images for each building type are specified and can be extended in `./frontend/src/Game/UI/buildingImages.json`
- **Troop Images**: Likewise, the troop images for each troop type are specified and can be extended in `./frontend/src/Game/UI/troops.json`
- **AG Grid Customization**: The AG Grid within the CityManager is highly customizable. Columns, data presentation, and interaction can be tailored to meet specific requirements. Info about the use of AGGrid can be found at https://www.ag-grid.com/react-data-grid/getting-started/.

## Conclusion
CityViewer is a crucial component that enhances user engagement by providing a visual and interactive representation of cities within the game's universe. 
Its integration with backend services ensures that the data displayed is always up-to-date, providing a seamless experience for users.


