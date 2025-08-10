from fastapi import FastAPI, Path, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal,Optional
import json

app = FastAPI(title="Patient Management System API")


# ----------------- Patient Model -----------------
class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the Patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the Patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the Patient")]
    gender: Annotated[Literal['male', 'female', 'other'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the Patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the Patient in kilograms")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25.0:
            return "Normal"
        elif self.bmi < 30.0:
            return "Overweight"
        else:
            return "Obese"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'other']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None,gt=0)]
    weight: Annotated[Optional[float], Field(default=None,gt=0)]
# ----------------- Utility Functions -----------------
def load_data():
    try:
        with open('patient.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return empty dict if file doesn't exist


def save_data(data):
    with open('patient.json', 'w') as f:
        json.dump(data, f, indent=4)


# ----------------- Routes -----------------
@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional Patient Management System API to manage patient records"}


@app.get("/view")
def view_all_patients():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="ID of the patient", examples=["P001"])
):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort on the basis of height, weight, bmi"),
    order: str = Query("asc", description="Sort order: asc or desc")
):
    valid_fields = ["weight", "height", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field. Choose from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Choose 'asc' or 'desc'")

    data = load_data()
    reverse = True if order == "desc" else False
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by), reverse=reverse)
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exists")

    # Include computed fields when saving
    data[patient.id] = patient.model_dump(exclude=["id"])
    save_data(data)

    return JSONResponse(status_code=201, content={"message": "Patient created successfully"})

@app.put("/edit/{Patient_id}")
def  update_patient(Patient_id: str, updatepatient:PatientUpdate):
    
    
    data = load_data()
    
    # check patient id presence
    if Patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #extract that patient detail
    exisiting_data_info = data[Patient_id]
    
    #extract updated fields and data
    new_patient_info = updatepatient.model_dump(exclude_unset=True)
    
    #inserting upated fields and data in existing one
    for key,value in new_patient_info.items():
        exisiting_data_info[key]= value
        
    #Computing bmi, verdict 
    #existing Patient info -> pydantic object -> updated bmi + weight 
    exisiting_data_info['id'] = Patient_id
    new_pydantic_obj = Patient(**exisiting_data_info)
    
    #pydantic object -> dict
    new_updated_data_info = new_pydantic_obj.model_dump(exclude="id")
    
    #add dict to data
    data[Patient_id] = new_updated_data_info
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient updated successfully"})
    
@app.delete('/delete/{Patient_id}')
def delete_patient(Patient_id:str):
    
    data = load_data()
    
    if Patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    del data[Patient_id]
    
    save_data(data)
    
    return JSONResponse(status_code=200, content={"message": "Patient deleted successfully"})
