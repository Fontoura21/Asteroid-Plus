from Profiles.Profile import Profile

class GameData:
    def __init__(self) -> None:
        self.__profile: Profile =       None
        self.__level: int =             None
        self.__score: int =             None
        self.__enemies_destroyed: int = None
        self.__ship_life: int =         None
        self.__only_boss_mode: bool =   None

    def set_only_boss_mode(self, v: bool) -> None:
        self.__only_boss_mode = v

    def set_enemies_destroyed(self, num: int) -> None:
        self.__enemies_destroyed = num

    def set_profile(self, profile: Profile) -> None:
        self.__profile = profile

    def set_level(self, level: int) -> None:
        self.__level = level

    def set_score(self, score: int) -> None:
        self.__score = score

    def set_ship_life(self, life: int) -> None:
        self.__ship_life = life

    @property
    def only_boss_mode(self) -> bool:
        return self.__only_boss_mode

    @property
    def profile(self) -> Profile:
        return self.__profile

    @property
    def enemies_destroyed(self) -> int:
        return self.__enemies_destroyed

    @property
    def level(self) -> int:
        return self.__level

    @property
    def score(self) -> int:
        return self.__score

    @property 
    def ship_life(self):
        return self.__ship_life
        