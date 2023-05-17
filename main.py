countries = []
completedCountries = {}
day = 0
lowerCoordinatesLimit = 1
upperCoordinatesLimit = 10
startValue = 1000000
valueToSend = 1000
daysLimit = 10000

# Класи для ініціації програми
class Country: # Клас, який уособлює країну
    def __init__(self, name, xl, yl, xh, yh): # Ініціалізація атрибутів країни
        self.name = name
        self.xl = int(xl)
        self.yl = int(yl)
        self.xh = int(xh)
        self.yh = int(yh)
        self.cities = []
        self.completed = False
        self.connected = False

    def SetCities(self): # Створення записів про міста країни
        self.cities = [
            City(x, y, self.name, countries) 
            for y in range(self.yl, self.yh + 1) 
            for x in range(self.xl, self.xh + 1)
        ]

    def Day(self): # Емуляція денного існування країни
        for city in self.cities:
            city.Day()

    def IsCompleted(self): # Встановлює статус країни, як завершений, якщо її кожне місто завершене
        for city in self.cities:
            if not city.IsCompleted():
                return False
        self.completed = True
        return True

    def Update(self): # Оновлює інформацію про місто після денного існування
        for city in self.cities:
            city.Update()

class City: # Клас, який уособлює місто країни
    def __init__(self, x, y, country, coinsNames): # Ініціалізація атрибутів міста
        self.x = x
        self.y = y
        self.country = country
        self.coins = {}
        self.previousCoins = {}
        for coin in coinsNames: # Ініціалізація початкових "монет" міста
            if coin.name == country:
                self.previousCoins[country] = startValue
                self.coins[country] = startValue
            else:
                self.previousCoins[coin.name] = 0
                self.coins[coin.name] = 0

    def Exist(self, x, y): # Перевірка, чи існує місто з даними координатами
        for country in countries:
            for city in country.cities:
                if city.x == x and city.y == y:
                    return city
        return None

    def SendCoinsToNeighbor(self, x, y): # Надсилання монет місту, яке знаходиться по сусідству, якщо воно існує
        city = self.Exist(x, y)
        self.SendCoins(city)

    def SendCoins(self, city): # Надсилання монет місту
        if city:
            for country in self.coins.keys():
                city.coins[country] += int(self.previousCoins[country] / valueToSend)
                self.previousCoins[country] -= int(self.previousCoins[country] / valueToSend)
                
    def Day(self): # Емуляція процесу денного проживання міста
        self.SendCoinsToNeighbor(self.x, self.y + 1)
        self.SendCoinsToNeighbor(self.x, self.y - 1)
        self.SendCoinsToNeighbor(self.x + 1, self.y)
        self.SendCoinsToNeighbor(self.x - 1, self.y)

    def Update(self): # Оновлення даних про місто
        self.previousCoins = self.coins

    def IsCompleted(self): # Перевірка, чи є місто завершеним
        for coin in self.coins.keys():
            if self.coins[coin] < 1:
                return False
        return True

# Перевірка правильності вводу даних та правильності виконання методів
def CheckInputData(): # Перевірка правильності введених даних
    data = input()
    dataWords = data.split(' ')
    count = len(dataWords)
    if count != 5:
        return None
    name = dataWords[0]
    if len(name) > 25:
        print("Надто велика назва країни")
        return None
    dataWordsDictionary = {'name': name}
    dataWordsDictionary['xl'] = int(dataWords[1])
    dataWordsDictionary['yl'] = int(dataWords[2])
    dataWordsDictionary['xh'] = int(dataWords[3])
    dataWordsDictionary['yh'] = int(dataWords[4])
    return dataWordsDictionary

def CheckRange(number): # Перевірка, чи є країна в межах координат
    return int(number) >= lowerCoordinatesLimit and int(number) <= upperCoordinatesLimit

def CheckPoints(xl, yl, xh, yh): # Перевірка, чи координати "найнижчого" міста країни не є більшими за координати "найвищого" міста
    return xl <= xh and yl <= yh

def CountryExist(countryName): # Перевірка, чи вже є країна з такою назвою
    return countryName in {country.name for country in countries}

def CheckData(data): # Перевірка, чи є країна за цими координатами
    if not IsFree(data['xl'], data['yl'], data['xh'], data['yh']) or not CheckRange(data['xl']) \
    or not CheckRange(data['yl']) or not CheckRange(data['xh']) or not CheckRange(data['yh']) \
    or not CheckPoints(data['xl'], data['yl'], data['xh'], data['yh']):
        return True
    return False

