SELECT s.name AS Name, s.surname AS Surname, sb.title AS Subject
FROM marks AS m LEFT JOIN students AS s ON m.student_id = s.id
LEFT JOIN subjects AS sb ON m.subject_id = sb.id
GROUP BY Name, Surname, Subject
HAVING Surname = (?);