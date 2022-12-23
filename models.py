from tortoise import Model
from pydantic import BaseModel
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from datetime import datetime
from typing import Literal

# Referrences:
# https://stackoverflow.com/questions/7296846/how-to-implement-one-to-one-one-to-many-and-many-to-many-relationships-while-de


class User(Model):
    # fields are null = False by default but i specified it for clarity
    id = fields.IntField(pk=True, index=True)
    username = fields.CharField(max_length=20, null=False, unique=True)
    email = fields.CharField(max_length=200, null=False, unique=True)
    password = fields.CharField(max_length=100, null=False)
    is_verified = fields.BooleanField(default=True)
    join_date = fields.DatetimeField(default=datetime.utcnow)


class Business(Model):
    id = fields.IntField(pk=True, index=True)
    business_name = fields.CharField(
        max_length=20, nullable=False, unique=True)
    city = fields.CharField(max_length=100, null=False, default="Unspecified")
    region = fields.CharField(
        max_length=100, null=False, default="Unspecified")
    business_description = fields.TextField(null=True)
    logo = fields.CharField(max_length=200, null=False, default="default.jpg")
    owner = fields.ForeignKeyField('models.User', related_name='business')


class Product(Model):
    # 12 signinficant digits, 2 of the significant digits are decimals.
    id = fields.IntField(pk=True, index=True)
    name = fields.CharField(max_length=100, null=False, index=True)
    main_category = fields.CharField(
        max_length=30, index=True, null=True,
        # specify the allowed values for the category field using Literal
        typing=Literal[
            "Clothes",
            "Electronics",
            "Household Appliances",
            "Accommodation",
            "Cars and supplies",
            "Furniture",
            "Other"
        ]
    )
    category = fields.CharField(
        max_length=30, index=True,
        # specify the allowed values for the category field using Literal
        typing=Literal[
            "Women’s Clothing", "Men’s Clothing", "Children’s Clothing",
            "Phones and tablets", "Photo and video cameras", "computers", "TV, audio systems",
            "Refrigerators", "Stoves and ovens", "Washing machines", "Climatic equipment", "Other appliances",
            "Apartment for sale", "Houses for sale", "Apartment rent", "Houses rent",
            "Cars", "Motorcycles", "Buses and Trucks", "Special machinery", "Trailers",
            "Spare parts and wheels", "Accessories and equipment", "Car care products",
            "Beds and mattresses", "Tables and Chairs", "Sofas and armchairs", "Kitchen sets", "Storing",
            "Services", "Sports and recreation", "Books and hobbies", "Pets", "Job", "Other ungrouped"
        ]
    )
    original_price = fields.DecimalField(max_digits=12, decimal_places=2)
    new_price = fields.DecimalField(max_digits=12, decimal_places=2)
    percentage_discount = fields.IntField()
    offer_expiration_date = fields.DateField(default=datetime.utcnow)
    product_image = fields.CharField(
        max_length=200, null=False, default="productDefault.jpg")
    date_published = fields.DatetimeField(default=datetime.utcnow)
    # the value for percentage_discount will be computed and
    # added using storing user input in the routes

    business = fields.ForeignKeyField(
        'models.Business', related_name='products')


# user_pydanticIn will be used to create users since it allows
# readOnly fields same for all the others
user_pydantic = pydantic_model_creator(
    User, name="User", exclude=("is_verified",))
user_pydanticIn = pydantic_model_creator(
    User, name="UserIn", exclude_readonly=True, exclude=("is_verified", 'join_date'))
user_pydanticOut = pydantic_model_creator(
    User, name="UserOut", exclude=("password", ))

business_pydantic = pydantic_model_creator(Business, name="Business")
business_pydanticIn = pydantic_model_creator(
    Business, name="Business", exclude_readonly=True)


product_pydantic = pydantic_model_creator(Product, name="Product")
product_pydanticIn = pydantic_model_creator(Product, name="ProductIn",
                                            exclude=("percentage_discount", "id", "main_category"))
