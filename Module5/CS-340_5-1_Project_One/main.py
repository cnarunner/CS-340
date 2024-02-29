from animalShelter import AnimalShelter
import datetime
CRUD = AnimalShelter()

####################################################################################
#                                    TESTS                                         #
####################################################################################

#
# Good create() test
#
print("\nTEST :: create() :: SHOULD EVALUATE TO TRUE")
date = datetime.datetime.now()
newAnimalTestData = {
    'age_upon_outcome': '10 years',
    'animal_id': 'BGJ0715',
    'animal_type': 'Dog',
    'breed': 'Border Collie',
    'color': 'Black and White',
    'date_of_birth': '2013-11-19',
    'datetime': f"{date.year}-{date.month}-{date.day} {date.hour}:{date.minute}:{date.second}",
    'name': 'Doug',
    'outcome_subtype': 'SCRP',
    'outcome_type': 'Transfer',
    'sex_upon_outcome': 'Neutered Male',
    'location_lat': 30.6525984560228,
    'location_long': -97.7419963476444,
    'age_upon_outcome_in_weeks': 533
}

created = CRUD.create(
    newAnimalTestData)
print(f"Item created: {created}")

#
# Good read() test
#
print("\nTEST :: read() :: SHOULD EVALUATE TO 1")

read_count = CRUD.read(
    {"animal_id": "BGJ0715"})

print(f"There are {read_count} document(s) that fit the query.")

#
# Good update() test
#
print("\nTEST :: update() :: SHOULD EVALUATE TO 1")

updated_count = CRUD.update(
    {"animal_id": "BGJ0715"},
    {"outcome_type": "Adopted"})

print(CRUD.read({"animal_id": "BGJ0715"}))
print(f"There was {updated_count} document(s) changed.")

#
# Good delete() test
#
print("\nTEST :: delete() :: SHOULD EVALUATE TO 1")
deleted_count = CRUD.delete(
    {'animal_id': 'BGJ0715'})
print(f"There was {deleted_count} document(s) deleted.")
