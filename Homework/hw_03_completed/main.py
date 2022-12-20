import json
import csv
import re

# В ЭТОМ ДЗ ВЫ БУДЕТЕ АНАЛИЗИРОВАТЬ ДАННЫЕ ОБ АВИАПРОИСШЕСТВИЯХ С УЧАСТИЕМ МОДЕЛЕЙ ДРОНОВ ИЗ ВАШИХ ИСХОДНЫХ ДАННЫХ В .JSON

# =====================================
# ЗАДАНИЕ 1: Классы - декораторы
# =====================================
# TODO 1-1 - Добавить атрибут incidents типа список
# Возьмите код из предыдущего ДЗ
# Добавьте в класс MultirotorUAV атрибут incidents и внесите туда информацию обо всех найденных происшествиях для этой модели
# Не забудьте, что атрибут добавляется при помощи декоратора

class Aircraft:
    def __init__(self, weight):
        self._weight = weight

class UAV:
    def __init__(self):
        self._has_autopilot = True
        self._missions = []

    @property
    def missions(self):
        return self._missions 

    @missions.setter
    def missions(self, mission):
        self._missions.append(mission)

    def count_missions(self):
        count = len(self.missions)
        return count        

      
class MultirotorUAV(Aircraft, UAV):

    def __init__(self, weight, model, brand):
        super().__init__(weight)
        UAV.__init__(self)
        self.__weight = weight
        self.__brand = brand
        self.__model = model
      
        # добавьте приватный атрибут incidents
        self.__incidents = []

    def get_info(self):
        return f"масса: {self.__weight}, производитель: {self.__brand}, количество миссий: {self.count_missions()}"

    def get_model(self):
        return self.__model
      
    def get_weight(self):
       return self.__weight

    def get_brand(self):
      return self.__brand

	# напишите код декоратора для атрибута incidents. Не забудьте сначала добавить приватный атрибут в класс
    @property
    def incidents(self):
        return self.__incidents

	# напишите публичный метод add_incident, который добавляет инцидент в список инцидентов для данной модели дрона
    def add_incident(self, incident):
        self.__incidents.append(incident)

	# напишите публичный метод save_data, который сохраняет информацию о дроне в файл json
    def save_data(self):
      path = "incidents_" + self.__class__.__name__ + "_" + self.get_model() + ".json"
      tmp = dict()
      tmp.setdefault("model", self.get_model())
      tmp.setdefault("weight", self.get_weight())
      tmp.setdefault("brand", self.get_brand())
      tmp.setdefault("missions", self.missions)
    
      incidents_tmp = []
      for incident in self.incidents:
        incidents_tmp.append(incident)

      tmp.setdefault("incidents", incidents_tmp)
      with open(path, 'w') as f:
        json.dump(tmp, f, ensure_ascii=False, allow_nan=False, indent=4, separators = (',', ':'))

      return tmp

def missions_by_pilot(pilot, data):
    return data[pilot]["missions"]

def missions_by_pilots(data):
    missions_count_by_pilots = {}
    for pilot in data.keys():
        missions = missions_by_pilot(pilot, data)
        missions_count_by_pilots[pilot] = len(missions)

    return dict(sorted(missions_count_by_pilots.items(), key=lambda item: item[1], reverse=True))

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

