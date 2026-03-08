-- Dimension: dim_time
CREATE TABLE dim_time (
    time_id SERIAL PRIMARY KEY,
    listened_at TIMESTAMP,
    hour INT,
    day INT,
    week INT,
    month INT,
    year INT,
    weekday VARCHAR(10)
);

-- Dimension: dim_artist
CREATE TABLE dim_artist (
    artist_id VARCHAR(50) PRIMARY KEY,
    artist_name VARCHAR(200),
    artist_popularity INT,
    artist_genres TEXT[]
);

-- Dimension: dim_album
CREATE TABLE dim_album (
    album_id VARCHAR(50) PRIMARY KEY,
    album_name VARCHAR(200),
    album_release_date DATE,
    album_total_tracks INT,
    album_popularity INT
);

-- Dimension: dim_track
CREATE TABLE dim_track (
    track_id VARCHAR(50) PRIMARY KEY,
    track_name VARCHAR(200),
    track_popularity INT,
    duration_ms INT,
    explicit BOOLEAN,
    artist_id VARCHAR(50) REFERENCES dim_artist(artist_id),
    album_id VARCHAR(50) REFERENCES dim_album(album_id)
);

-- Fact: fact_listens
CREATE TABLE fact_listens (
    listen_id SERIAL PRIMARY KEY,
    track_id VARCHAR(50) REFERENCES dim_track(track_id),
    time_id INT REFERENCES dim_time(time_id),
    played_at TIMESTAMP,
    context VARCHAR(50)  -- misal: 'playlist', 'album', 'library'
);