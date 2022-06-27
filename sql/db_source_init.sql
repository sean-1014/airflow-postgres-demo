CREATE TABLE IF NOT EXISTS sales (
  id SERIAL PRIMARY KEY,
  creation_date DATE,
  sale_value NUMERIC(10,2)
);

INSERT INTO sales(creation_date, sale_value)
VALUES ('2022-06-15', 1234.56),
       ('2022-06-16', 9876.54);