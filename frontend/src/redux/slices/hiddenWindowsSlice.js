import {createSlice} from '@reduxjs/toolkit'

const hiddenWindowsSlice = createSlice({
    name: 'hiddenWindows',
    initialState: {
        windows: []
    },
    reducers: {
        addWindow(state, action) {
            let index = state.windows.indexOf(action.payload)
            if (index === -1) state.windows.push(action.payload)
        },
        removeWindow(state, action) {
            let index = state.windows.indexOf(action.payload)
            if (index !== -1) {
                state.windows.splice(index, 1)
            }
        }
    },
})

export const {addWindow, removeWindow} = hiddenWindowsSlice.actions
export default hiddenWindowsSlice.reducer