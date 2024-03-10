SELECT g.name AS Team, sb.title AS Subject, AVG(m.mark) AS avg 
FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
LEFT JOIN students AS s ON m.student_id = s.id
LEFT JOIN groups as g ON s.group_id = g.id
GROUP BY Subject, Team
HAVING Subject=(?)
ORDER BY Team ;