from os import path
from Profiles.Exceptions.ProfileExceptions import *
from Profiles.Profile import Profile
import pickle

DataBase = path.dirname(__file__) + "//DataBase//Profiles.pkl"

class ProfileDAO:
    def __init__(self):
        #lista com todos os perfils
        self.__all_profiles = list()

    #carrega os perfils do banco de dados
    def load_database(self) -> None:
        try:
            with open(DataBase, "rb") as data:
                self.__all_profiles = list(sorted(pickle.load(data), key=lambda x: x.max_score, reverse=True))
        except:
            with open(DataBase, "wb") as data:
                pickle.dump(list(), data)
    
    #salva o self.all_profiles atual no banco de dados
    def save_database(self) -> None:
        with open(DataBase, "wb") as data:
            pickle.dump(self.all_profiles, data)

    #retorna um perfil pelo nome
    def get_profile(self, name: str) -> Profile:
        self.load_database()

        if (self.verify_profile_existence(name)):
            for profile in self.all_profiles:
                if (profile.name == name):
                    return profile
        else:
            return False

    #verifica se existe um perfil pelo nome
    #True -> se existe
    #False -> se não existe
    def verify_profile_existence(self, name: str) -> bool:
        self.load_database()

        name = name.capitalize().strip()
        self.detect_exceptions(name)
        try:
            for profile in self.all_profiles:
                if (name == profile.name):
                    return True 
            else:
                return False
        except:
            return True

    #remove um perfil pelo nome
    #True -> Removido com sucesso
    #False -> Perfil não existe
    def remove_profile(self, name: str) -> bool:
        self.load_database()

        name = name.capitalize().strip()
        self.detect_exceptions(name)

        if (self.verify_profile_existence(name)):

            for i, profile in enumerate(self.all_profiles):
                if (profile.name == name):
                    self.all_profiles.pop(i)

                    self.save_database()
                    return True
        else:
            return False
    
    #salva um perfil JÁ EXISTENTE
    #True -> Salvado com sucesso
    def save_profile(self, profile: Profile) -> bool:
        self.load_database()

        if (self.verify_profile_existence(profile.name)):
            self.remove_profile(profile.name)
            self.all_profiles.append(profile)
            self.save_database()
            return True
        else:
            return False

    #cria um novo perfil
    #Da erro de o perfil já existir
    def create_profile(self, name: str,
                       credit: int,
                       max_score: int,
                       ship_damage: int,
                       ship_vel_max: float,
                       ship_life: int,
                       ship_cooldown: int,
                       ship_qtd_bullet: int) -> None:
        self.load_database()

        name = name.capitalize().strip()
        self.detect_exceptions(name)

        if (self.verify_profile_existence(name)):
            raise ProfileAlreadyExist

        profile = Profile(name, credit, max_score, ship_damage, ship_vel_max, ship_life, ship_cooldown, ship_qtd_bullet)
        self.all_profiles.append(profile)
            
        self.save_database()

    def get_all_profiles(self) -> list[Profile]:
        self.load_database()
        return self.all_profiles

    def detect_exceptions(self, name: str) -> None:
        if (" " in name):
            raise NameWithSpace

        if (len(name) > 5):
            raise NameWithMoreThan5Letters

        if (name == ""):
            raise NullName

    @property
    def all_profiles(self):
        return self.__all_profiles

