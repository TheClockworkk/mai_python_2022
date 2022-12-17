import json

class Aircraft:
    def __init__(self, weight):
        self._weight = weight

class UAV:
    # Для вас уже написаны заготовки классов Aircraft и UAV
    # TODO 3-1
    # Добавьте в класс UAV защищенный атрибут _=_missions (тип - список списков [[], []]),         куда вы будете сохранять все миссии, которые отлетал беспилотник
    def __init__(self):
        self._has_autopilot = True
        self._missions = []

    # TODO 3-2
    # При помощи декоратора @property сделайте возможность чтения и записи миссий в этот           атрибут (лекция 8)
    @property
    def missions(self):
        return self._missions 

    @missions.setter
    def missions(self, mission):
        self._missions.append(mission)

    # TODO 3-3
    # Создайте в классе UAV публичный метод count_missions, который возвращает количество          миссий (лекция 7)
    def count_missions(self):
        count = len(self.missions)
        return count        
      
# TODO 3-4) Создайте класс MultirotorUAV - наследник классов Aircraft и UAV (лекция 7)
class MultirotorUAV(Aircraft, UAV):

    def __init__(self, weight, model, brand):
        super().__init__(weight)
        UAV.__init__(self)
        self.__weight = weight
        self.__brand = brand
        self.__model = model

    def get_info(self):
        return f"масса: {self.__weight}, производитель: {self.__brand}, количество миссий: {self.count_missions()}"

    def get_model(self):
        return self.__model


def read_json(filename):

    with open(filename) as json_file:
        data = json.load(json_file)
    
    return data

# TODO 2-1
# Подсчитайте, сколько миссий налетал каждый пилот. Выведите результат в порядке убывания      миссий
# ИНФОРМАЦИЯ:
# структура данных в файле: {"имя_пилота": "список_миссий":[миссия1, ...]]
# структура одной миссии: {"drone":"модель_дрона", "mission":[список точек миссии]}
# у пилотов неодинаковое количество миссий (и миссии могут быть разной длины). у каждой        миссии - произвольная модель дрона
def missions_by_pilot(pilot, data):
    return data[pilot]["missions"]

def missions_by_pilots(data):
    missions_count_by_pilots = {}
    for pilot in data.keys():
        missions = missions_by_pilot(pilot, data)
        missions_count_by_pilots[pilot] = len(missions)

    return dict(sorted(missions_count_by_pilots.items(), key=lambda item: item[1], reverse=True))

# TODO 2-2
# Получите и выведите список всех моделей дронов, которые были в файле pilot_path.json
def all_drone_types(data):
    
    used_drones = []

    drones_missions = missions_by_drones(data)

    for drone in drones_missions.keys():
        if not drone in used_drones:
            used_drones.append(drone)

    return used_drones           
            

def missions_by_drones(data):

    drones_missions_dict = {}

    for pilot in data.keys():
        missions = missions_by_pilot(pilot, data)
        for mission in missions:
            drone = mission["drone"]
            if not drone in drones_missions_dict.keys():
                drones_missions_dict[drone] = []    
            drones_missions_dict[drone].append(mission["mission"])


    return drones_missions_dict 

# TODO 2-3
# Получите список миссий для каждой модели дронов, которые были в файле                        pilot_path.json,
# и выведите на экран модель дрона и количество миссий, которые он отлетал
def count_missions_by_drones(data):

    drones_missions = missions_by_drones(data)
    result = {}

    for drone in drones_missions.keys():
        result[drone] = len(drones_missions[drone])

    return result    


def choose_drone(lower_input):
    
    drones = {
        "dji inspire 2" : "DJI Inspire 2",
        "dji mavic 2 pro" : "DJI Mavic 2 Pro",
        "dji mavic 2 enterprise advanced" : "DJI Mavic 2 Enterprise Advanced",
        "dji mavic 3" : "DJI Mavic 3",
        "dji mavic 2 zoom" : "DJI Mavic 2 Zoom"
    }

    return drones[lower_input]


