# This script will create different dataSet for my mock-Town. Every dataSet is going to represent a different zone of
# the city, with different prices, square_meters and so on Every single instance is going to generata a random number
# and use that as a multiplication factor for the house properties . This is how I'm going to create a "skeleton" for
# my mock-town system. I'll then use this dataSet to build a fake housing site database that is going to serve for my
# personal projects.

import random
import pandas as pd
import openpyxl

# Create empty lists of houses relative to the different City Zones (names are totally made up)


housesObola = []
housesFornaci = []
housesSanZeno = []
housesRoccalata = []
housesBellaria = []
energy_classes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
r_seller = ['Marconi Immobiliare', 'Pronto Casa', 'Case & Cose', 'Solide Realtà', 'Fundamenta', 'Righi & Figli',
            'Studio Onori', 'Soluzioni Alecco']
r_amenities = ['Ospedale', 'Scuola Materna', 'Scuola Elementare', 'Scuole Medie e Superiori', 'Linea Metropolitana',
               'Fermata Autobus', 'Farmacia', 'Supermercato', 'Mercato Rionale', 'Stazione dei treni',
               'Entrata Tangenziale', 'Palazzetto dello sport', 'Centro storico']


# I'm adding a energyClassifier function that will assign a random value from A to G to the house's energy efficiency.
# This value will influence the house price by up to 20%, and will be appended to the final list of house properties.
# The function will return the price multiplication factor along with the classification letter stored within a tuple
# for easy access within the house generating function itself
def energyClassifier():
    r = random.randrange(0, 7)

    if r == 0:
        energy_factor = 1.2
        energy_class = 'A'
    elif r == 1:
        energy_factor = 1.15
        energy_class = 'B'
    elif r == 2:
        energy_factor = 1.10
        energy_class = 'C'
    elif r == 3:
        energy_factor = 1.05
        energy_class = 'D'
    elif r == 4:
        energy_factor = 1
        energy_class = 'E'
    elif r == 5:
        energy_factor = .95
        energy_class = 'F'
    else:
        energy_factor = .9
        energy_class = 'G'
    return energy_factor, energy_class


# I'll add a randomSeller function that will assign a random operator for each individual house. This is meant to
# simulate an open market with more than one real-estate operator. This may prove interesting to study for pattern
# recognition analytics. As usual, nothing crazy: I'll use a list of random names and assign one to each generated house
# at random by calling the function inside the HouseGenerator. I could implement this function in the energyClassifier
# one but for the moment I'd rather keep everything separated for ease of use
def randomSeller():
    r = random.randrange(0, 8)
    return r_seller[r]


# Same same, the randomAmenities function will define a random number of interesting/important buildings located near
# the house, once again taken from a list I defined at the beginning of the script. all these random functions will be
# collapsed into one at the end of the scripting process (maybe)

def randomAmenities():
    r = random.randrange(1, 5)
    amenities = ",".join(random.sample(r_amenities, r))
    return amenities


# I'll add a function to generate a random house condition: for the time being I'll just go with
# 0:poor ; 1:good ;2: very good . House condition will play a role in price definition

def houseCondition():
    r = random.randrange(0, 4)
    if r == 0:
        c_multiplier = .85
        c = "Da ristrutturare"
    elif r == 1:
        c_multiplier = 1
        c = "Abitabile"
    elif r == 2:
        c_multiplier = 1.15
        c = "Appena ristrutturato"
    else:
        c_multiplier = 1.25
        c = "Di nuova costruzione"
    return c, c_multiplier


# Define functions for the creation of the single house in a set zone This is a bit of a hard-coded solution,
# In future updates I'll try to implement just a single function that takes the zone as an argument,
# but for the moment that is the quickest solution and as such it allows me to start working of
# the system rather than the preparation, updates will follow

