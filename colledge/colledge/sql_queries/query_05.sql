SELECT p.name AS Name, p.surname AS Surname, sb.title AS Subject
FROM proffessors AS p LEFT JOIN subjects AS sb ON sb.proffessor_id = p.id
WHERE Surname = "Baker";