if __name__ == "__main__":

    # TODO 1-1
    # Прочитайте данные из файла pilot_path.json (лекция 9)

    filename = "pilot_path.json"
    json_data = read_json(filename)

    # TODO 2-1
    # Подсчитайте, сколько миссий налетал каждый пилот. Выведите результат в порядке убывания      миссий
    pilots_missions_count = missions_by_pilots(json_data)
    print(pilots_missions_count)
    print("\n")

    # TODO 2-2
    # Получите и выведите список всех моделей дронов, которые были в файле pilot_path.json
    used_drones = all_drone_types(json_data)
    print(f'Полеты совершались на дронах следующих моделей: {", ".join(used_drones)}')
    print("\n")

    # TODO 2-3
    # Получите список миссий для каждой модели дронов, которые были в файле                        pilot_path.json,
    # и выведите на экран модель дрона и количество миссий, которые он отлетал
    drones_missions_count = count_missions_by_drones(json_data)
    for drone in drones_missions_count.keys():
        print(f"Дрон {drone} отлетал {drones_missions_count[drone]} миссий")
    print("\n")

    drone_catalog = {
        "DJI Mavic 2 Pro": {"weight": 903, "brand": "DJI"},
        "DJI Mavic 2 Zoom": {"weight": 900, "brand": "DJI"},
        "DJI Mavic 2 Enterprise Advanced": {"weight": 920, "brand": "DJI"},
        "DJI Inspire 2": {"weight": 1500, "brand": "DJI"},
        "DJI Mavic 3": {"weight": 1000, "brand": "DJI"}
    }

    missions_drones = missions_by_drones(json_data)
    drone_arr = []

    # TODO 4-1
    # Создайте экземпляры класса MultirotorUAV для всех моделей дронов, которые были в файле       pilot_path.json
    # Подсказка: созданные экземпляры класса MultirotorUAV сохраните в список для последующего     использования
    for drone in used_drones:

        # TODO 4-2
        # При создании каждого экземпляра задайте ему как приватные атрибуты массу и                   производителя из справочника дронов drone_catalog в соответствии с моделью дрона
        drone_sample = MultirotorUAV(
            weight = drone_catalog[drone]["weight"], 
            model = drone, 
            brand = drone_catalog[drone]["brand"]
        )

        # TODO 4-3
        # А также добавьте ему миссии, найденные для этой модели дрона на шаге 2-3
        # Напоминание: миссии находятся в атрибуте missions (с декоратором, и поэтому он               публично доступен) в классе UAV
        for mission in missions_drones[drone]:
            drone_sample.missions.append(mission)
        drone_arr.append(drone_sample)

    # TODO 4-4
    # Напишите код, который выводит информацию по заданной модели дрона. Состав информации:        масса, производитель, количество отлетанных миссий
    # (название модели пользователь вводит с клавиатуры в любом регистре, но без опечаток)
    # Подсказка: для этого вам необходимо вернуться в ЗАДАНИЕ 3 и добавить в класс два             публичных метода: get_info(), который выводит нужную информацию,
    # и get_model, который позволит получить название модели дрона
    # РЕЗУЛЬТАТ:
    # Информация о дроне DJI Mavic 2 Pro: масса 903, производитель DJI, количество миссий 6
    flag = 0
    while flag !=2:
      flag = 0
      try:
        user_input = str(input("Введите модель дрона (полностью) в любом регистре\n"))
        lower_input = user_input.lower()
        chosen_drone = choose_drone(lower_input)
        flag = 2
      except: 
        print("Дрона с таким названием не существует, повторите ввод снова!")
        flag = 1
      
    for drone in drone_arr:
        model = drone.get_model()
        if model == chosen_drone:
            print(f"Информация о дроне {model}: {drone.get_info()}")
