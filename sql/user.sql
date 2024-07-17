SELECT 
    COUNT(Posts.postid) AS total_posts,
    Users.username,
    Users.fullname,
    -- %(logname)s IN (SELECT username1 FROM following WHERE username2=%(username)s) AS followed_by_current_user,
    (
        SELECT
        ARRAY_AGG(
            JSON_BUILD_OBJECT(
                'postid', postid,
                'filename', ('/uploads/' || filename))
        )
        FROM posts
        WHERE owner = %(username)s
        GROUP BY postid
        ORDER BY postid DESC
    ) AS posts,
    (
        SELECT
        COUNT(username2)
        FROM following
        WHERE username1 = %(username)s
    ) AS following,
    (
        SELECT
        COUNT(username1)
        FROM following
        WHERE username2 = %(username)s
    ) AS followers
FROM 
    posts Posts INNER JOIN users Users ON Posts.owner = Users.username
    WHERE Posts.owner = %(username)s
GROUP BY Users.username