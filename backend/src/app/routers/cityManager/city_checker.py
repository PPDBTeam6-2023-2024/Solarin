class CityChecker:
    """
    This class is a checker so we can trigger the right city checks, and update the city information
    """

    def __init__(self, city_id: int):
        """
        Constructor for the checker containing the city id we want to check
        """

        self.city_id = city_id

    def check_all(self):
        """
        this function will do all checks
        """
        self.check_training()

    def check_training(self):
        """
        this function will check the training of units and its assignment to an army when they are trained
        """
        pass