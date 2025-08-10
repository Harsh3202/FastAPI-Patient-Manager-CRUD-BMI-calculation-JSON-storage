from pydantic import BaseModel
from typing import List,Dict,Optional
class Address(BaseModel):
    city:str
    pincode: str 
    street: str
class Patient(BaseModel):
    name:str
    age:int
    allergies: List[str] ## if we would have written list then inside the list we could have written any type      and it would accept it
    married: Optional[bool] = False
    contact_details: Dict[str,str]  ## if we would have written dict then inside the dict we could have written any type      and it would accept it
    address: Address
    
def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.married)
    print(patient.address)
    print('inserted')
address_info = {'city':'Kolkata','pincode': '711202','street':'G.T.Road'}
address1 = Address(**address_info)
patient_info = {'name': 'nitish', 'age': 30,'allergies': ['pollen','dust'],'contact_details':{'gaon':'bally','email_id':'abc@gmail.com'},'address': address1}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
