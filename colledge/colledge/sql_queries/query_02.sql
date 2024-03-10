SELECT sb.title AS Subject, AVG(m.mark) as avg, s.name AS Name, s.surname AS Surname 
FROM marks AS m LEFT JOIN students AS s ON m.student_id = s.id 
LEFT JOIN subjects AS sb ON sb.id = m.subject_id
GROUP BY Name, Surname, Subject 
HAVING Subject=(?)
ORDER BY avg DESC LIMIT 1;