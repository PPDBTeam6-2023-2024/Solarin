export const fetchCities = async ({getCities, handleCityClick, setCityImages, setCitiesLoaded}, planetId) => {
    const cities = await getCities(planetId);

    // replace with actual planetID
    const cityElements = cities.map(city => ({
        ...city,
        onClick: () => handleCityClick(city.id, city.controlled_by),
    }));
    setCityImages(cityElements);
    setCitiesLoaded(true);
};