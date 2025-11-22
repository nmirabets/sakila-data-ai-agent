-- Sakila Sample Database Schema - PostgreSQL Version
-- Converted from MySQL to PostgreSQL for Supabase deployment
-- Version 1.5

-- Create database (Supabase will handle this)
-- Note: Supabase automatically creates a database, so we'll work within it

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop schema if exists (for clean deployment)
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public;

--
-- Table structure for table actor
--

CREATE TABLE actor (
  actor_id SERIAL PRIMARY KEY,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_actor_last_name ON actor (last_name);

--
-- Table structure for table country
--

CREATE TABLE country (
  country_id SERIAL PRIMARY KEY,
  country VARCHAR(50) NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--
-- Table structure for table city
--

CREATE TABLE city (
  city_id SERIAL PRIMARY KEY,
  city VARCHAR(50) NOT NULL,
  country_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_city_fk_country_id ON city (country_id);

--
-- Table structure for table address
--

CREATE TABLE address (
  address_id SERIAL PRIMARY KEY,
  address VARCHAR(50) NOT NULL,
  address2 VARCHAR(50) DEFAULT NULL,
  district VARCHAR(20) NOT NULL,
  city_id SMALLINT NOT NULL,
  postal_code VARCHAR(10) DEFAULT NULL,
  phone VARCHAR(20) NOT NULL,
  -- PostgreSQL uses POINT type for location data instead of GEOMETRY
  location POINT DEFAULT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_address_city FOREIGN KEY (city_id) REFERENCES city (city_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_address_fk_city_id ON address (city_id);

--
-- Table structure for table category
--

CREATE TABLE category (
  category_id SERIAL PRIMARY KEY,
  name VARCHAR(25) NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--
-- Table structure for table language
--

CREATE TABLE language (
  language_id SERIAL PRIMARY KEY,
  name CHAR(20) NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

--
-- Table structure for table film
--

CREATE TABLE film (
  film_id SERIAL PRIMARY KEY,
  title VARCHAR(128) NOT NULL,
  description TEXT DEFAULT NULL,
  release_year INTEGER DEFAULT NULL,
  language_id SMALLINT NOT NULL,
  original_language_id SMALLINT DEFAULT NULL,
  rental_duration SMALLINT NOT NULL DEFAULT 3,
  rental_rate DECIMAL(4,2) NOT NULL DEFAULT 4.99,
  length SMALLINT DEFAULT NULL,
  replacement_cost DECIMAL(5,2) NOT NULL DEFAULT 19.99,
  rating VARCHAR(10) DEFAULT 'G' CHECK (rating IN ('G','PG','PG-13','R','NC-17')),
  special_features TEXT[] DEFAULT NULL, -- PostgreSQL array instead of SET
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_film_language FOREIGN KEY (language_id) REFERENCES language (language_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_film_language_original FOREIGN KEY (original_language_id) REFERENCES language (language_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_title ON film (title);
CREATE INDEX idx_film_fk_language_id ON film (language_id);
CREATE INDEX idx_film_fk_original_language_id ON film (original_language_id);

--
-- Table structure for table film_actor
--

CREATE TABLE film_actor (
  actor_id SMALLINT NOT NULL,
  film_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (actor_id, film_id),
  CONSTRAINT fk_film_actor_actor FOREIGN KEY (actor_id) REFERENCES actor (actor_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_film_actor_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_film_actor_fk_film_id ON film_actor (film_id);

--
-- Table structure for table film_category
--

CREATE TABLE film_category (
  film_id SMALLINT NOT NULL,
  category_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (film_id, category_id),
  CONSTRAINT fk_film_category_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_film_category_category FOREIGN KEY (category_id) REFERENCES category (category_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

--
-- Table structure for table film_text
-- PostgreSQL has built-in full-text search capabilities
--

CREATE TABLE film_text (
  film_id SMALLINT NOT NULL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  -- PostgreSQL full-text search vector
  title_description_vector tsvector
);

-- Create full-text search index
CREATE INDEX idx_title_description_fts ON film_text USING gin(title_description_vector);

--
-- Table structure for table store
--

CREATE TABLE store (
  store_id SERIAL PRIMARY KEY,
  manager_staff_id SMALLINT NOT NULL,
  address_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX idx_unique_manager ON store (manager_staff_id);
CREATE INDEX idx_store_fk_address_id ON store (address_id);

--
-- Table structure for table staff
--

CREATE TABLE staff (
  staff_id SERIAL PRIMARY KEY,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  address_id SMALLINT NOT NULL,
  picture BYTEA DEFAULT NULL,
  email VARCHAR(50) DEFAULT NULL,
  store_id SMALLINT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  username VARCHAR(16) NOT NULL,
  password VARCHAR(40) DEFAULT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_staff_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_staff_address FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_staff_fk_store_id ON staff (store_id);
CREATE INDEX idx_staff_fk_address_id ON staff (address_id);

-- Add foreign key constraint to store table (circular reference handled)
ALTER TABLE store ADD CONSTRAINT fk_store_staff FOREIGN KEY (manager_staff_id) REFERENCES staff (staff_id) ON DELETE RESTRICT ON UPDATE CASCADE;
ALTER TABLE store ADD CONSTRAINT fk_store_address FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Table structure for table customer
--

CREATE TABLE customer (
  customer_id SERIAL PRIMARY KEY,
  store_id SMALLINT NOT NULL,
  first_name VARCHAR(45) NOT NULL,
  last_name VARCHAR(45) NOT NULL,
  email VARCHAR(50) DEFAULT NULL,
  address_id SMALLINT NOT NULL,
  active BOOLEAN NOT NULL DEFAULT TRUE,
  create_date TIMESTAMP NOT NULL,
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_customer_address FOREIGN KEY (address_id) REFERENCES address (address_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_customer_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_customer_fk_store_id ON customer (store_id);
CREATE INDEX idx_customer_fk_address_id ON customer (address_id);
CREATE INDEX idx_last_name ON customer (last_name);

--
-- Table structure for table inventory
--

CREATE TABLE inventory (
  inventory_id SERIAL PRIMARY KEY,
  film_id SMALLINT NOT NULL,
  store_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_inventory_store FOREIGN KEY (store_id) REFERENCES store (store_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_inventory_film FOREIGN KEY (film_id) REFERENCES film (film_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_inventory_fk_film_id ON inventory (film_id);
CREATE INDEX idx_store_id_film_id ON inventory (store_id, film_id);

--
-- Table structure for table rental
--

CREATE TABLE rental (
  rental_id SERIAL PRIMARY KEY,
  rental_date TIMESTAMP NOT NULL,
  inventory_id INTEGER NOT NULL,
  customer_id SMALLINT NOT NULL,
  return_date TIMESTAMP DEFAULT NULL,
  staff_id SMALLINT NOT NULL,
  last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_rental_staff FOREIGN KEY (staff_id) REFERENCES staff (staff_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_rental_inventory FOREIGN KEY (inventory_id) REFERENCES inventory (inventory_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_rental_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE UNIQUE INDEX idx_rental_unique ON rental (rental_date, inventory_id, customer_id);
CREATE INDEX idx_rental_fk_inventory_id ON rental (inventory_id);
CREATE INDEX idx_rental_fk_customer_id ON rental (customer_id);
CREATE INDEX idx_rental_fk_staff_id ON rental (staff_id);

--
-- Table structure for table payment
--

CREATE TABLE payment (
  payment_id SERIAL PRIMARY KEY,
  customer_id SMALLINT NOT NULL,
  staff_id SMALLINT NOT NULL,
  rental_id INTEGER DEFAULT NULL,
  amount DECIMAL(5,2) NOT NULL,
  payment_date TIMESTAMP NOT NULL,
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_payment_rental FOREIGN KEY (rental_id) REFERENCES rental (rental_id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_payment_customer FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_payment_staff FOREIGN KEY (staff_id) REFERENCES staff (staff_id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_payment_fk_staff_id ON payment (staff_id);
CREATE INDEX idx_payment_fk_customer_id ON payment (customer_id);

--
-- Triggers for film_text table (PostgreSQL syntax)
--

-- Function to update film_text when film is inserted
CREATE OR REPLACE FUNCTION update_film_text_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO film_text (film_id, title, description, title_description_vector)
    VALUES (NEW.film_id, NEW.title, NEW.description, 
            to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, '')));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to update film_text when film is updated
CREATE OR REPLACE FUNCTION update_film_text_update() RETURNS TRIGGER AS $$
BEGIN
    IF (OLD.title != NEW.title) OR (OLD.description != NEW.description) OR (OLD.film_id != NEW.film_id) THEN
        UPDATE film_text
        SET title = NEW.title,
            description = NEW.description,
            film_id = NEW.film_id,
            title_description_vector = to_tsvector('english', COALESCE(NEW.title, '') || ' ' || COALESCE(NEW.description, ''))
        WHERE film_id = OLD.film_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to delete from film_text when film is deleted
CREATE OR REPLACE FUNCTION update_film_text_delete() RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM film_text WHERE film_id = OLD.film_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER ins_film 
    AFTER INSERT ON film 
    FOR EACH ROW 
    EXECUTE FUNCTION update_film_text_insert();

CREATE TRIGGER upd_film 
    AFTER UPDATE ON film 
    FOR EACH ROW 
    EXECUTE FUNCTION update_film_text_update();

CREATE TRIGGER del_film 
    AFTER DELETE ON film 
    FOR EACH ROW 
    EXECUTE FUNCTION update_film_text_delete();

--
-- Function to update last_update timestamp
--

CREATE OR REPLACE FUNCTION update_last_update_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_update = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for automatic timestamp updates
CREATE TRIGGER update_actor_last_update BEFORE UPDATE ON actor FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_address_last_update BEFORE UPDATE ON address FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_category_last_update BEFORE UPDATE ON category FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_city_last_update BEFORE UPDATE ON city FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_country_last_update BEFORE UPDATE ON country FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_customer_last_update BEFORE UPDATE ON customer FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_film_last_update BEFORE UPDATE ON film FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_film_actor_last_update BEFORE UPDATE ON film_actor FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_film_category_last_update BEFORE UPDATE ON film_category FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_inventory_last_update BEFORE UPDATE ON inventory FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_language_last_update BEFORE UPDATE ON language FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_payment_last_update BEFORE UPDATE ON payment FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_rental_last_update BEFORE UPDATE ON rental FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_staff_last_update BEFORE UPDATE ON staff FOR EACH ROW EXECUTE FUNCTION update_last_update_column();
CREATE TRIGGER update_store_last_update BEFORE UPDATE ON store FOR EACH ROW EXECUTE FUNCTION update_last_update_column();

--
-- Views
--

-- customer_list view
CREATE VIEW customer_list AS
SELECT 
    cu.customer_id AS id, 
    CONCAT(cu.first_name, ' ', cu.last_name) AS name, 
    a.address AS address, 
    a.postal_code AS "zip code",
    a.phone AS phone, 
    city.city AS city, 
    country.country AS country, 
    CASE WHEN cu.active THEN 'active' ELSE '' END AS notes, 
    cu.store_id AS sid
FROM customer AS cu 
JOIN address AS a ON cu.address_id = a.address_id 
JOIN city ON a.city_id = city.city_id
JOIN country ON city.country_id = country.country_id;

-- film_list view
CREATE VIEW film_list AS
SELECT 
    film.film_id AS fid, 
    film.title AS title, 
    film.description AS description, 
    category.name AS category, 
    film.rental_rate AS price,
    film.length AS length, 
    film.rating AS rating, 
    STRING_AGG(CONCAT(actor.first_name, ' ', actor.last_name), ', ') AS actors
FROM film 
LEFT JOIN film_category ON film_category.film_id = film.film_id
LEFT JOIN category ON category.category_id = film_category.category_id 
LEFT JOIN film_actor ON film.film_id = film_actor.film_id 
LEFT JOIN actor ON film_actor.actor_id = actor.actor_id
GROUP BY film.film_id, category.name, film.title, film.description, film.rental_rate, film.length, film.rating;

-- staff_list view
CREATE VIEW staff_list AS
SELECT 
    s.staff_id AS id, 
    CONCAT(s.first_name, ' ', s.last_name) AS name, 
    a.address AS address, 
    a.postal_code AS "zip code", 
    a.phone AS phone,
    city.city AS city, 
    country.country AS country, 
    s.store_id AS sid
FROM staff AS s 
JOIN address AS a ON s.address_id = a.address_id 
JOIN city ON a.city_id = city.city_id
JOIN country ON city.country_id = country.country_id;

-- sales_by_store view
CREATE VIEW sales_by_store AS
SELECT
    CONCAT(c.city, ',', cy.country) AS store,
    CONCAT(m.first_name, ' ', m.last_name) AS manager,
    SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN store AS s ON i.store_id = s.store_id
INNER JOIN address AS a ON s.address_id = a.address_id
INNER JOIN city AS c ON a.city_id = c.city_id
INNER JOIN country AS cy ON c.country_id = cy.country_id
INNER JOIN staff AS m ON s.manager_staff_id = m.staff_id
GROUP BY s.store_id, c.city, cy.country, m.first_name, m.last_name
ORDER BY cy.country, c.city;

-- sales_by_film_category view
CREATE VIEW sales_by_film_category AS
SELECT
    c.name AS category,
    SUM(p.amount) AS total_sales
FROM payment AS p
INNER JOIN rental AS r ON p.rental_id = r.rental_id
INNER JOIN inventory AS i ON r.inventory_id = i.inventory_id
INNER JOIN film AS f ON i.film_id = f.film_id
INNER JOIN film_category AS fc ON f.film_id = fc.film_id
INNER JOIN category AS c ON fc.category_id = c.category_id
GROUP BY c.name
ORDER BY total_sales DESC;

--
-- PostgreSQL Functions (converted from MySQL)
--

-- Function to check if inventory is in stock
CREATE OR REPLACE FUNCTION inventory_in_stock(p_inventory_id INTEGER) 
RETURNS BOOLEAN AS $$
DECLARE
    v_rentals INTEGER;
    v_out INTEGER;
BEGIN
    -- An item is in-stock if there are either no rows in the rental table
    -- for the item or all rows have return_date populated
    
    SELECT COUNT(*) INTO v_rentals
    FROM rental
    WHERE inventory_id = p_inventory_id;
    
    IF v_rentals = 0 THEN
        RETURN TRUE;
    END IF;
    
    SELECT COUNT(rental_id) INTO v_out
    FROM inventory 
    LEFT JOIN rental USING(inventory_id)
    WHERE inventory.inventory_id = p_inventory_id
    AND rental.return_date IS NULL;
    
    IF v_out > 0 THEN
        RETURN FALSE;
    ELSE
        RETURN TRUE;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Function to get customer who has inventory
CREATE OR REPLACE FUNCTION inventory_held_by_customer(p_inventory_id INTEGER) 
RETURNS INTEGER AS $$
DECLARE
    v_customer_id INTEGER;
BEGIN
    SELECT customer_id INTO v_customer_id
    FROM rental
    WHERE return_date IS NULL
    AND inventory_id = p_inventory_id;
    
    RETURN v_customer_id;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Function to get customer balance
CREATE OR REPLACE FUNCTION get_customer_balance(p_customer_id INTEGER, p_effective_date TIMESTAMP) 
RETURNS DECIMAL(5,2) AS $$
DECLARE
    v_rentfees DECIMAL(5,2);
    v_overfees INTEGER;
    v_payments DECIMAL(5,2);
BEGIN
    -- Calculate rental fees
    SELECT COALESCE(SUM(film.rental_rate), 0) INTO v_rentfees
    FROM film, inventory, rental
    WHERE film.film_id = inventory.film_id
      AND inventory.inventory_id = rental.inventory_id
      AND rental.rental_date <= p_effective_date
      AND rental.customer_id = p_customer_id;
    
    -- Calculate late fees
    SELECT COALESCE(SUM(
        CASE WHEN (EXTRACT(DAY FROM rental.return_date) - EXTRACT(DAY FROM rental.rental_date)) > film.rental_duration
        THEN ((EXTRACT(DAY FROM rental.return_date) - EXTRACT(DAY FROM rental.rental_date)) - film.rental_duration)
        ELSE 0 END), 0) INTO v_overfees
    FROM rental, inventory, film
    WHERE film.film_id = inventory.film_id
      AND inventory.inventory_id = rental.inventory_id
      AND rental.rental_date <= p_effective_date
      AND rental.customer_id = p_customer_id;
    
    -- Calculate payments
    SELECT COALESCE(SUM(payment.amount), 0) INTO v_payments
    FROM payment
    WHERE payment.payment_date <= p_effective_date
    AND payment.customer_id = p_customer_id;
    
    RETURN v_rentfees + v_overfees - v_payments;
END;
$$ LANGUAGE plpgsql;

-- Note: Complex procedures like rewards_report, film_in_stock, and film_not_in_stock
-- would need significant adaptation for PostgreSQL and may require breaking into
-- multiple functions or using different approaches.
-- For a basic deployment, the above schema provides the core functionality.

-- Grant permissions (adjust as needed for Supabase)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO authenticated;
