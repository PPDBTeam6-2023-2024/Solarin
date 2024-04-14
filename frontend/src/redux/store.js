import {configureStore} from '@reduxjs/toolkit'
import hiddenWindowsReducer from './slices/hiddenWindowsSlice'
import resourcesReducer from './slices/resourcesSlice'

export default configureStore({
    reducer: {
        hiddenWindows: hiddenWindowsReducer,
        resources:resourcesReducer,
    },
})