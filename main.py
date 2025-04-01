from fastapi import FastAPI, Query, Path,HTTPException
from typing import Annotated
import pyd
app=FastAPI()

products=[
    {'id':1,'name':'milk','price':50,'description':'milk 1l'},]

@app.get("/items/",response_model=list[pyd.Item])
def show_items(name:str=Query(default=None,min_length=2),min_price:int=Query(default=None,gt=0),max_price:int=Query(default=None,gt=0), limit:Annotated[int,Query(lt=100)]=10):
    if max_price and min_price:
        if max_price <= min_price:
            raise HTTPException(
                status_code=400,
                detail="max_price must be greater than min_price"
            )
    filtered_products = [
        product for product in products
        if (name is None or name.lower() in product['name'].lower()) and
           (min_price is None or product['price'] >= min_price) and
           (max_price is None or product['price'] <= max_price)
    ]
    
    return filtered_products[:limit]

@app.get("/items/{item_id}")
def show_item(item_id:int=Path(gt=0)):
    for product in products:
        if product['id'] == item_id:
            return product
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/")
def create_item(item:pyd.Item):
    item_id = len(products) + 1
    new_item = item.model_dump()
    new_item['id'] = item_id
    products.append(new_item)
    return new_item
