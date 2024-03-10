SELECT g.name AS Team, sb.title AS Subject, m.mark AS Mark, s.name AS Name, s.surname AS Surname
FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
LEFT JOIN students AS s ON m.student_id = s.id
LEFT JOIN groups AS g ON s.group_id = g.id
WHERE Team = (?) AND Subject = (?);