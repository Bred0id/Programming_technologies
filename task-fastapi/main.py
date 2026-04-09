from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
import time

app = FastAPI()

class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"

class Dog(BaseModel):
    name: str
    pk: Optional[int] = None
    kind: DogType
    
class Timestamp(BaseModel):
    id: int
    timestamp: int
    
dogs: List[Dog] = []
max_pk = 0
current_time = Timestamp(id=1, timestamp=int(time.time()))
    
@app.get("/")
def root():
    return {"message": "Welcome to the best veterinary clinic for dogs"}

@app.get("/dog")
def get_dogs_by_kind(kind: Optional[DogType] = None):
    dogs_with_correct_type = []
    for dog in dogs:
        if kind is None or dog.kind == kind:
            dogs_with_correct_type.append(dog)
    return dogs_with_correct_type

@app.get("/dog/{pk}")
def get_dog(pk: int):
    for dog in dogs:
        if dog.pk == pk:
            return dog
    raise HTTPException(status_code=404, detail="Dog not found")

@app.post("/post")
def get_timestamp():
    current_time.id += 1
    current_time.timestamp = int(time.time())
    return current_time

@app.post("/dog")
def add_dog(new_dog: Dog):
    global max_pk
    if new_dog.pk is None:
        new_dog.pk = max_pk
        max_pk += 1
    for dog in dogs:
        if new_dog.pk == dog.pk:
            raise HTTPException(status_code=409, detail="Dog with this pk already exists")
    dogs.append(new_dog)
    max_pk = max(max_pk, new_dog.pk)
    return new_dog

@app.patch("/dog/{pk}")
def change_dog(pk: int, changed_dog: Dog):
    for dog in dogs:
        if dog.pk == pk:
            dog.name = changed_dog.name
            dog.kind = changed_dog.kind
            return dog
    raise HTTPException(status_code=404, detail="Dog not found")
            