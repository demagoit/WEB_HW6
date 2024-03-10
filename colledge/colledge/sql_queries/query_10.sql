SELECT s.surname AS Student, p.surname AS Proffessor, sb.title AS Subject
FROM marks AS m LEFT JOIN subjects AS sb ON m.subject_id = sb.id
LEFT JOIN students AS s ON m.student_id = s.id
LEFT JOIN proffessors AS p ON sb.proffessor_id = p.id
GROUP BY Student, Proffessor, Subject
HAVING Student = (?) AND Proffessor = (?);