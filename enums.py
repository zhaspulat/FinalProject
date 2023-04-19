import enum


class Genre(enum.Enum):
    Alternative = 'Alternative'
    Action = 'Action'
    Comedy = 'Comedy'
    Drama = 'Drama'
    Fantasy = 'Fantasy'
    Horror = 'Horror'
    Mystery = 'Mystery'
    Romance = 'Romance'
    Thriller = 'Thriller'
    Crime ='Crime'
    Adventure = 'Adventure' 
        
    @classmethod
    def choices(cls):
        return [(choice.name , choice.value) for choice in cls]

class Participance_name(enum.Enum):
    Director = 'Director'
    Writer = 'Writer'
    Star = 'Star'
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]

class Gender(enum.Enum):
    male = 'Male'
    female = 'Female'
    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]