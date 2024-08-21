from complementizer.type import TypeField
from faker import Faker
import random
import requests

class Field:
    
    def __init__(self, name: str, type: TypeField, male: bool, faker: Faker, **info):
        self.name = name
        self.type = type
        self.info = info

        if male:
            if self.type == TypeField.NAME_FULL:
                full_name = faker.name_male()
                pronomes_tratamento = ["Sr.", "Sra.", "Dr.", "Dra.", "Prof.", "Profa."]
                for pronome in pronomes_tratamento:
                    if full_name.startswith(pronome):
                        full_name = full_name.replace(pronome, "").strip()
                self.data = full_name
                
            if self.type == TypeField.NAME_FIRST:
                self.data = faker.first_name_male()
            if self.type == TypeField.NAME_LAST:
                self.data = faker.last_name_male()
            if self.type == TypeField.SEX:
                self.data = 'man'
        else:
            if self.type == TypeField.NAME_FULL:
                full_name = faker.name_female()
                pronomes_tratamento = ["Sr.", "Sra.", "Dr.", "Dra.", "Prof.", "Profa."]
                for pronome in pronomes_tratamento:
                    if full_name.startswith(pronome):
                        full_name = full_name.replace(pronome, "").strip()
                self.data = full_name
            if self.type == TypeField.NAME_FIRST:
                self.data = faker.first_name_female()
            if self.type == TypeField.NAME_LAST:
                self.data = faker.last_name_female()
            if self.type == TypeField.SEX:
                self.data = 'woman'

        if self.type == TypeField.ADDRESS:
            self.data = str(faker.address()).replace('\n', ' ')
        if self.type == TypeField.STREET:
            self.data = faker.street_name()
        if self.type == TypeField.NUMBER:
            self.data = faker.port_number()
        if self.type == TypeField.DISTRICT:
            self.data = faker.bairro()
        if self.type == TypeField.POSTAL:
            self.data = faker.postcode()
        if self.type == TypeField.CITY:
            self.data = faker.city()
        if self.type == TypeField.STATE:
            self.data = faker.state_abbr()
        if self.type == TypeField.COUNTRY:
            self.data = faker.country()
        if self.type == TypeField.DATE_OF_BIRTH:
            self.data = str(faker.date_of_birth(**self.info))
        if self.type == TypeField.PHONE:
            self.data = faker.phone_number()
        if self.type == TypeField.EMAIL:
            self.data = faker.email()
        if self.type == TypeField.PASSWORD:
            self.data = faker.password(15, True, True, True, True)
        if self.type == TypeField.COMPANY:
            self.data = faker.company()
        if self.type == TypeField.CATEGORY:
            self.data = faker.job()
        if self.type == TypeField.CPF:
            self.data = faker.cpf()
        if self.type == TypeField.CHOICES:
            self.data = faker.random_element(self.info['choices'])
        if self.type == TypeField.BOOLEAN:
            self.data = faker.boolean(chance_of_getting_true=50)

class Dependency:

    def __init__(self, name, values) -> None:
        self.name = name
        self.values = values

class Default():

    def __init__(self, name: str, value):
        self.name = name
        self.value = value

class Form:
    
    def __init__(self, table: str, complementizer):
        self.faker = Faker(locale = 'pt_br', )
        self.table = table
        self.fields: list[Field] = []
        self.defaults: list[Default] = []
        self.dependencies: list[Dependency] = []
        self.male: bool = self.faker.boolean(50)
        self.comp = complementizer
    
    def createField(self, name: str, type: TypeField, **info):
        field = Field(name, type, self.male, self.faker, **info)
        self.fields.append(field)
        return field
    
    def createDependecy(self, name, path):
        response = requests.get(self.comp.url_base + path, headers = { 'Authorization': 'Token ' + self.comp.token }) 
        
        values = []
        for temp in response.json():
            values.append(temp['id'])

        dependency = Dependency(name, values)       
        self.dependencies.append(dependency)
        return dependency

    def createDefault(self, name, value):
        default = Default(name, value)
        self.defaults.append(default)
        return default

    def generate(self):
        data = {}

        for field in self.fields:
            data[field.name] = field.data
        for default in self.defaults:
            data[default.name] = default.value
        for dependency in self.dependencies:
            data[dependency.name] = dependency.values[random.randint(0, len(dependency.values) - 1)]

        return data