import {configureStore} from '@reduxjs/toolkit'
import hiddenWindowsReducer from './slices/hiddenWindowsSlice'
import resourcesReducer from './slices/resourcesSlice'
import maintenanceSlice from "./slices/maintenanceSlice";
export default configureStore({
    reducer: {
        hiddenWindows: hiddenWindowsReducer,
        resources:resourcesReducer,
        maintenance:maintenanceSlice
    },
})