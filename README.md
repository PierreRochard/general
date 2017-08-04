![General Insignia][insignia]

[logo]: https://github.com/PierreRochard/general/blob/master/general_insignia.png "General Insignia"

# General

General is a framework that integrates mature open source libraries to 
deliver modern web applications with astounding effectiveness.

General solves the repetitive problem of building CRUD interfaces
on top of a rich data model. 

General revolves around PostgreSQL, the most powerful and mature relational
database.

General is a set of API endpoints that provide configuration parameters to 
a front end application.

Configuration parameters are stored in normalized database tables.

Configuration parameters can be applied to users or groups.

Currently, configuration parameters encompass the following
front end components:
* Menubar
* Tables
* Forms

Additional components will be supported as General evolves.

Examples of configuration parameters include:
* Which tables or forms appear in the menubar and its submenus
* What icon is associated with each table or form
* Custom names for tables and forms
* Which columns or fields are visible/editable
* Which columns the user can filter on


## The stack

### SQLAlchemy

The models for General are developed as Python classes with the SQLAlchemy ORM.
SQLAlchemy is a highly flexible and mature ORM.

Your application models can use any ORM in any language, 
as long as it's compatible with PostgreSQL. 
You can also just use raw SQL scripts to develop your data model.

### Alembic

Migrations for General are performed with Alembic as it is built for 
SQLAlchemy and performs as advertised.

For changes to your application schema you can use your ORM's migration manager 
or an independent one like Flyway.

### PostgreSQL

PostgreSQL is the most reliable and feature-rich relational database. 

Both General's tables/functions as well as your application's are automatically
detected using the PostgreSQL's system catalogs. This avoids the issue of
repeating yourself, the data model is hard-coded only in one place: your ORM or SQL scripts.

### PostgREST

PostgREST is the service layer of General. It automatically generates
the REST endpoints based on the tables, views, and functions defined inside
the API schema(s). All of the relevant HTTP verbs are implemented and a
Swagger/OpenAPI specification is automatically generated as well.
This avoids the issue of repeating yourself, 
the data model is hard-coded only in one place: 
your ORM or SQL scripts. (seeing a pattern?)

### Nginx

It is recommended that you place nginx in front of PostgREST configured
as a reverse proxy.