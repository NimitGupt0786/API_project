from fastapi import FastAPI,Query,HTTPException
from pydantic import BaseModel
from typing import Optional
import json

app=FastAPI()

class Person(BaseModel):
    id:Optional[int]=None
    name:str
    age:int
    gender:str

with open("people.json","r") as f:
    people = json.load(f)

@app.get('/person/{p_id}',status_code=200)
def get_person(p_id: int):
    ans=[i for i in people if i['id'] == p_id]
    return ans[0] if len(ans)>0 else {}

@app.get('/search',status_code=200)
def search(a_ge: Optional[int]=Query(None),
           n_ame: Optional[str]=Query(None)):

    p = [i for i in people if i['age'] == a_ge]

    if n_ame is None:
        if a_ge is None:
            return people
        else:
            return p

    d = [i for i in people if i['name'].lower() == n_ame.lower()]

    if a_ge is None:
        if n_ame is not None:
            return d
    if a_ge is not None:
        if n_ame is not None:
            e=[i for i in p if i in d]
            return e


@app.post('/adduser')
def add_person(person: Person):
    new_id=max([p['id'] for p in people]) + 1
    new_person={
        'id':new_id,
        'name':person.name,
        'age':person.age,
        'gender':person.gender
    }
    people.append(new_person)
    with open('people.json','w') as f:
        json.dump(people,f)

    return new_person
@app.put("/changeperson")
def change_person(person:Person):
    new_person={
        'id':person.id,
        'name':person.name,
        'age':person.age,
        'gender':person.gender
    }
    p_list=[i for i in people if i['id']==person.id]
    if len(p_list)>0:
        people.remove(p_list[0])
        people.append(new_person)
        with open('people.json', 'w') as f:
            json.dump(people, f)
        return new_person
    else:
        return HTTPException(status_code=404,detail="person does not exist")

@app.delete("/delete/{p_id}")
def delete_person (p_id: int) :
    person = [p for p in people if p['id'] == p_id]
    if len (person) > 0:
        people.remove (person [0])
        with open('people.json', 'W') as f:
            json.dump (people, f)
    else:
        return HTTPException(status_code=404,detail="person does not exist")

