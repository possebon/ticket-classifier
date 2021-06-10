-- Database OTRS version 5.0

-- Service / Category
-- +-------------+--------------+------+-----+---------+----------------+
-- | Field       | Type         | Null | Key | Default | Extra          |
-- +-------------+--------------+------+-----+---------+----------------+
-- | id          | int(11)      | NO   | PRI | NULL    | auto_increment |
-- | name        | varchar(200) | NO   | UNI | NULL    |                |
-- | valid_id    | smallint(6)  | NO   |     | NULL    |                |
-- | comments    | varchar(250) | YES  |     | NULL    |                |
-- | create_time | datetime     | NO   |     | NULL    |                |
-- | create_by   | int(11)      | NO   | MUL | NULL    |                |
-- | change_time | datetime     | NO   |     | NULL    |                |
-- | change_by   | int(11)      | NO   | MUL | NULL    |                |
-- | type_id     | int(11)      | YES  |     | NULL    |                |
-- | criticality | varchar(200) | YES  |     | NULL    |                |
-- +-------------+--------------+------+-----+---------+----------------+


SELECT id, name FROM service

-- Ticket
-- +--------------------------+--------------+------+-----+---------+----------------+
-- | Field                    | Type         | Null | Key | Default | Extra          |
-- +--------------------------+--------------+------+-----+---------+----------------+
-- | id                       | bigint(20)   | NO   | PRI | NULL    | auto_increment |
-- | tn                       | varchar(50)  | NO   | UNI | NULL    |                |
-- | title                    | varchar(255) | YES  | MUL | NULL    |                |
-- | queue_id                 | int(11)      | NO   | MUL | NULL    |                |
-- | ticket_lock_id           | smallint(6)  | NO   | MUL | NULL    |                |
-- | type_id                  | smallint(6)  | YES  | MUL | NULL    |                |
-- | service_id               | int(11)      | YES  | MUL | NULL    |                |
-- | sla_id                   | int(11)      | YES  | MUL | NULL    |                |
-- | user_id                  | int(11)      | NO   | MUL | NULL    |                |
-- | responsible_user_id      | int(11)      | NO   | MUL | NULL    |                |
-- | ticket_priority_id       | smallint(6)  | NO   | MUL | NULL    |                |
-- | ticket_state_id          | smallint(6)  | NO   | MUL | NULL    |                |
-- | customer_id              | varchar(150) | YES  | MUL | NULL    |                |
-- | customer_user_id         | varchar(250) | YES  | MUL | NULL    |                |
-- | timeout                  | int(11)      | NO   | MUL | NULL    |                |
-- | until_time               | int(11)      | NO   | MUL | NULL    |                |
-- | escalation_time          | int(11)      | NO   | MUL | NULL    |                |
-- | escalation_update_time   | int(11)      | NO   | MUL | NULL    |                |
-- | escalation_response_time | int(11)      | NO   | MUL | NULL    |                |
-- | escalation_solution_time | int(11)      | NO   | MUL | NULL    |                |
-- | archive_flag             | smallint(6)  | NO   | MUL | 0       |                |
-- | create_time_unix         | bigint(20)   | NO   | MUL | NULL    |                |
-- | create_time              | datetime     | NO   | MUL | NULL    |                |
-- | create_by                | int(11)      | NO   | MUL | NULL    |                |
-- | change_time              | datetime     | NO   |     | NULL    |                |
-- | change_by                | int(11)      | NO   | MUL | NULL    |                |
-- +--------------------------+--------------+------+-----+---------+----------------+


SELECT id, tn, title, service_id FROM ticket

-- Article
-- +------------------------+--------------+------+-----+---------+----------------+
-- | Field                  | Type         | Null | Key | Default | Extra          |
-- +------------------------+--------------+------+-----+---------+----------------+
-- | id                     | bigint(20)   | NO   | PRI | NULL    | auto_increment |
-- | ticket_id              | bigint(20)   | NO   | MUL | NULL    |                |
-- | article_type_id        | smallint(6)  | NO   | MUL | NULL    |                |
-- | article_sender_type_id | smallint(6)  | NO   | MUL | NULL    |                |
-- | a_from                 | text         | YES  |     | NULL    |                |
-- | a_reply_to             | text         | YES  |     | NULL    |                |
-- | a_to                   | text         | YES  |     | NULL    |                |
-- | a_cc                   | text         | YES  |     | NULL    |                |
-- | a_subject              | text         | YES  |     | NULL    |                |
-- | a_message_id           | text         | YES  |     | NULL    |                |
-- | a_message_id_md5       | varchar(32)  | YES  | MUL | NULL    |                |
-- | a_in_reply_to          | text         | YES  |     | NULL    |                |
-- | a_references           | text         | YES  |     | NULL    |                |
-- | a_content_type         | varchar(250) | YES  |     | NULL    |                |
-- | a_body                 | mediumtext   | NO   |     | NULL    |                |
-- | incoming_time          | int(11)      | NO   |     | NULL    |                |
-- | content_path           | varchar(250) | YES  |     | NULL    |                |
-- | valid_id               | smallint(6)  | NO   | MUL | NULL    |                |
-- | create_time            | datetime     | NO   |     | NULL    |                |
-- | create_by              | int(11)      | NO   | MUL | NULL    |                |
-- | change_time            | datetime     | NO   |     | NULL    |                |
-- | change_by              | int(11)      | NO   | MUL | NULL    |                |
-- +------------------------+--------------+------+-----+---------+----------------+
SELECT
    a.ticket_id as ticket_id,
	MIN(a.id) as article_id,
	a.a_subject as article_subject,
	a.a_body as article_body,
	t.title as tickect_title,
	t.tn as ticket_number,
	t.service_id as service_id,
	s.name as service_name
FROM
	article a
	JOIN ticket t ON a.ticket_id = t.id
	LEFT JOIN service s ON t.service_id = s.id
GROUP BY
	a.ticket_id