def createObola(house_num):
    # "Type" will define is the house is a studio flat (type_0), a flat (type_1) or a standalone house (type_2).
    # More types could be defined. This definition allows me to specify different square meters,
    # price multiplication factor and qualities for different house types
    conditions = houseCondition()
    spec = energyClassifier()
    seller = randomSeller()
    amenities = randomAmenities()
    type = random.randrange(0, 2)
    price_base = 90000
    if type == 0:
        price_base = 70000
        mq_b = 30
        house_rooms = 1
        m_factor = random.uniform(.9, 1.3)
        house_title = "Monolocale in zona Obola"
    elif type == 1:
        mq_b = 60
        house_rooms = random.randrange(2, 5)
        m_factor = random.uniform(.85, 1.5)
        house_title = "Appartamento da " + str(house_rooms) + " Stanze in zona Obola"

    elif type == 2:
        mq_b = 90
        house_rooms = random.randrange(3, 5)
        m_factor = random.uniform(.85, 1.6)
        house_title = "Casa indipendente da " + str(house_rooms) + " Stanze in zona Obola"

    house_mq = round(mq_b * m_factor)
    if house_mq < 100:
        mq_txt = "0" + str(house_mq)
    else:
        mq_txt = str(house_mq)
    if house_num < 10:
        house_id = "A" + str(type) + mq_txt + str(house_rooms) + "0000" + str(house_num)
    elif house_num < 100:
        house_id = "A" + str(type) + mq_txt + str(house_rooms) + "000" + str(house_num)
    elif house_num < 1000:
        house_id = "A" + str(type) + mq_txt + str(house_rooms) + "00" + str(house_num)
    elif house_num < 10000:
        house_id = "A" + str(type) + mq_txt + str(house_rooms) + "0" + str(house_num)
    else:
        house_id = "A" + str(type) + mq_txt + str(house_rooms) + str(house_num)
    house_price = str(round(((price_base * m_factor) * spec[0] * conditions[1]), -3)) + " €"
    house_zona = 'Obola'
    # I'll create a house item with the data I generated and append the item to the zone list

    house = {'ID': str(house_id), 'Title': house_title, 'Rooms': house_rooms, 'Mq': house_mq, 'Zone': house_zona,
             'Price': house_price, 'Condition': conditions[0], 'EnergyClass': spec[1], 'Seller': seller,
             'Close to': amenities}
    housesObola.append(house)


def createFornaci(house_num):
    conditions = houseCondition()
    spec = energyClassifier()
    seller = randomSeller()
    amenities = randomAmenities()
    price_base = 110000
    type = random.randrange(0, 3)
    if type == 0:
        price_base = 90000
        mq_b = 45
        house_rooms = 1
        m_factor = random.uniform(.85, 1.3)
        house_title = "Monolocale in zona Fornaci"
    elif type == 1:
        mq_b = 80
        house_rooms = random.randrange(2, 5)
        m_factor = random.uniform(.9, 1.5)
        house_title = "Appartamento da " + str(house_rooms) + " Stanze in zona Fornaci"

    elif type == 2:
        mq_b = 100
        house_rooms = random.randrange(3, 6)
        m_factor = random.uniform(1.1, 2)
        house_title = "Casa indipendente da " + str(house_rooms) + " Stanze in zona Fornaci"

    house_mq = round(mq_b * m_factor)
    if house_mq < 100:
        mq_txt = "0" + str(house_mq)
    else:
        mq_txt = str(house_mq)
    if house_num < 10:
        house_id = "B" + str(type) + mq_txt + str(house_rooms) + "0000" + str(house_num)
    elif house_num < 100:
        house_id = "B" + str(type) + mq_txt + str(house_rooms) + "000" + str(house_num)
    elif house_num < 1000:
        house_id = "B" + str(type) + mq_txt + str(house_rooms) + "00" + str(house_num)
    elif house_num < 10000:
        house_id = "B" + str(type) + mq_txt + str(house_rooms) + "0" + str(house_num)
    else:
        house_id = "B" + str(type) + mq_txt + str(house_rooms) + str(house_num)
    house_price = str(round(((price_base * m_factor) * spec[0] * conditions[1]), -3)) + " €"
    house_zona = 'Fornaci'

    house1 = {'ID': str(house_id), 'Title': house_title, 'Rooms': house_rooms, 'Mq': house_mq, 'Zone': house_zona,
              'Price': house_price, 'Condition': conditions[0], 'EnergyClass': spec[1], 'Seller': seller,
              'Close to': amenities}
    housesFornaci.append(house1)


