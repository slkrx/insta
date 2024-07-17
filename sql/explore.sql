SELECT F.username1 AS followed_by_current_user,
        unfollowed_users.*
FROM (
                SELECT *
                FROM Users
                WHERE username NOT IN (
                                SELECT username2
                                FROM following
                                WHERE username1 = %(username)s
                        )
                        AND username <> %(username)s
        ) unfollowed_users
        LEFT JOIN following F ON unfollowed_users.username = F.username2
        AND F.username1 = %(username)s