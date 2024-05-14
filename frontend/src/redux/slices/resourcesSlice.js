import { createSlice } from '@reduxjs/toolkit'

const resourcesSlice = createSlice({
  name: 'resources',
  initialState : {
    resources: {}
  },
  reducers: {
      setResources(state, action) {
        state.resources = action.payload
      },
      setResource(state, action) {
          state.resources[action.payload.resource] = action.payload.value
      },
      setDecreaseResource(state, action) {

          let resources = state.resources


          let state_copy = {...state, "resources": {...resources, [action.payload.resource]: Math.max(resources[action.payload.resource]-1, 0)}}

          return state_copy
      }

  },
})

export const {setResources, setResource, setDecreaseResource} = resourcesSlice.actions
export default resourcesSlice.reducer