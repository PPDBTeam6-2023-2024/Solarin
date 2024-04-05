import {useSelector, useDispatch } from 'react-redux'
import WindowUI from '../WindowUI/WindowUI'
import { BottomNavigation, BottomNavigationAction, Box } from '@mui/material'
import { removeWindow } from '../../../redux/slices/hiddenWindowsSlice'
function HiddenWindowsViewer () {
    const hiddenWindows = useSelector((state) => state.hiddenWindows.windows)
    const dispatch = useDispatch()
    return (
        <WindowUI>
        <Box position="fixed" top="50%" right="0">
        <BottomNavigation sx={{bgcolor: "black"}} showLabels>
        {
            hiddenWindows.map((elem) => {
                return <BottomNavigationAction onClick={() => dispatch(removeWindow(elem))}sx={{ width: "2vw"}} label={elem} />
            })
        }
        </BottomNavigation>
        </Box>
        </WindowUI>
    )
}
export default HiddenWindowsViewer