def IsFree(xl, yl, xh, yh): # Перевірка, чи вільні координати, на які претендує нова країна
    for country in countries:
        if HasPoint(country, xl, yl, xh, yh):
            return False
    return True

def HasPoint(country, xl, yl, xh, yh): # Перевірка, чи вільні координати, на які претендує нова країна
    return CheckLeftLower(country, xl, yl) or CheckLeftUpper(country, xl, yh) or CheckRightLower(country, yl, xh) or CheckRightUpper(country, xh, yh)

def CheckLeftLower(country, xl, yl): # Перевірка, чи вільне місце за лівою нижньою координатою
    return xl >= country.xl and xl <= country.xh and yl >= country.yl and yl <= country.yh

def CheckLeftUpper(country, xl, yh): # Перевірка, чи вільне місце за лівою верньою координатою
    return xl >= country.xl and xl <= country.xh and yh >= country.yl and yh <= country.yh

def CheckRightLower(country, yl, xh): # Перевірка, чи вільне місце за правою нижньою координатою країни
    return yl >= country.yl and yl <= country.yh and xh >= country.xl and xh <= country.xh

def CheckRightUpper(country, xh, yh): # Перевірка, чи вільне місце за правою верхньою координатою країни
    return yh >= country.yl and yh <= country.yh and xh >= country.xl and xh <= country.xh

def CheckInputValidation(count): # Вивід перевірок
    global countries, completedCountries, day
    countries = []
    completedCountries = {}
    day = 0
    position = 0
    while position < count:
        data = []
        try:
            data = CheckInputData()
        except Exception as e:
            print("Координати країни введено неправильно")
            continue
        if not data:
            print("Спробуйте ввести назву країни та її координати ще раз")
            continue
        elif CountryExist(data['name']):
            print("Країна вже існує")
            continue
        elif CheckData(data):
            print("Невалідні координати країни")
            continue
        countries.append(Country(data['name'], data['xl'], data['yl'], data['xh'], data['yh']))
        position += 1

def CheckCompleted(): # Перевірка країн на рахунок їх завершеності
    global day
    for country in countries:
        if BeNotInCompleted(country):
            completedCountries[country] = day
        if len(countries) == 1:
            completedCountries[country] = 0

def BeNotInCompleted(country): # Встановлення країн, що не були завершеними
    return country not in completedCountries.keys() and country.completed

def SortName(country): # Сортування країн за назвою
    return country.name

def SortDays(country): # Сортування країн за днем "завершеності"
    return completedCountries[country]

def ShowCompleted(): # Вивід результату обчислення кількості днів
    l = list(completedCountries)
    l.sort(key=SortDays)
    l.sort(key=SortName)
    for country in l:
        print('{} {}'.format(country.name, completedCountries[country]))

def CheckConnections(): # Перевірка порядку зв'язаності міст
    count = 1
    length = len(countries)
    while count < length:
        countriesTemp = countries[: count+1]
        country = countriesTemp[count]
        connected = CheckNear(country, countriesTemp)
        if not connected:
           return False
        count += 1
    return True

def CheckNear(country, countriesTemp): # Перевірка міста на сусідні міста
    for city in country.cities:
        s = city.Exist(city.x, city.y - 1)
        w = city.Exist(city.x - 1, city.y)
        e = city.Exist(city.x + 1, city.y)
        n = city.Exist(city.x, city.y + 1)
        cities = [n, e, s, w]
        for country in countriesTemp:
            name = country.name
            if name == city.country:
                continue
            connected = CityFound(cities, name)
            if connected:
                return True
    return False

def CityFound(cities, name): # Перевірка, чи є місто за сусідніми координатами
    for c in cities:
        if c and c.country == name:
                return True
    return False

# Методи для обчислення параметрів задачі
def Set(): # Встановлення даних про міста країни
    for country in countries:
        country.SetCities()

def Complete(): # Процес існування країн до завершення кожної з них
    length = len(countries)
    while length != len(completedCountries.keys()):
        Day()

def Day(): # Емуляція одного дня
    global day
    day += 1
    for country in countries:
            country.Day()
            country.Update()
            country.IsCompleted()
            CheckCompleted()

# MAIN
def Main():
    count = 0
    while True:
        try:
            count = int(input())
        except Exception as e:
            print("Некоректне введення числа країн")
            continue
        if count < 0 or count > 20:
            print("Неправильно введене число країн")
            continue
        if not count:
            break
        else:
            CheckInputValidation(count)
            Set()
            if not CheckConnections():
                print("Порушений порядок зв'язаності міст")
                continue
            Complete()
            ShowCompleted()
            if day > daysLimit:
                break

if __name__ == '__main__':
    Main()