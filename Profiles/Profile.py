class Profile:
    def __init__(self, name: str,
                 credit: int,
                 max_score: int,
                 ship_damage: int,
                 ship_vel_max: int,
                 ship_life: int,
                 ship_cooldown: int,
                 ship_qtd_bullet: int) -> None:
        
        self.__name = name
        self.__credit = credit
        self.__max_score = max_score
        self.__ship_damage = ship_damage
        self.__ship_vel_max = ship_vel_max
        self.__ship_life = ship_life
        self.__ship_cooldown = ship_cooldown
        self.__ship_qtd_bullet = ship_qtd_bullet

    def set_credit(self, credit: int) -> None:
        self.__credit = credit

    def set_max_score(self, score: int) -> None:
        self.__max_score = score

    def set_ship_damage(self, dmg: int) -> None:
        self.__ship_damage = dmg

    def set_ship_vel_max(self, vel: int) -> None:
        self.__ship_vel_max = vel

    def set_ship_life(self, life: int) -> None:
        self.__ship_life = life

    def set_ship_cooldown(self, cdw: int) -> None:
        self.__ship_cooldown = cdw

    def set_ship_qtd_bullet(self, qtdb: int) -> None:
        self.__ship_qtd_bullet = qtdb

    @property
    def name(self):
        return self.__name

    @property
    def credit(self):
        return self.__credit

    @property
    def max_score(self):
        return self.__max_score
        
    @property
    def ship_damage(self):
        return self.__ship_damage

    @property
    def ship_vel_max(self):
        return self.__ship_vel_max

    @property
    def ship_life(self):
        return self.__ship_life

    @property
    def ship_cooldown(self):
        return self.__ship_cooldown

    @property
    def ship_qtd_bullet(self):
        return self.__ship_qtd_bullet
