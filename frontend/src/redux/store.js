import { configureStore } from '@reduxjs/toolkit'
import hiddenWindowsReducer from './slices/hiddenWindowsSlice'

export default configureStore({
    reducer: {
        hiddenWindows: hiddenWindowsReducer,
    },
})