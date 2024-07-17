SELECT Followers.*,
    Following.username1 AS followed_by_current_user
FROM (
        SELECT '/uploads/' || Followers.filename AS img_url,
            Followers.username
        FROM users Followers
            INNER JOIN following Following ON Following.username1 = Followers.username
        WHERE Following.username2 = %(username)s
    ) Followers
    LEFT JOIN following Following ON Following.username2 = Followers.username
    AND Following.username1 = %(logname)s