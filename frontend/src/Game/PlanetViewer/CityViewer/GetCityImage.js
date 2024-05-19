// Determine which image should be used, based on the city rank
export const getCityImage = (cityRank) => {
    switch (cityRank) {
        case 1:
            return '/images/city_images/City_Rank1.png';
        case 2:
            return '/images/city_images/City_Rank2.png';
        case 3:
            return '/images/city_images/City_Rank3.png';
        case 4:
            return '/images/city_images/City_Rank4.png';
        case 5:
            return '/images/city_images/City_Rank5.png';
    }
};