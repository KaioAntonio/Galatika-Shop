from http.client import responses
from fastapi import APIRouter, Body
from models.cart import Cart
from models.product import Product
from models.section import Section
from routers.user_router import get_current_user


router = APIRouter()
responses_custom = {
        422: {
            "content": {
                "application/json": {
                    "example": {"status": 422, "message": "validation error"}
                }
            },
        },
        200: {
            "content": {
                "application/json": {
                    "example": {"status": 200, "message": "method sucess"}
                }
            },
        },
    }

@router.post("/v1/cart/", tags=["Cart"], description="Insert products a Cart", responses=responses_custom, )
def insert_cart(new_products: Cart = Body(
        default={
        "products_cart": "84307b01-6d82-4268-9069-d80105c56f42,84307b01-6d82-4268-9069-1231234124"
        }
    )):
    products = new_products.products_cart.replace(",", " ")
    email = new_products.email
    products_split = products.split()
    product_erro = 0
    product_list = []
    for i in range(len(products_split)):
        if not Product.find_by_id_products(products_split[i]):
            product_erro += 1
    if product_erro > 0:
         return {'status': 422, "message": "product id don't exists!"}
    else:
        if new_products.read_cart(new_products.email):
            product_list.append(new_products.read_cart(new_products.email))
            for i in range(len(products_split)):
                product_list[0]['products_cart'].append(products_split[i])
                print(product_list[0]['products_cart'])
                new_products.patch_products_cart(product_list[0]['products_cart'], email)
        return {'status': 200, "message": "Products adds with sucess"} 
        

@router.get("/v1/cart/{email}", tags=["Cart"], description="Read cart by email of current user", responses= responses_custom)
def get_cart(email: str):
    cart = Cart()
    return cart.read_cart(email)

@router.delete("/v1/cart/", tags=["Cart"], description="Delete cart products by email of current user",
responses= responses_custom)
def delete_product_cart(cart: Cart):
    email = cart.email
    products = cart.products_cart
    if cart.read_cart(email):
        cart.delete_products_cart(products,email)
        return {"message": "Product(s) delete with success"}
    else:
        return {"message": "Error in delete product"}
    
    