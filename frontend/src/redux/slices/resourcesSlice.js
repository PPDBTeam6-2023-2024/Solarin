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
      }
  },
})

export const {setResources, setResource} = resourcesSlice.actions
export default resourcesSlice.reducer