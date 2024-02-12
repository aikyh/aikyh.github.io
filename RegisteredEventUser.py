import shelve


class RegisteredEventUser():
    count_id = 0

    def __init__(self, user_id, name, no_of_people, email):
        RegisteredEventUser.count_id += 1
        self.user_id = user_id
        self.name = name
        self.no_of_people = no_of_people
        self.email = email
