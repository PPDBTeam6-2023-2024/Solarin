import axios from "axios"

const getarmies = async (planetid) => {
    axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`};
    const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/army/armies?planet_id=1`);
    if(response.status===200){
        return response.data
    }
}