# код из предыдущего ДЗ, необходимый для решения этого ДЗ (чтение данных о пилотах, сбор информации о дронах и пр.):
def read_json(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

if __name__ == "__main__":  
  
  filename = "pilot_path.json"
  json_data = read_json(filename)
  
  drone_catalog = {
        "DJI Mavic 2 Pro": {"weight": 903, "brand": "DJI"},
        "DJI Mavic 2 Zoom": {"weight": 900, "brand": "DJI"},
        "DJI Mavic 2 Enterprise Advanced": {"weight": 920, "brand": "DJI"},
        "DJI Inspire 2": {"weight": 1500, "brand": "DJI"},
        "DJI Mavic 3": {"weight": 1000, "brand": "DJI"}
    }
  
  missions_drones = missions_by_drones(json_data)
  drone_arr = []
  
  used_drones = all_drone_types(json_data)
  for drone in used_drones:
        drone_sample = MultirotorUAV(
            weight = drone_catalog[drone]["weight"], 
            model = drone, 
            brand = drone_catalog[drone]["brand"]
        )
    
        for mission in missions_drones[drone]:
            drone_sample.missions.append(mission)
        drone_arr.append(drone_sample)

  # =====================================
  # ЗАДАНИЕ 2: Файлы - CSV
  # =====================================
  # TODO 2-1 - Загрузите информацию об авиапроисшествиях из файла csv
  # Проверьте по моделям (названия моделей возьмите из экземпляров класса MultirotorUAV), какие из них участвовали в авиапроисшествиях

  # код чтения данных из файла:
  with open ("faa_incidents.csv") as filename_csv:
    csv_data = csv.reader(filename_csv)
    #for line in csv_data:
      #print (line)
  
  # =====================================
  # ЗАДАНИЕ 3: Классы
  # =====================================
  # TODO 3-1 - Для каждой модели дрона добавьте в экземпляр класса информацию об авиапроисшествиях, в которых участвовала эта модель
  # Информацию сохраните в атрибут incidents (используйте декораторы)
  # Подсказка: вот так вы получаете названия модели для каждого экземпляра класса MultirotorUAV
  # Экземпляры все так же находятся в списке (например, drones_cls_list)

  #проверка происшествий по моделям
  with open ("faa_incidents.csv") as filename_csv:
    csv_data = csv.reader(filename_csv)
    for line in csv_data:
      my_st = str(line).split("', ")
      for drone in drone_arr:
        drone_name = str(drone.get_model()).replace("DJI ","")
        for st in my_st:
          incident = re.search(drone_name, str(st), re.I)
          if incident != None:
            drone.add_incident(incident.string)
    
  # TODO 3-2 - Добавьте в класс MultirotorUAV публичный метод save_data, который сохраняет статистику по дрону в файл
  # Внимание! Метод save_data не принимает параметры. Название файла сформируйте как: название класса + название модели + расширение .json
  # например: "MultirotorUAV_DJI Mavic 2 Pro.json"
  # Подсказка: название класса вы можете получить вот так: self.__class__.__name__
  # используйте ключи: "model", "weight", "brand", "missions", "incidents"
  # например: {"model":"DJI Inspire 2", "weight": 1500, "info": "...", "manufacturer": "DJI", "missions": [], "incidents": []}
  # код в объявлении класса дописан
  
  # =====================================
  # ЗАДАНИЕ 4: Регулярные выражения
  # =====================================
  # TODO 4-1 - Выведите на экран собранную информацию по инцидентам по каждому дрону в таком виде:
  # модель: инцидентов - количество
  # 1 - краткий текст инцидента*
  # полный текст инцидента
  # * - краткий текст инцидента получайте следующим образом: в исходном тексте инцидента найдите модель, например, INSPIRE 2,
  # и выведите все предложения, в которых встречается упоминание этой модели
  # код:
  
  for drone in drone_arr:
      print(f"\n{drone.get_model()}: инцидентов - {len(drone.incidents)}\n")
      if len(drone.incidents)!=0:
        i=1
        for incident in drone.incidents:
          drone_incidents = incident.split(".")
          short_inc=""
          print(f"\nИнцидент {i}:\n\n", end='')
          for d_incident in drone_incidents:
            if str(drone.get_model()).replace("DJI ","").upper() in str(d_incident):
              short_inc=short_inc+d_incident+"."
          print("Краткое описание:\n", short_inc)
          print("\nПолное описание:\n", str(incident))
          i+=1
    
   
  
  # TODO 4-2 - После вывода информации об инциденте сохраните всю информацию о дроне в файл .json при помощи метода save_data
  # код:
  for drone in drone_arr:
    drone.save_data()
  
  # РЕЗУЛЬТАТ:
  # см. приложенные файлы в файлах с названием incidents_MultirotorUAV_(drone_name)
