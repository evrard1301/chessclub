class Player:
    def __init__(self,
                 last_name,
                 first_name,
                 date_of_birth,
                 gender,
                 ranking):
        self.last_name = last_name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.ranking = ranking

    @property
    def __dict__(self):
        return {
            'last_name': self.last_name,
            'first_name': self.first_name,
            'date_of_birth': str(self.date_of_birth),
            'gender': self.gender,
            'ranking': self.ranking
        }

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def same_as(self, player):
        return player.last_name == self.last_name \
            and player.first_name == self.first_name
