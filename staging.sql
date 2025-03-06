CREATE TABLE IF NOT EXISTS staging.department (
    dept_id INT PRIMARY KEY,
    dept_label VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS staging.category (
    cat_id INT PRIMARY KEY,
    cat_label VARCHAR(255) UNIQUE,
    dept_id INT REFERENCES staging.department(dept_id)
);

CREATE TABLE IF NOT EXISTS staging.subcategory (
    subcat_id INT PRIMARY KEY,
    subcat_label VARCHAR(255) UNIQUE,
    cat_id INT REFERENCES staging.category(cat_id)
);

CREATE TABLE IF NOT EXISTS staging.style (
    styl_id INT PRIMARY KEY,
    styl_label VARCHAR(255) UNIQUE,
    subcat_id INT REFERENCES staging.subcategory(subcat_id)
);

CREATE TABLE IF NOT EXISTS staging.style_color (
    stylclr_id INT PRIMARY KEY,
    stylclr_label VARCHAR(255) UNIQUE,
    styl_id INT REFERENCES staging.style(styl_id)
);

CREATE TABLE IF NOT EXISTS staging.products (
    sku_id INT PRIMARY KEY,
    sku_label VARCHAR(255),
    stylclr_id INT REFERENCES staging.style_color(stylclr_id),
    issvc BOOLEAN,
    isasmbly BOOLEAN,
    isnfs BOOLEAN
);