def createSanZeno(house_num):
    conditions = houseCondition()
    spec = energyClassifier()
    seller = randomSeller()
    amenities = randomAmenities()
    price_base = 140000
    type = random.randrange(0, 3)
    if type == 0:
        price_base = 120000
        mq_b = 55
        house_rooms = 1
        m_factor = random.uniform(.6, 1.1)
        house_title = "Monolocale in zona San Zeno"
    elif type == 1:
        mq_b = 90
        house_rooms = random.randrange(3, 6)
        m_factor = random.uniform(.8, 1.7)
        house_title = "Appartamento da " + str(house_rooms) + " Stanze in zona San Zeno"

    elif type == 2:
        mq_b = 100
        house_rooms = random.randrange(4, 8)
        m_factor = random.uniform(1.1, 2)
        house_title = "Villetta indipendente da " + str(house_rooms) + " Stanze in zona San Zeno"

    house_mq = round(mq_b * m_factor)
    if house_mq < 100:
        mq_txt = "0" + str(house_mq)
    else:
        mq_txt = str(house_mq)
    if house_num < 10:
        house_id = "C" + str(type) + mq_txt + str(house_rooms) + "0000" + str(house_num)
    elif house_num < 100:
        house_id = "C" + str(type) + mq_txt + str(house_rooms) + "000" + str(house_num)
    elif house_num < 1000:
        house_id = "C" + str(type) + mq_txt + str(house_rooms) + "00" + str(house_num)
    elif house_num < 10000:
        house_id = "C" + str(type) + mq_txt + str(house_rooms) + "0" + str(house_num)
    else:
        house_id = "C" + str(type) + mq_txt + str(house_rooms) + str(house_num)
    house_price = str(round(((price_base * m_factor) * spec[0] * conditions[1]), -3)) + " €"
    house_zona = 'San Zeno'

    house2 = {'ID': str(house_id), 'Title': house_title, 'Rooms': house_rooms, 'Mq': house_mq, 'Zone': house_zona,
              'Price': house_price, 'Condition': conditions[0], 'EnergyClass': spec[1], 'Seller': seller,
              'Close to': amenities}
    housesSanZeno.append(house2)


def createRoccalata(house_num):
    conditions = houseCondition()
    spec = energyClassifier()
    seller = randomSeller()
    amenities = randomAmenities()
    price_base = 170000
    type = random.randrange(0, 3)
    if type == 0:
        price_base = 150000
        mq_b = 50
        house_rooms = 1
        m_factor = random.uniform(.6, 1.2)
        house_title = "Monolocale in zona Roccalata"
    elif type == 1:
        mq_b = 90
        house_rooms = random.randrange(3, 6)
        m_factor = random.uniform(.8, 1.7)
        house_title = "Appartamento da " + str(house_rooms) + " Stanze in zona Roccalata"

    elif type == 2:
        mq_b = 110
        house_rooms = random.randrange(4, 9)
        m_factor = random.uniform(1.1, 2)
        house_title = "Villetta indipendente da " + str(house_rooms) + " Stanze in zona Roccalata"

    house_mq = round(mq_b * m_factor)
    if house_mq < 100:
        mq_txt = "0" + str(house_mq)
    else:
        mq_txt = str(house_mq)
    if house_num < 10:
        house_id = "D" + str(type) + mq_txt + str(house_rooms) + "0000" + str(house_num)
    elif house_num < 100:
        house_id = "D" + str(type) + mq_txt + str(house_rooms) + "000" + str(house_num)
    elif house_num < 1000:
        house_id = "D" + str(type) + mq_txt + str(house_rooms) + "00" + str(house_num)
    elif house_num < 10000:
        house_id = "D" + str(type) + mq_txt + str(house_rooms) + "0" + str(house_num)
    else:
        house_id = "D" + str(type) + mq_txt + str(house_rooms) + str(house_num)
    house_price = str(round(((price_base * m_factor) * spec[0] * conditions[1]), -3)) + " €"
    house_zona = 'Roccalata'

    house3 = {'ID': str(house_id), 'Title': house_title, 'Rooms': house_rooms, 'Mq': house_mq, 'Zone': house_zona,
              'Price': house_price, 'Condition': conditions[0], 'EnergyClass': spec[1], 'Seller': seller,
              'Close to': amenities}
    housesRoccalata.append(house3)


