SELECT AVG(m.mark) AS avg, s.name AS Name, s.surname AS Surname 
FROM marks AS m LEFT JOIN students AS s ON s.id = m.student_id 
GROUP BY Name, Surname ORDER BY avg DESC LIMIT 5;