SELECT p.name AS Name, p.surname AS Surname, sb.title AS Subject, AVG(m.mark) AS avg
FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
LEFT JOIN proffessors AS p ON sb.proffessor_id = p.id
GROUP BY Name, Surname, Subject
HAVING Surname = "Martin";