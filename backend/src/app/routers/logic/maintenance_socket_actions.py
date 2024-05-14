import json
from ..core.connection_pool import ConnectionPool
from fastapi.websockets import WebSocket
from ...database.database_access.data_access import DataAccess


class MaintenanceSocketActions:
    """
    This class gives structure to the socket action methods
    """

    def __init__(self, user_id: int, data_access: DataAccess, websocket: WebSocket=None):
        """
        The provided parameters are parameters that stay the same for the entire lifetime of this Object
        """

        self.user_id = user_id
        self.data_access = data_access

        self.websocket = websocket

    async def maintenance_request(self, data: json):
        """
        Update maintenance information
        """
        delta_time = await self.data_access.ResourceAccess.maintenance_delta_time(self.user_id)

        cost_dict = await self.check_maintenance()
        cost_dict = [(k, v) for k, v in cost_dict.items()]
        """
        checkin, gives information to the user, that calibration with the backend is no use for at least
        the amount provided in the checkin
        """
        if self.websocket is not None:
            await self.websocket.send_json({"type": "update_cost",
                                            "maintenance_cost": cost_dict, "checkin": 3610-(delta_time % 3600)})

    async def check_maintenance(self, commit=True):
        """
        Update the maintenance information

        """
        change_occurred = False
        cities = await self.data_access.CityAccess.get_cities_by_controller(self.user_id)
        for city in cities:
            changed = await self.data_access.ResourceAccess.check_maintenance_city(self.user_id, city.id)
            if changed:
                change_occurred = True

        armies = await self.data_access.ArmyAccess.get_user_armies(self.user_id)
        for army in armies:
            changed = await self.data_access.ResourceAccess.check_maintenance_army(self.user_id, army.id)
            if changed:
                change_occurred = True

        """
        Update last checked timer
        """
        await self.data_access.flush()
        await self.data_access.ResourceAccess.maintenance_checked(self.user_id)

        if commit:
            await self.data_access.commit()
        else:
            await self.data_access.flush()

        """
        Calculate total remaining maintenance cost
        """
        cost_dict = {}

        cities = await self.data_access.CityAccess.get_cities_by_controller(self.user_id)
        for city in cities:
            temp_dict = await self.data_access.ResourceAccess.get_maintenance_city(city.id)
            for k, v in temp_dict.items():
                cost_dict[k] = cost_dict.get(k, 0)+v

        armies = await self.data_access.ArmyAccess.get_user_armies(self.user_id)
        for army in armies:
            temp_dict = await self.data_access.ResourceAccess.get_maintenance_army(army.id)
            for k, v in temp_dict.items():
                cost_dict[k] = cost_dict.get(k, 0) + v

        if change_occurred and self.websocket is not None:
            await self.websocket.send_json({"request_type": "reload"})

        return cost_dict

