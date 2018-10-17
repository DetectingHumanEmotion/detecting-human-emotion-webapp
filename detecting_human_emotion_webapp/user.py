class User:

    def __init__(self, firstname, lastname, race, gender, age, questions=[]):
        self.firstname = firstname
        self.lastname = lastname
        self.race = race
        self.gender = gender
        self.age = age
        self.questions = questions

    def print_data(self):
        print(self.firstname)
        print(self.lastname)
        print(self.race)
        print(self.gender)
        print(self.age)
        print(self.questions)
