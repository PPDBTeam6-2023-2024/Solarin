// Determine which image should be used, based on the city rank
export const getCityImage = (cityRank) => {
    switch (cityRank) {
        case 1:
            return '/images/city_images/City_Rank0.png';
        case 2:
            return '/images/city_images/City_Rank1.png';
        case 3:
            return '/images/city_images/City_Rank2.png';
        default:
            return '/images/city_images/City_Rank0.png';
    }
};