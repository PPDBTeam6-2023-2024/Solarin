import { useEffect, useState} from "react"
import axios from 'axios'
import PlanetViewer from "./PlanetViewer/PlanetViewer"

const Game = () => {
    const [isAuth, setIsAuth] = useState(false)
    const [userInfo, setUserInfo] = useState(null)

    const authenticate = async() => {
        try {
        axios.defaults.headers.common = {'Authorization': `Bearer ${localStorage.getItem('access-token')}`}
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_PATH}/auth/me`)
        if (response.status === 200) {
            setIsAuth(true)
            setUserInfo(response.data)
        }
        }
        catch(error) {
            setIsAuth(false)
        }
    }

    useEffect(() => {
        authenticate()
    }, [])
    return (<div className="h-screen bg-gray-900">
        {userInfo && <>
            <PlanetViewer planetName="Mars"/>
            </>}
        {!userInfo && !isAuth && <h1>Not authenticated</h1>}
    </div>)
}
export default Game