CREATE TABLE IF NOT EXISTS guilds (
	guild_id integer PRIMARY KEY,
	prefix text DEFAULT ".",
	log_channel integer
);

CREATE TABLE IF NOT EXISTS users (
    discord_user_id integer PRIMARY KEY
);
