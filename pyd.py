from pydantic import BaseModel,Field

class Item(BaseModel):
    name: str = Field (example='Ноутбук')
    description:str= Field(example='good Laptop')
    price: float=Field(example=999.99)