import { createSlice } from '@reduxjs/toolkit'

/*
* Store the maintenance information of a user
* maintenanceCost: the maintenance cost for the user
* maintenanceCheckable: whether the frontend is allowed to sync with the backend about the maintenance information
* (This is mainly used to avoid spam of requests with the backend in case our resources reach 0)
*/
const maintenanceSlice = createSlice({
  name: 'maintenance',
  initialState : {
    maintenance: {"maintenanceCost": [], "maintenanceCheckable": false}
  },
  reducers: {
      setMaintenanceCost(state, action) {
        state.resources["maintenanceCost"] = action.payload
      }
  },
})

export const {setMaintenanceCost} = maintenanceSlice.actions
export default maintenanceSlice.reducer