CREATE TABLE IF NOT EXISTS Users (
    username VARCHAR(255) PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255),
    password_hashed VARCHAR(255),
    time_created TIMESTAMP,
    bio TEXT,
    email varchar(255),
    is_logged_in bool DEFAULT false,
    img_link VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Genre (
    genre_id INT PRIMARY KEY auto_increment,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Eras (
    era_id INT PRIMARY KEY auto_increment,
    name VARCHAR(100) NOT NULL,
    parent_era_id INT,
    era_range varchar(255),
    era_description varchar(1000),
    
    CONSTRAINT fk_parenteraid_eras FOREIGN KEY (parent_era_id) REFERENCES Eras(era_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Media (
    media_id INT PRIMARY KEY auto_increment,
    mediatype VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    img_link TEXT,
    ext_link TEXT,
    release_date DATE,
    age_rating VARCHAR(20),
    rating Decimal(2,1) ,
    description TEXT,
    era_id INT,
    CONSTRAINT check_rating_media CHECK (rating between 0 and 10),
    CONSTRAINT check_agerating_media CHECK (age_rating IN(
            'G', 'PG', 'PG-13', 'R', 'NC-17',
            'TV-Y', 'TV-Y7', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA',
            '13+', '16+', '18+', 'Unrated')),
    CONSTRAINT fk_eraid_media FOREIGN KEY (era_id) REFERENCES Eras(era_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT check_mediatype_media  CHECK (mediatype IN ('movies', 'series', 'books', 'games', 'cartoons', 'anime'))
);

CREATE TABLE IF NOT EXISTS Media_Genre (
    media_id INT,
    genre_id INT,
    PRIMARY KEY (media_id, genre_id),
    CONSTRAINT fk_mediaid_mediagenre FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_genreid_mediagenre FOREIGN KEY (genre_id) REFERENCES Genre(genre_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Series (
    media_id INT PRIMARY KEY,
    end_date DATE,
    episodes INT,
    seasons INT,
    CONSTRAINT fk_seriesid_series FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movies (
    media_id INT PRIMARY KEY,
    trailer_url TEXT,
    runtime_hours INT,
    oscar_winner BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT fk_movieid_movies FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Cartoons (
    media_id INT PRIMARY KEY,
    animation_style VARCHAR(100),
    languages TEXT,
    episodes INT,
    end_date DATE,
    CONSTRAINT fk_cartoonid_cartoons FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Anime (
    media_id INT PRIMARY KEY,
    type VARCHAR(100),
    episodes INT,
    seasons INT,
    end_date DATE,
    CONSTRAINT fk_animeid_anime FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Books (
    media_id INT PRIMARY KEY,
    ISBN VARCHAR(20) UNIQUE NOT NULL,
    page_count INT,
    CONSTRAINT fk_bookid_books FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Games (
    media_id INT PRIMARY KEY,
    perspective VARCHAR(100),
    playtime_hours INT,
    player_support VARCHAR(100),
    local_online VARCHAR(100),
    CONSTRAINT fk_gameid_games FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Developer (
    developer_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255),
    founded_year INT,
    status VARCHAR(50),
    CONSTRAINT check_status CHECK (status IN ('Active', 'Inactive'))
);

CREATE TABLE IF NOT EXISTS Author (
    author_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255),
    birthdate DATE,
    sex VARCHAR(20),
    CONSTRAINT check_sex_author CHECK (sex IN ('Male', 'Female', 'Intersex'))
);

CREATE TABLE IF NOT EXISTS Producer (
    producer_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255),
    birthdate DATE,
    sex VARCHAR(20),
    CONSTRAINT check_sex_producer CHECK (sex IN ('Male', 'Female', 'Intersex'))
);

CREATE TABLE IF NOT EXISTS Director (
    director_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255),
    birthdate DATE,
    sex VARCHAR(20),
    CONSTRAINT check_sex_director CHECK (sex IN ('Male', 'Female', 'Intersex'))
);

CREATE TABLE IF NOT EXISTS A_Studio (
    anime_studio_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255),
    founded_year INT,
    status VARCHAR(50),
    CONSTRAINT check_status_astudio CHECK (status IN ('Active', 'Inactive'))
);

CREATE TABLE IF NOT EXISTS C_Studio (
    cartoon_studio_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255),
    founded_year INT,
    status VARCHAR(50),
    CONSTRAINT check_status_cstudio CHECK (status IN ('Active', 'Inactive'))
);

CREATE TABLE IF NOT EXISTS Writer (
    writer_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    birthdate DATE,
    sex VARCHAR(20),
    CONSTRAINT check_sex_writer CHECK (sex IN ('Male', 'Female', 'Intersex'))
);

CREATE TABLE IF NOT EXISTS Game_Devs (
    game_id INT,
    developer_id INT,
    PRIMARY KEY (game_id, developer_id),
    CONSTRAINT fk_gameid_gamedevs FOREIGN KEY (game_id) REFERENCES Games(game_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_devid_gamedevs FOREIGN KEY (developer_id) REFERENCES Developer(developer_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Book_Author (
    book_id INT,
    author_id INT,
    PRIMARY KEY (book_id, author_id),
    CONSTRAINT fk_bookid_bookauthor FOREIGN KEY (book_id) REFERENCES Books(book_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_authorid_bookauthor FOREIGN KEY (author_id) REFERENCES Author(author_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Anime_Writer (
    anime_id INT,
    writer_id INT,
    PRIMARY KEY (anime_id, writer_id),
    CONSTRAINT fk_animeid_animewriter FOREIGN KEY (anime_id) REFERENCES Anime(anime_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_writerid_animewriter FOREIGN KEY (writer_id) REFERENCES Writer(writer_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Anime_Studio (
    anime_id INT,
    anime_studio_id INT,
    PRIMARY KEY (anime_id, anime_studio_id),
    CONSTRAINT fk_animeid_animestudio FOREIGN KEY (anime_id) REFERENCES Anime(anime_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_animestudioid_animestudio FOREIGN KEY (anime_studio_id) REFERENCES A_Studio(anime_studio_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Cartoon_Studio (
    cartoon_id INT,
    cartoon_studio_id INT,
    PRIMARY KEY (cartoon_id, cartoon_studio_id),
    CONSTRAINT fk_cartoonid_cartoonstudio FOREIGN KEY (cartoon_id) REFERENCES Cartoons(cartoon_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_cartoonstudioid_cartoonstudio FOREIGN KEY (cartoon_studio_id) REFERENCES C_Studio(cartoon_studio_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movie_Director (
    movie_id INT,
    director_id INT,
    PRIMARY KEY (movie_id, director_id),
    CONSTRAINT fk_movieid_moviedirector FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_directorid_moviedirector FOREIGN KEY (director_id) REFERENCES Director(director_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movie_Producer (
    movie_id INT,
    producer_id INT,
    PRIMARY KEY (movie_id, producer_id),
    CONSTRAINT fk_movieid_movieproducer FOREIGN KEY (movie_id) REFERENCES Movies(movie_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_producerid_movieproducer FOREIGN KEY (producer_id) REFERENCES Producer(producer_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Series_Producer (
    series_id INT,
    producer_id INT,
    PRIMARY KEY (series_id, producer_id),
    CONSTRAINT fk_seriesid_seriesproducer FOREIGN KEY (series_id) REFERENCES Series(series_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_producerid_seriesproducer FOREIGN KEY (producer_id) REFERENCES Producer(producer_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Followers (
    username VARCHAR(255) NOT NULL,
    follower_username VARCHAR(255) NOT NULL,
    time_followed TIMESTAMP,
    PRIMARY KEY (username, follower_username),
    CONSTRAINT fk_username_followers FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_follower_username_followers FOREIGN KEY (follower_username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE
);

DELIMITER //

CREATE TRIGGER prevent_self_follow
BEFORE INSERT ON Followers
FOR EACH ROW
BEGIN
    IF NEW.username = NEW.follower_username THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'A user cannot follow themselves.';
    END IF;
END;
//

DELIMITER ;

CREATE TABLE IF NOT EXISTS Milestones (
    milestone_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    date_achieved DATE
);

CREATE TABLE IF NOT EXISTS User_Milestone (
    username VARCHAR(255) NOT NULL,
    milestone_id INT NOT NULL,
    PRIMARY KEY (username, milestone_id),
    CONSTRAINT fk_username_usermilestone FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_milestoneid_usermilestone FOREIGN KEY (milestone_id) REFERENCES Milestones(milestone_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Notes (
    note_id INT PRIMARY KEY auto_increment,
    content TEXT,
    username VARCHAR(255) NOT NULL,
    media_id INT NOT NULL,
    CONSTRAINT unique_usermedia UNIQUE (username, media_id),
    CONSTRAINT fk_username_notes FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_mediaid_notes FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Reviews (
    review_id INT PRIMARY KEY auto_increment,
    content TEXT,
    upvotes_count INT DEFAULT 0,
    downvotes_count INT DEFAULT 0,
    username VARCHAR(255) NOT NULL,
    media_id INT NOT NULL,
    CONSTRAINT unique_usermedia_reviews UNIQUE (username, media_id),
    CONSTRAINT fk_username_reviews FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_mediaid_reviews FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Discussions (
    discussion_id INT PRIMARY KEY auto_increment,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP,
    upvotes INT DEFAULT 0,
    downvotes INT DEFAULT 0,
    username VARCHAR(255) NOT NULL,
    mediatag VARCHAR(20) CHECK (mediatag IN ('Movies','Books','Games','Series','Cartoons','Anime')),
    CONSTRAINT fk_username_discussions FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Comments (
    comment_id INT PRIMARY KEY auto_increment,
    content TEXT,
    likes INT DEFAULT 0,
    discussion_id INT,
    username VARCHAR(255),
    CONSTRAINT fk_discussionid_comments FOREIGN KEY (discussion_id) REFERENCES Discussions(discussion_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_username_comments FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Boards (
    board_id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    username VARCHAR(255) NOT NULL,
    def boolean not null,
    CONSTRAINT fk_username_boards FOREIGN KEY (username) REFERENCES Users(username) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Board_Content (
    board_id INT,
    media_id INT,
    PRIMARY KEY (board_id, media_id),
    CONSTRAINT fk_boardid_boardcontent FOREIGN KEY (board_id) REFERENCES Boards(board_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_mediaid_boardcontent FOREIGN KEY (media_id) REFERENCES Media(media_id) ON UPDATE CASCADE ON DELETE CASCADE
);

create table if not exists LikeComments (
	username VARCHAR(255) not null,
    comment_id int not null,
    constraint fk_username_likecomments foreign key (username) references users(username),
    constraint fk_comment_likecomments foreign key (comment_id) references comments(comment_id)
    
	);
    
CREATE TABLE votes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username varchar(255) not null,
  discussion_id INT not null,
  UNIQUE(username, discussion_id),
  constraint fk_username_votes foreign key (username) references users(username),
    constraint fk_discussion_votes foreign key (discussion_id) references discussions(discussion_id)
);
