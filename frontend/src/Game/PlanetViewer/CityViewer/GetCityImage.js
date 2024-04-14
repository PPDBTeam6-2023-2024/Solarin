import cityRank0 from "../../Images/city_images/City_Rank0.png";
import cityRank1 from "../../Images/city_images/City_Rank1.png";
import cityRank2 from "../../Images/city_images/City_Rank2.png";

// Determine which image should be used, based on the city rank
export const getCityImage = (cityRank) => {
    switch (cityRank) {
        case 0:
            return cityRank0;
        case 1:
            return cityRank1;
        case 2:
            return cityRank2;
        default:
            return cityRank0;
    }
};