def createBellaria(house_num):
    conditions = houseCondition()
    spec = energyClassifier()
    seller = randomSeller()
    amenities = randomAmenities()
    price_base = 190000
    type = random.randrange(1, 3)
    if type == 1:
        mq_b = 100
        house_rooms = random.randrange(3, 6)
        m_factor = random.uniform(.9, 1.8)
        house_title = "Appartamento da " + str(house_rooms) + " Stanze in zona Bellaria"

    elif type == 2:
        mq_b = 110
        house_rooms = random.randrange(4, 9)
        m_factor = random.uniform(1.1, 2)
        house_title = "Villetta indipendente da " + str(house_rooms) + " Stanze in zona Bellaria"

    house_mq = round(mq_b * m_factor)

    if house_mq < 100:
        mq_txt = "0" + str(house_mq)
    else:
        mq_txt = str(house_mq)
    if house_num < 10:
        house_id = "E" + str(type) + mq_txt + str(house_rooms) + "0000" + str(house_num)
    elif house_num < 100:
        house_id = "E" + str(type) + mq_txt + str(house_rooms) + "000" + str(house_num)
    elif house_num < 1000:
        house_id = "E" + str(type) + mq_txt + str(house_rooms) + "00" + str(house_num)
    elif house_num < 10000:
        house_id = "E" + str(type) + mq_txt + str(house_rooms) + "0" + str(house_num)
    else:
        house_id = "E" + str(type) + mq_txt + str(house_rooms) + str(house_num)
    house_price = str(round(((price_base * m_factor) * spec[0] * conditions[1]), -3)) + " €"
    house_zona = 'Bellaria'

    house4 = {'ID': str(house_id), 'Title': house_title, 'Rooms': house_rooms, 'Mq': house_mq, 'Zone': house_zona,
              'Price': house_price, 'Condition': conditions[0], 'EnergyClass': spec[1], 'Seller': seller,
              'Close to': amenities}
    housesBellaria.append(house4)


# here I'm able to decide how many records I want for every zone, in this case the script will generate 10k houses
# per zone. Ideally (coming in future updates) I could assign a different variable for every function in order not to
# generate dataset of identical length

for i in range(0, 100, 1):
    print(i)
    createObola(i)
    createFornaci(i)
    createSanZeno(i)
    createRoccalata(i)
    createBellaria(i)


# Once the lists are filled with the items, I'm going to use them to create dataSets and save them as xlsx files in
# my directory, this way every time I run the script I'll generate a fully disposable and random set of data that I
# can use for study purpose
def printExcell():
    df = pd.DataFrame(housesObola)
    with pd.ExcelWriter('case_Obola.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')

    df = pd.DataFrame(housesFornaci)
    with pd.ExcelWriter('case_Fornaci.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    df = pd.DataFrame(housesSanZeno)
    with pd.ExcelWriter('case_SanZeno.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    df = pd.DataFrame(housesRoccalata)
    with pd.ExcelWriter('case_Roccalata.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    df = pd.DataFrame(housesBellaria)
    with pd.ExcelWriter('case_Bellaria.xlsx') as writer:
        df.to_excel(writer, sheet_name='Sheet1')


printExcell()
