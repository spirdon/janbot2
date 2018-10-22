CREATE TABLE IF NOT EXISTS servers(
    server_id VARCHAR(255),
    prefix VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS channels(
    channel_id VARCHAR(255),
    is_anonymous BOOLEAN
);
