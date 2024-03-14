SELECT s_g.Name AS Name, s_g.Surname AS Surname, s_m.Mark AS Mark, s_m.Date AS Date
FROM
(SELECT s.name AS Name, s.surname AS Surname, s.id AS id
FROM groups AS g LEFT JOIN students AS s ON g.id = s.group_id
WHERE g.name = "Group_1") AS s_g
INNER JOIN
(SELECT m.student_id AS id, m.mark AS Mark, m.set_at AS Date
FROM subjects AS sb LEFT JOIN marks AS m ON m.subject_id = sb.id
WHERE sb.title = "Math") AS s_m
ON s_g.id = s_m.id
WHERE Date = (
    SELECT MAX(s_m.Date) AS max
    FROM
    (SELECT s.id AS id
    FROM groups AS g LEFT JOIN students AS s ON g.id = s.group_id
    WHERE g.name = "Group_1") AS s_g
    INNER JOIN
    (SELECT m.student_id AS id, m.set_at AS Date
    FROM subjects AS sb LEFT JOIN marks AS m ON m.subject_id = sb.id
    WHERE sb.title = "Math") AS s_m
    ON s_g.id = s_m.id
    );