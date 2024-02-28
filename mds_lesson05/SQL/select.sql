SELECT id, name as fullname
FROM contacts as c
WHERE favorite != TRUE 
ORDER BY fullname
LIMIT 100
OFFSET 0;

SELECT name, email, age
FROM users u
WHERE age IN (20, 30, 40);

SELECT name, email, age
FROM users u
WHERE age NOT BETWEEN 24 AND 40;

SELECT name, email, age
FROM users u
WHERE age >= 24 AND age <= 40;

SELECT name, email, age
FROM users u
WHERE name LIKE "%s";

SELECT COUNT(user_id) as total, user_id
FROM contacts c
GROUP BY user_id;

SELECT *
FROM contacts c 
WHERE user_id IN (
	SELECT id 
	FROM users u 
	WHERE age <=35
);

SELECT c.name, c.email, c.phone, u.name as user_name, u.email as user_email 
FROM contacts c 
JOIN users u ON u.id = c.user_id;

SELECT c.name, c.email, c.phone, u.name as user_name, u.email as user_email 
FROM contacts c 
LEFT JOIN users u ON u.id = c.user_id;

UPDATE contacts SET user_id = 3 WHERE id = 5;

CREATE INDEX idx_name ON contacts (name);
