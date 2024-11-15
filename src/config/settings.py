# stdlib
import os

# App Description
APP_DESCRIPTION = {
    "title": "[FastAPI] User",
    "description": "Simple User Model with CRUD Operations.",
    "version": "1.0.0",
    "terms_of_service": "https://www.marsdevs.com/",
    "contact": {
        "name": "Sanam Kapoor",
        "url": "http://www.github.com/sanamkapoor1900/",
        "email": "sanamkapoor1900@gmail.com",
    },
    "license_info": {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/lincenses/LICENSE-2.0.html",
    },
    "openapi_tags": [
        {
            "name": "Defaults:",
            "description": "An uncategorised API list contains unsorted APIs with mixed functionality, no category grouping, and diverse purposes.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://www.marsdevs.com/",
            },
        },
        {
            "name": "Authentication:",
            "description": "The **login** logic is here.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
        {
            "name": "Users:",
            "description": "Operations of **User** and **Profile** Model. The **login** logic is also here.",
            "externalDocs": {
                "description": "Items external docs",
                "url": "https://fastapi.tiangolo.com/",
            },
        },
        # {
        #     "name": "Courses:",
        #     "description": "Manage items. So _fancy_ they have their own docs.",
        #     "externalDocs": {
        #         "description": "Items external docs",
        #         "url": "https://fastapi.tiangolo.com/",
        #     },
        # },
        # {
        #     "name": "Sections:",
        #     "description": "Manage items. So _fancy_ they have their own docs.",
        #     "externalDocs": {
        #         "description": "Items external docs",
        #         "url": "https://fastapi.tiangolo.com/",
        #     },
        # },
    ],
}


#
DATABASE_URL = "postgresql://postgres:root@localhost/restfulapi_assignment"
TEST_DATABASE_URL = "postgresql://postgres:root@localhost/test_restfulapi_assignment"

SECRET_KEY = "3c1f8a5b9d0e44f2af1b613b92f788aa874b219f57e9d8c76fa3d02e1c49a7c8"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30
