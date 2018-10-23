SELECT server_id, user_id, exp, lvl, DENSE_RANK() OVER(ORDER BY exp DESC)
FROM users WHERE server_id=%s;
