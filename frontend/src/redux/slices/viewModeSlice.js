import { createSlice } from '@reduxjs/toolkit'
import {ViewModeContext, View} from "./Context/ViewModeContext"

const viewModeSlice = createSlice({
  name: 'viewMode',
  initialState : {
    mode: View.PlanetView,
  },
  reducers: {
      setResources(state, action) {
        state.resources = action.payload
      },
      setResource(state, action) {
        state.resources[action.payload.resource] = action.payload.value
      }
  },
})

export const {setResources, setResource} = resourcesSlice.actions
export default resourcesSlice.reducer