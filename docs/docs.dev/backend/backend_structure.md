# Backend Structure

## Overview
Explanation about the backend file structure/organization

## Description
Our backend file structure is completely in the 'backend' directory
```
.
└── backend/
    ├── logs/
    │   └── logs of backend
    ├── migrations/
    │   └── migrate database model to real tables using alembic
    └── src/
        ├── app/
        │   ├── database/
        │   │   ├── data_base_access/
        │   │   │   └── access methods to access information from the databse
        │   │   ├── models/
        │   │   │   └── database models
        │   │   └── exceptions/
        │   │       └── database access exceptions
        │   ├── fill_db/
        │   │   └── setting up database (Adding resource types, ...)
        │   └── routers/
        │       └── routers/endpoints to access backend
        ├── logic/
        │   ├── combat/
        │   │   └── handling of army combat
        │   ├── formula/
        │   │   └── calcualting formula used in calculations
        │   └── name_generator/
        │       └── name_generator for random planet name
        └── tests/
            └── backend_testcases
```