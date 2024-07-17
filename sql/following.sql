SELECT UsersFollowed.*,
    Following.username1 AS followed_by_current_user
FROM (
        SELECT '/uploads/' || UsersFollowed.filename AS img_url,
            UsersFollowed.username
        FROM users UsersFollowed
            INNER JOIN following Following ON Following.username2 = UsersFollowed.username
        WHERE Following.username1 = %(username)s
    ) UsersFollowed
    LEFT JOIN following Following ON Following.username2 = UsersFollowed.username
    AND Following.username1 = %(logname)s