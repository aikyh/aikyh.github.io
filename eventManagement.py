
class eventManagement:
    count_id = 0

    # initializer method
    def __init__(self, name, date, timing, location, description, budget, person_in_charge,  collaborators):
        eventManagement.count_id += 1
        self.__event_id = eventManagement.count_id
        self.__name = name
        self.__date = date
        self.__timing = timing
        self.__location = location
        self.__description = description
        self.__person_in_charge = person_in_charge
        self.__budget = budget
        self.__collaborators = collaborators

        

    # accessor methods
    def get_event_id(self):
        return self.__event_id

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_timing(self):
        return self.__timing

    def get_location(self):
        return self.__location

    def get_description(self):
        return self.__description

    def get_person_in_charge(self):
        return self.__person_in_charge

    def get_collaborators(self):
        return self.__collaborators

    def get_budget(self):
        return self.__budget

    def get_photo(self):
        return self.__photo
    # mutator methods
    def set_event_id(self, event_id):
        self.__event_id = event_id

    def set_name(self, name):
        self.__name = name

    def set_date(self, date):
        self.__date = date

    def set_timing(self, timing):
        self.__timing = timing

    def set_location(self, location):
        self.__location = location

    def set_description(self, description):
        self.__description = description

    def set_person_in_charge(self, person_in_charge):
        self.__person_in_charge = person_in_charge

    def set_budget(self, budget):
        self.__budget = budget

    def set_collaborators(self, collaborators):
        self.__collaborators = collaborators

    def set_photo(self, photo):
        self.__photo = photo