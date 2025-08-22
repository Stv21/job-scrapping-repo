CREATE TABLE job_listings (
    id SERIAL PRIMARY KEY,
    job_title VARCHAR(255),
    company_name VARCHAR(255),
    location VARCHAR(255),
    job_url VARCHAR(512) UNIQUE,
    salary_info TEXT,
    job_description TEXT,
    source_site VARCHAR(100),
    scraped_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);