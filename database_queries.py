import mysql.connector
from flask_bcrypt import bcrypt
from mysql.connector import Error
# establishing the connection with the database
def get_connection():
    return mysql.connector.connect(
        host="localhost",       
        user="root",  
        password="12345678",
        database="abyssdatabase7",
        use_pure=True
    )

# search all media
def searchFromAllMedia(string):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT media_id,title FROM media WHERE title LIKE %s"
    cursor.execute(query, (f"{string}%",))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# search media from one category
def searchFromOneCategory(string, category):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"SELECT title FROM media WHERE title LIKE %s and mediatype = %s"
    cursor.execute(query, (f"{string}%",category))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetchTimelineRange(era):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select era_range from eras where name = %s"
    cursor.execute(query,(era,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result
    
def fetchlistoferas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select name from eras"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetchSubTypesByMainType(maintype):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "select e2.name , e1.name from eras e1 join eras e2 on e1.parent_era_id = e2.era_id where e2.name = %s "
    cursor.execute(query, (maintype,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def fetchDataByCategory(era, category):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM all_media WHERE era = %s AND category = %s"
    cursor.execute(query, (era, category))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetchDescriptionOfEra(era):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT era_description FROM eras WHERE name = %s"
    cursor.execute(query, (era,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Generalized function for fetching all media of a specific type by era
def fetchAllMediaByEra(era, media_type):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select media_id, title, description, img_link, age_rating, rating from media m join eras e on m.era_id = e.era_id where e.name = %s and m.mediatype = %s"
    cursor.execute(query, (era,media_type))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetchAllEras():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select name from eras"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Shortcuts for specific media types
def fetchAllMoviesByEra(era): return fetchAllMediaByEra(era, 'movies')
def fetchAllCartoonsByEra(era): return fetchAllMediaByEra(era, 'cartoons')
def fetchAllGamesByEra(era): return fetchAllMediaByEra(era, 'games')
def fetchAllAnimeByEra(era): return fetchAllMediaByEra(era, 'anime')
def fetchAllSeriesByEra(era): return fetchAllMediaByEra(era, 'series')
def fetchAllBooksByEra(era): return fetchAllMediaByEra(era, 'books')

# verify username and password
def verifyUsernameAndPassword(username, password):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if(username):
        query = "SELECT password_hashed FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        hashed_password = cursor.fetchone()

        # converting the password from the user and the hashed_password into PYbytes because the bcrypt.checkpw needs the arguments in the form of the pybytes
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = hashed_password["password_hashed"].encode('utf-8')
        cursor.close()
        conn.close()
        return bcrypt.checkpw(password_bytes,hashed_password_bytes)
    else:
        return False
    
   

def ifUserExist(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select * from users where username = %s"
    cursor.execute(query, (username, ))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if(result):
        return True
    else :
        return False
    

# this function is adding user to the database and also creating a default board for the user
def addUser(username, firstname, lastname, hashed_password, email, bio):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"""
    INSERT INTO users (
    username, firstname, lastname, password_hashed, time_created, bio, email
) VALUES
(%s,%s ,%s , %s, NOW() , %s, %s)
"""
    cursor.execute(query, (username, firstname, lastname, hashed_password, bio,email))
    # Commit the changes to the database
    conn.commit()
    query = f"""  
    insert into boards (name, description, username, def) values (%s, %s, %s,%s)
    """
    cursor.execute(query, (f"{username}'s board", f"Your default Board, {username} !", username, True))


    # Commit the changes to the database
    conn.commit()
    cursor.close()
    conn.close()
    if (cursor.rowcount):
        return True
    else:
        return False


    
# this function is fetching the data of the user from the database
def fetchAllUserData(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select username, firstname, lastname, bio, img_link from users where username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# this is fetching the board count for the user
# def fetchBoardCount(username):
#     conn = get_connection()
#     cursor = conn.cursor()
#     query = f"select count(*) from boards where username = %s"

#     cursor.execute(query, (username,))
#     result = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     return result[0]

# fetching all the boards for the user and its count
def fetchAllBoardsByUsername(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = f"select * from boards where username = %s"
    cursor.execute(query, (username,))
    boards = cursor.fetchall()
    query = f"select count(*) as board_count from boards where username = %s"
    cursor.execute(query, (username,))
    count = cursor.fetchone()
    result = {
        "boards": boards,
        "count": count
    }
    cursor.close()
    conn.close()
    return result

# this is fetching the follower count for the user
def fetchFollowersCount(username):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"select count(*) from followers where username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

# following count
def fetchFollowingCount(username):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"select count(*) from followers where follower_username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]

# this is fetching the earned milestones for the user 
def fetchUserMilestoneData(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # query for fetching the data for the user milestone based on the user activity in the past 30 days or week
    query = "select * from milestones m join user_milestone u on u.milestone_id = m.milestone_id where u.username = %s"
    cursor.execute(query,(username,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetchLeaderBoardData():
    conn = get_connection()
    cursor = conn.cursor()
    # query for fetching the data for the leaderboard based on the user activity in the past 30 days or week
    query = f"select * from users "
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def fetchCommunityData(type, mediacategory):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Base query: fetch all required fields and aggregate comment counts
    base_query = """
        SELECT mediatag, discussion_id, title, upvotes, description, username, img_link, comment_count, created_at
        FROM (
            SELECT d.mediatag, d.created_at, d.discussion_id, d.title, d.upvotes, d.description,
                   d.username, u.img_link, COUNT(c.comment_id) AS comment_count
            FROM discussions d
            JOIN users u ON d.username = u.username
            LEFT JOIN comments c ON c.discussion_id = d.discussion_id
            {where_clause}
            GROUP BY d.discussion_id
        ) AS sub
        ORDER BY {order_column} DESC
        LIMIT 20
    """

    # Determine WHERE clause and order column
    where_clause = ""
    params = ()
    # print(mediacategory)
    if mediacategory != 'all':
        where_clause = "WHERE d.mediatag = %s"
        params = (mediacategory,)

    order_column = "created_at" if type == "recent" else "upvotes"

    # Fill in the final query with dynamic parts
    final_query = base_query.format(where_clause=where_clause, order_column=order_column)

    # Execute and fetch
    cursor.execute(final_query, params)
    result = cursor.fetchall()

    cursor.close()
    conn.close()
    # formatting the date
    for row in result:
        row['created_at'] = row['created_at'].strftime('%b %d, %Y %I:%M %p')

    return result



# editing the user data in the database

def editUserProfile(username, firstname, lastname, bio,img_link=None):
    try:
        connection = get_connection()
        cursor = connection.cursor()

            # Construct the base SQL query for updating the user's profile
        update_query = """
            UPDATE Users 
            SET firstname = %s, lastname = %s , bio = %s
            """
            
        params = [firstname, lastname, bio]
            
            # Optionally update the profile image link if provided
        if img_link:
            update_query += ", img_link = %s"
            params.append(img_link)
            
            # Add the WHERE condition to specify the user
        update_query += " WHERE username = %s"
        params.append(username)
            
            # Execute the update query
        cursor.execute(update_query, tuple(params))

            # Commit the changes to the database
        connection.commit()

        if cursor.rowcount > 0:
            print(f"User profile for {username} updated successfully.")
            return True
        else:
            print(f"No changes made for {username}.")
            return False
    except Error as e:
        print(f"Error updating profile: {e}")
        return False
    finally:
        cursor.close()
        connection.close()

# following another user
def followUserByUsername(username, follower_username):
    conn = get_connection()
    cursor = conn.cursor()
    # query for following the user
    query = f"insert into followers (username, follower_username, time_followed) values (%s, %s, NOW())"
    cursor.execute(query, (username, follower_username))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount:
        return True
    else:
        return False
    
# unfollowing another user
def unfollowUserByUsername(username, follower_username):
    conn = get_connection()
    cursor = conn.cursor()
    # query for unfollowing the user
    query = f"delete from followers where username = %s and follower_username = %s"
    cursor.execute(query, (username, follower_username))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount:
        return True
    else:
        return False

# checking whether the user is following another user or not
def checkIfUserFollowing(username, follower_username):
    conn = get_connection()
    cursor = conn.cursor()
    # query for checking whether the user is following another user or not
    query = f"select * from followers where username = %s and follower_username = %s"
    cursor.execute(query, (username, follower_username))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return True
    else:
        return False

# create a custom board for the user 
def createBoardByUsername(username, board_name, description):
    conn = get_connection()
    cursor = conn.cursor()
    # query for creating a custom board for the user
    query = f"insert into boards (name, description, username, def) values (%s, %s, %s, False)"
    cursor.execute(query, (board_name, description, username))
    conn.commit()
    cursor.close()
    conn.close()
    if cursor.rowcount:
        return True
    else:
        return False
def fetchDataForSingleMediaPage(category, media_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # removing the last s from the category just because of the table name in the database
    table = category[:-1]
    # query for fetching the data for the single media 
    query = f"select * from media m join {category} s on m.media_id = s.{table}_id where m.media_id = %s"
    cursor.execute(query, (media_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def fetchDataForSingleDiscussion( discussion_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT discussion_id, title, username, description, created_at, upvotes, downvotes, mediatag
    FROM discussions 
    WHERE discussion_id = %s
    """
    
    cursor.execute(query, (discussion_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return data

def fetchComments(discussion_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT comment_id,username, content, likes
    FROM comments 
    WHERE discussion_id = %s
    """
    
    cursor.execute(query, (discussion_id,))
    comments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return comments

def fetchDiscussionsByMediaTag(mediatag):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
    SELECT  discussion_id, title, username, description, upvotes, mediatag
    FROM discussions 
    WHERE mediatag = %s LIMIT 10
    """
    
    cursor.execute(query, (mediatag,))
    discussions = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return discussions

def addComment(discussion_id, content, username):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
    INSERT INTO comments (discussion_id, content, username, likes)
    VALUES (%s, %s, %s, 0)
    """
    
    cursor.execute(query, (discussion_id, content, username))
    conn.commit()
    
    cursor.close()
    conn.close()
    if cursor.rowcount:
        return True
    else:
        return False

# def checkIfUserIsLoggedIn(username):
#     conn = get_connection()
#     cursor = conn.cursor()
#     query = f"select login from users where username = %s"
#     cursor.execute(query,(username,))
#     result = cursor.fetchall()
#     if result:
#         print(result[0][0])
#     else:
#         return 0
#     cursor.close()
#     conn.close()
#     return result[0][0]

def createBoard(username):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"insert into boards ()"
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    if (cursor.rowcount):
        return True
    else:
        return False
    
def logstateDatabase(username, logstate):

    conn = get_connection()
    cursor = conn.cursor()

    query = f"""UPDATE users
                SET login = {logstate}
                WHERE username = %s;"""
    
    cursor.execute(query,(username,))
    conn.commit()
    cursor.close()
    conn.close()

def voteDiscussionById(discussion_id, username):
    conn = get_connection()
    cursor = conn.cursor()
    query = "select * from votes where discussion_id = %s and username = %s"
    cursor.execute(query, (discussion_id, username))
    result = cursor.fetchone()
    if result:
        query = "delete from votes where discussion_id = %s and username = %s"
        cursor.execute(query, (discussion_id, username))
        conn.commit()
        query = "update discussions set upvotes = upvotes - 1 where discussion_id = %s"
        cursor.execute(query, (discussion_id,))
        conn.commit()
        incremented = False
    else:
        query = "insert into votes (discussion_id, username) values (%s, %s)"
        cursor.execute(query, (discussion_id, username))
        conn.commit()
        query = "update discussions set upvotes = upvotes + 1 where discussion_id = %s"
        cursor.execute(query, (discussion_id,))
        conn.commit()
        incremented = True
    

    # Fetch updated vote count
    cursor.execute("SELECT upvotes FROM discussions WHERE discussion_id = %s", (discussion_id,))
    updated_count = cursor.fetchone()[0]

    
    cursor.close()
    conn.close()

    return {"incremented": incremented, "updated_count": updated_count}

# fucntion to check whether the user has liked a discussion or not 
def checkupvoteofdiscussion(username, discussion_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "select * from votes where username = %s and discussion_id = %s"
    cursor.execute(query, (username,discussion_id))
    result = cursor.fetchone()
    if result:
        return ({"success" : True , "upvote" : True})
    else:
        return ({"success" : True , "upvote" : False})



# like functionality of the comments on the discussion

# This function increments the like count of a comment and updates the likecomments table accordingly.
# It checks if the user has already liked the comment. If they have, it decrements the like count and removes the like from the likecomments table.
def incrementLikeCount(username, comment_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Check if user has already liked
        query_check = "SELECT * FROM likecomments WHERE username = %s AND comment_id = %s"
        cursor.execute(query_check, (username, comment_id))
        already_liked = cursor.fetchone()

        if already_liked:
            # Unlike
            query_update = "UPDATE comments SET likes = likes - 1 WHERE comment_id = %s"
            cursor.execute(query_update, (comment_id,))

            query_delete = "DELETE FROM likecomments WHERE comment_id = %s AND username = %s"
            cursor.execute(query_delete, (comment_id, username))
            incremented = False
        else:
            # Like
            query_update = "UPDATE comments SET likes = likes + 1 WHERE comment_id = %s"
            cursor.execute(query_update, (comment_id,))

            query_insert = "INSERT INTO likecomments (comment_id, username) VALUES (%s, %s)"
            cursor.execute(query_insert, (comment_id, username))
            incremented = True

        conn.commit()
        success = cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Error in incrementLikeCount: {e}")
        success = False
        incremented = False
    finally:
        cursor.close()
        conn.close()

    return {"success": success, "incremented": incremented}

# this function is to check whether the user has liked the particular comment or not
def checkIfUserLikedComment(username, comment_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM likecomments WHERE username = %s AND comment_id = %s"
    cursor.execute(query, (username, comment_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        return True
        
    else:
        return False

# email subscribers table filling 
def emailsubscribedb(email):
    conn = get_connection()
    cursor = conn.cursor()
    query = "insert into email_subscribers (email) values (%s)"
    cursor.execute(query,(email,))
    conn.commit()
    if cursor.rowcount:
        return True
    return False
