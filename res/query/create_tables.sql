CREATE TABLE IF NOT EXISTS servers(
    server_id VARCHAR(255),
    prefix VARCHAR(255),
    cooldown INTEGER
);

CREATE TABLE IF NOT EXISTS channels(
    channel_id VARCHAR(255),
    is_anonymous BOOLEAN,
    is_ranked BOOLEAN,
    has_roulette BOOLEAN
);

CREATE TABLE IF NOT EXISTS users(
    server_id VARCHAR(255),
    user_id VARCHAR(255),
    exp INTEGER,
    lvl INTEGER,
    kudos INTEGER,
    cooldown_end INTEGER
);

CREATE TABLE IF NOT EXISTS roles(
    server_id VARCHAR(255),
    channel_id VARCHAR(255),
    role_name VARCHAR(255),
    owner_id VARCHAR(255),
    role_time INTEGER,
    time_end INTEGER,
    stexts_url VARCHAR(255),
    texts_url VARCHAR(255),
    etexts_url VARCHAR(255)
);
