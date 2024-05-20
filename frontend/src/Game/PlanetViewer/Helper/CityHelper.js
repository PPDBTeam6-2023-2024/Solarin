import GetCities from '../CityViewer/GetCities';

export const fetchCities = async ({handleCityClick, setCityImages}, planetId) => {
    /** Get all the cities on the provided planet from backend*/
    const cities = await GetCities(planetId);

    // replace with actual planetID
    const cityElements = cities.map(city => ({
        ...city,
        onClick: () => handleCityClick(city.id, city.controlled_by),
    }));
    setCityImages(cityElements);
};