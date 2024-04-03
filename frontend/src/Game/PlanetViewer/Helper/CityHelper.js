export const fetchCities = async ({getCities, handleCityClick, setCityImages, setCitiesLoaded}) => {
    const cities = await getCities(1);

    // replace with actual planetID
    const cityElements = cities.map(city => ({
        ...city,
        onClick: () => handleCityClick(city.id, city.controlled_by),
    }));
    setCityImages(cityElements);
    setCitiesLoaded(true);
};