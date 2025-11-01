SAKILA_SCHEMA = """
==================================================
TABLES IN SAKILA DATABASE
==================================================

- actor
- actor_info
- address
- category
- city
- country
- customer
- customer_list
- customer_rental_info
- customer_rental_payment1
- events
- film
- film_actor
- film_category
- film_list
- film_text
- inventory
- language
- nicer_but_slower_film_list
- payment
- rental
- sales_by_film_category
- sales_by_store
- staff
- staff_list
- store

==================================================
TABLE COLUMNS AND THEIR PROPERTIES
==================================================

Table: actor
------------
  actor_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  first_name:
    Type: varchar(45)
    Nullable: NO
  last_name:
    Type: varchar(45)
    Nullable: NO
    Key: MUL
  last_update:
    Type: timestamp
    Nullable: NO

Table: actor_info
-----------------
  actor_id:
    Type: smallint unsigned
    Nullable: NO
  first_name:
    Type: varchar(45)
    Nullable: NO
  last_name:
    Type: varchar(45)
    Nullable: NO
  film_info:
    Type: text
    Nullable: YES

Table: address
--------------
  address_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  address:
    Type: varchar(50)
    Nullable: NO
  address2:
    Type: varchar(50)
    Nullable: YES
  district:
    Type: varchar(20)
    Nullable: NO
  city_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  postal_code:
    Type: varchar(10)
    Nullable: YES
  phone:
    Type: varchar(20)
    Nullable: NO
  location:
    Type: geometry
    Nullable: NO
    Key: MUL
  last_update:
    Type: timestamp
    Nullable: NO

Table: category
---------------
  category_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: PRI
  name:
    Type: varchar(25)
    Nullable: NO
  last_update:
    Type: timestamp
    Nullable: NO

Table: city
-----------
  city_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  city:
    Type: varchar(50)
    Nullable: NO
  country_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  last_update:
    Type: timestamp
    Nullable: NO

Table: country
--------------
  country_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  country:
    Type: varchar(50)
    Nullable: NO
  last_update:
    Type: timestamp
    Nullable: NO

Table: customer
---------------
  customer_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  store_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: MUL
  first_name:
    Type: varchar(45)
    Nullable: NO
  last_name:
    Type: varchar(45)
    Nullable: NO
    Key: MUL
  email:
    Type: varchar(50)
    Nullable: YES
  address_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  active:
    Type: tinyint(1)
    Nullable: NO
  create_date:
    Type: datetime
    Nullable: NO
  last_update:
    Type: timestamp
    Nullable: YES

Table: customer_list
--------------------
  ID:
    Type: smallint unsigned
    Nullable: NO
  name:
    Type: varchar(91)
    Nullable: YES
  address:
    Type: varchar(50)
    Nullable: NO
  zip code:
    Type: varchar(10)
    Nullable: YES
  phone:
    Type: varchar(20)
    Nullable: NO
  city:
    Type: varchar(50)
    Nullable: NO
  country:
    Type: varchar(50)
    Nullable: NO
  notes:
    Type: varchar(6)
    Nullable: NO
  SID:
    Type: tinyint unsigned
    Nullable: NO

Table: customer_rental_info
---------------------------
  customer_id:
    Type: smallint unsigned
    Nullable: NO
  first_name:
    Type: varchar(45)
    Nullable: NO
  last_name:
    Type: varchar(45)
    Nullable: NO
  email:
    Type: varchar(50)
    Nullable: YES
  rental_count:
    Type: bigint
    Nullable: NO

Table: customer_rental_payment1
-------------------------------
  customer_id:
    Type: smallint unsigned
    Nullable: NO
  first_name:
    Type: varchar(45)
    Nullable: NO
  last_name:
    Type: varchar(45)
    Nullable: NO
  email:
    Type: varchar(50)
    Nullable: YES
  rental_count:
    Type: bigint
    Nullable: NO
  total_amount_paid:
    Type: decimal(27,2)
    Nullable: YES

Table: events
-------------
  VAERS_ID:
    Type: int
    Nullable: NO
    Key: PRI
  RECVDATE:
    Type: date
    Nullable: YES
  STATE:
    Type: varchar(2)
    Nullable: YES
  AGE_YRS:
    Type: float
    Nullable: YES
  CAGE_YR:
    Type: float
    Nullable: YES
  CAGE_MO:
    Type: int
    Nullable: YES
  SEX:
    Type: char(1)
    Nullable: YES
  RPT_DATE:
    Type: date
    Nullable: YES
  SYMPTOM_TEXT:
    Type: text
    Nullable: YES
  DIED:
    Type: varchar(3)
    Nullable: YES
  CUR_ILL:
    Type: varchar(255)
    Nullable: YES
  HISTORY:
    Type: text
    Nullable: YES
  PRIOR_VAX:
    Type: varchar(3)
    Nullable: YES
  SPLTTYPE:
    Type: varchar(50)
    Nullable: YES
  FORM_VERS:
    Type: int
    Nullable: YES
  TODAYS_DATE:
    Type: date
    Nullable: YES
  BIRTH_DEFECT:
    Type: varchar(3)
    Nullable: YES
  OFC_VISIT:
    Type: varchar(3)
    Nullable: YES
  ER_ED_VISIT:
    Type: varchar(3)
    Nullable: YES
  ALLERGIES:
    Type: varchar(255)
    Nullable: YES

Table: film
-----------
  film_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  title:
    Type: varchar(128)
    Nullable: NO
    Key: MUL
  description:
    Type: text
    Nullable: YES
  release_year:
    Type: year
    Nullable: YES
  language_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: MUL
  original_language_id:
    Type: tinyint unsigned
    Nullable: YES
    Key: MUL
  rental_duration:
    Type: tinyint unsigned
    Nullable: NO
  rental_rate:
    Type: decimal(4,2)
    Nullable: NO
  length:
    Type: smallint unsigned
    Nullable: YES
  replacement_cost:
    Type: decimal(5,2)
    Nullable: NO
  rating:
    Type: enum('G','PG','PG-13','R','NC-17')
    Nullable: YES
  special_features:
    Type: set('Trailers','Commentaries','Deleted Scenes','Behind the Scenes')
    Nullable: YES
  last_update:
    Type: timestamp
    Nullable: NO

Table: film_actor
-----------------
  actor_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  film_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  last_update:
    Type: timestamp
    Nullable: NO

Table: film_category
--------------------
  film_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  category_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: PRI
  last_update:
    Type: timestamp
    Nullable: NO

Table: film_list
----------------
  FID:
    Type: smallint unsigned
    Nullable: NO
  title:
    Type: varchar(128)
    Nullable: NO
  description:
    Type: text
    Nullable: YES
  category:
    Type: varchar(25)
    Nullable: YES
  price:
    Type: decimal(4,2)
    Nullable: NO
  length:
    Type: smallint unsigned
    Nullable: YES
  rating:
    Type: enum('G','PG','PG-13','R','NC-17')
    Nullable: YES
  actors:
    Type: text
    Nullable: YES

Table: film_text
----------------
  film_id:
    Type: smallint
    Nullable: NO
    Key: PRI
  title:
    Type: varchar(255)
    Nullable: NO
    Key: MUL
  description:
    Type: text
    Nullable: YES

Table: inventory
----------------
  inventory_id:
    Type: mediumint unsigned
    Nullable: NO
    Key: PRI
  film_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  store_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: MUL
  last_update:
    Type: timestamp
    Nullable: NO

Table: language
---------------
  language_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: PRI
  name:
    Type: char(20)
    Nullable: NO
  last_update:
    Type: timestamp
    Nullable: NO

Table: nicer_but_slower_film_list
---------------------------------
  FID:
    Type: smallint unsigned
    Nullable: NO
  title:
    Type: varchar(128)
    Nullable: NO
  description:
    Type: text
    Nullable: YES
  category:
    Type: varchar(25)
    Nullable: YES
  price:
    Type: decimal(4,2)
    Nullable: NO
  length:
    Type: smallint unsigned
    Nullable: YES
  rating:
    Type: enum('G','PG','PG-13','R','NC-17')
    Nullable: YES
  actors:
    Type: text
    Nullable: YES

Table: payment
--------------
  payment_id:
    Type: smallint unsigned
    Nullable: NO
    Key: PRI
  customer_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  staff_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: MUL
  rental_id:
    Type: int
    Nullable: YES
    Key: MUL
  amount:
    Type: decimal(5,2)
    Nullable: NO
  payment_date:
    Type: datetime
    Nullable: NO
  last_update:
    Type: timestamp
    Nullable: YES

Table: rental
-------------
  rental_id:
    Type: int
    Nullable: NO
    Key: PRI
  rental_date:
    Type: datetime
    Nullable: NO
    Key: MUL
  inventory_id:
    Type: mediumint unsigned
    Nullable: NO
    Key: MUL
  customer_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  return_date:
    Type: datetime
    Nullable: YES
  staff_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: MUL
  last_update:
    Type: timestamp
    Nullable: NO

Table: sales_by_film_category
-----------------------------
  category:
    Type: varchar(25)
    Nullable: NO
  total_sales:
    Type: decimal(27,2)
    Nullable: YES

Table: sales_by_store
---------------------
  store:
    Type: varchar(101)
    Nullable: YES
  manager:
    Type: varchar(91)
    Nullable: YES
  total_sales:
    Type: decimal(27,2)
    Nullable: YES

Table: staff
------------
  staff_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: PRI
  first_name:
    Type: varchar(45)
    Nullable: NO
  last_name:
    Type: varchar(45)
    Nullable: NO
  address_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  picture:
    Type: blob
    Nullable: YES
  email:
    Type: varchar(50)
    Nullable: YES
  store_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: MUL
  active:
    Type: tinyint(1)
    Nullable: NO
  username:
    Type: varchar(16)
    Nullable: NO
  password:
    Type: varchar(40)
    Nullable: YES
  last_update:
    Type: timestamp
    Nullable: NO

Table: staff_list
-----------------
  ID:
    Type: tinyint unsigned
    Nullable: NO
  name:
    Type: varchar(91)
    Nullable: YES
  address:
    Type: varchar(50)
    Nullable: NO
  zip code:
    Type: varchar(10)
    Nullable: YES
  phone:
    Type: varchar(20)
    Nullable: NO
  city:
    Type: varchar(50)
    Nullable: NO
  country:
    Type: varchar(50)
    Nullable: NO
  SID:
    Type: tinyint unsigned
    Nullable: NO

Table: store
------------
  store_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: PRI
  manager_staff_id:
    Type: tinyint unsigned
    Nullable: NO
    Key: UNI
  address_id:
    Type: smallint unsigned
    Nullable: NO
    Key: MUL
  last_update:
    Type: timestamp
    Nullable: NO

==================================================
FOREIGN KEY RELATIONSHIPS
==================================================

- address.city_id -> city.city_id
- city.country_id -> country.country_id
- customer.address_id -> address.address_id
- customer.store_id -> store.store_id
- film.language_id -> language.language_id
- film.original_language_id -> language.language_id
- film_actor.actor_id -> actor.actor_id
- film_actor.film_id -> film.film_id
- film_category.category_id -> category.category_id
- film_category.film_id -> film.film_id
- inventory.film_id -> film.film_id
- inventory.store_id -> store.store_id
- payment.customer_id -> customer.customer_id
- payment.rental_id -> rental.rental_id
- payment.staff_id -> staff.staff_id
- rental.customer_id -> customer.customer_id
- rental.inventory_id -> inventory.inventory_id
- rental.staff_id -> staff.staff_id
- staff.address_id -> address.address_id
- staff.store_id -> store.store_id
- store.address_id -> address.address_id
- store.manager_staff_id -> staff.staff_id
"""