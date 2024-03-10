SELECT p_m.Surname AS Proffessor, s_m.Surname AS Student, AVG(s_m.Mark) AS avg
FROM
(SELECT p.surname AS Surname, m.id AS id
FROM marks AS m LEFT JOIN proffessors AS p ON m.proffessor_id = p.id
WHERE Surname = (?)) AS p_m
INNER JOIN
(SELECT s.surname AS Surname, m.mark AS Mark, m.id AS id
FROM marks AS m LEFT JOIN students AS s ON m.student_id = s.id
WHERE Surname = (?)) AS s_m
ON p_m.id = s_m.id
GROUP BY Student, Proffessor;