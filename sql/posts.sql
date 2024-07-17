SELECT user_post_comments_likes.*,
    L.owner AS 'liked_by_user'
FROM (
        SELECT user_post_comments.*,
            COUNT(L.postid) AS 'likes'
        FROM (
                SELECT post_comments.*,
                    '/uploads/' || U.filename AS 'owner_img_url'
                FROM (
                        SELECT P.postid,
                            P.owner,
                            '/uploads/' || P.filename AS 'img_url',
                            P.created AS 'timestamp',
                            ARRAY(C.owner, C.text, C.commentid) AS 'comments'
                        FROM posts P
                            LEFT JOIN comments C ON P.postid = C.postid
                        WHERE P.owner IN (
                                SELECT username2
                                FROM following
                                WHERE username1 = %(username) s
                            )
                            OR P.owner = %(username) s
                        GROUP BY P.postid
                    ) post_comments
                    INNER JOIN users U ON U.username = post_comments.owner
                ORDER BY post_comments.timestamp DESC,
                    post_comments.postid
            ) user_post_comments
            LEFT JOIN likes L ON L.postid = user_post_comments.postid
        GROUP BY user_post_comments.postid
    ) user_post_comments_likes
    LEFT JOIN likes L ON L.postid = user_post_comments_likes.postid
    AND L.owner = %(username) s
ORDER BY postid DESC;