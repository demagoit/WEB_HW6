SELECT g.name AS Team, s.name AS Name, s.surname as Surname
FROM students AS s LEFT JOIN groups AS g ON s.group_id = g.id
WHERE Team = "Group_1";