import shelve
import eventManagement


class RegisteredEventUser:
    count_id = 0

    def __init__(self, name, no_of_people, email, contact_number):
        RegisteredEventUser.count_id += 1
        self.name = name
        self.no_of_people = no_of_people
        self.email = email
        self.contact_number = contact_number



