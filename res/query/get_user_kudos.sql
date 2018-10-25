SELECT server_id, user_id, kudos, DENSE_RANK() OVER(ORDER BY kudos DESC)
FROM users WHERE server_id=%s ORDER BY kudos DESC;
