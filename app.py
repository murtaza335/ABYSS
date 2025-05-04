from database_queries import *
from flask import Flask, jsonify, request, session, render_template, redirect, abort, url_for
from flask_session import Session
from flask_bcrypt import Bcrypt
from datetime import datetime, date
from werkzeug.utils import secure_filename
import os
from flask import send_from_directory
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'abyss'
bcrypt = Bcrypt(app) 

                    # Configuration 
app.config["SESSION_PERMANENT"] = False     # Sessions expire when the browser is closed
app.config["SESSION_TYPE"] = "filesystem"     # Store session data in files


# Configure the folder where the images will be saved
# Set absolute path
UPLOAD_FOLDER = os.path.join(os.getcwd(),'static', 'uploads', 'profile_pics')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Automatically creates folder if missing
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Flask-Session
Session(app)

# mail to send when a user signs up
msg = EmailMessage()




# Gmail SMTP setup
smtp_server = 'smtp.gmail.com'
smtp_port = 587
your_email = 'your_email@gmail.com'
your_password = 'your_app_password'  

import smtplib
from email.message import EmailMessage

def sendmail(username, email):
    # Compose the message
    msg = EmailMessage()
    msg['Subject'] = 'Welcome to Abyss – Explore Media Like Never Before!'
    msg['From'] = 'murtazabaig335@gmail.com'
    msg['To'] = email
    msg.set_content(f"""
Hello {username}, and welcome to Abyss!

We're thrilled to have you join our growing community of media enthusiasts. Abyss is more than just a media database — it’s your gateway to discovering films, books, anime, documentaries, and more through a unique lens: *eras*. Whether you love vintage classics or modern masterpieces, Abyss helps you explore media by time, genre, popularity, and countless other features.

Here’s what you can look forward to:
• Discover media from every era and genre.
• Build your personal lists and watchlists.
• Join discussions, comment, rate, and share opinions with a passionate community.
• Earn badges, write notes, and connect with other users who share your taste.

You’ve just stepped into a space where media is more than entertainment — it’s a journey.

Explore your Abyss.

Best regards,  
The Abyss Team
""")

    # Connect to Gmail SMTP server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    # Login using your App Password
    server.login("murtazabaig335@gmail.com", "fxxbfgfzfqaexvlo")  # No spaces

    # Send email
    server.send_message(msg)

    # Close the connection
    server.quit()

    print(f"Welcome email sent to {email}")
 
# ------------------------------------
# rendering templates 
# ------------------------------------


# ------------home page-------------------
@app.route('/', methods = ['GET'])
def abyssHome():
    return render_template('index.html')
# -------------main era page -------------
@app.route('/mainerapage/<era>', methods=['GET'])
def mainEraPage(era):
    return render_template('prehistory.html')
# -------------main media page -------------
@app.route('/mainmediapage/<era>/<media>', methods=['GET'])
def mainMediaPage(media,era):
    return render_template('movies.html')
# ---------singleDiscussionPage----------
@app.route('/mediapage/<era>/<category>/<title>', methods = ['GET'])
def singleMediaPage(era, category, title):
    return render_template('movies.html')
# ----------leaderboard page---------------
@app.route('/leaderboard', methods=['GET'])
def leaderboard():
    return render_template('leaderboard.html')
# -------community/ discussions page--------
@app.route('/community', methods=['GET'])
def community():
    return render_template('community.html')
# --------user profile page----------
@app.route('/profilepage/<username>', methods = ['GET'])
def userProfilePage(username):
    if username == session.get('username'):
            return render_template('dynamicuserprofile.html')
    else:
        return render_template('dynamicuserprofile.html')
    
# -------one discussion page-------------
@app.route('/discussion/<discussion_id>', methods = ['GET'])    
def rendersingleDiscussionPage(discussion_id):
    return render_template('singlediscussion.html')
# -------signup page / auth----------------
@app.route('/auth', methods = ['GET'])
def authorize():
    return render_template('auth.html')





# apis for sending data to the frontend



# these routes are for the media pages 

# the home page
# the eras page 
# the main media page 
# single media page 


# -------------main era page -------------
# teseted </
@app.route('/api/mainerapagedata/<era>', methods=['GET'])
def mainEraPageData(era):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)  # Forbidden if not AJAX
    data = {}
    # range of years
    eraRange = fetchTimelineRange(era)
    eraDescription = fetchDescriptionOfEra(era)
    subtypes = fetchSubTypesByMainType(era)
    movies = fetchAllMoviesByEra(era)
    cartoons = fetchAllCartoonsByEra(era)
    games = fetchAllGamesByEra(era)
    anime = fetchAllAnimeByEra(era)
    series = fetchAllSeriesByEra(era)
    books = fetchAllBooksByEra(era)

    data = {
        "subtypes": subtypes,
        "eraRange" : eraRange,
        "eraDescription": eraDescription,
        "movies": movies,
        "cartoons": cartoons,
        "games": games,
        "anime": anime,
        "series": series,
        "books": books
    }

    return jsonify(data)

# -------------main media page -------------
@app.route('/api/mainmediapagedata/<era>/<media>', methods=['GET'])
def mainMediaPageData(era,media):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)  # Forbidden if not AJAX
    data = {}
    media = fetchAllMediaByEra(era, media)
    eras = fetchAllEras()
    data = {
        "eras" : eras,
        "media" : media
    }
    return render_template('movies.html'),jsonify(data) 
# ---------single media page----------
@app.route('/api/mediadata/<category>/<media_id>', methods = ['GET'])
def singleMediaPageData(category, media_id):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)  # Forbidden if not AJAX
    data = fetchDataForSingleMediaPage(category, media_id)
    return jsonify(data)

# route for rendering the single media page
@app.route('/media/<category>/<media_id>', methods = ['GET'])
def renderSingleMediaPage(category, media_id):
    return render_template('singlemedia.html')

# route for adding data to the board 
@app.route('/api/addToBoard', methods = ['POST'])
def addToBoard():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    data = request.get_json()
    media_id = data.get('media_id')
    board_id = data.get('board_id')


# creating a new board 
@app.route('/api/createBoard', methods = ['POST'])
def createBoard():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    data = request.get_json()
    board_name = data.get('name')
    description = data.get('description')
    username = session.get('username')
    if username is None:
        return jsonify({"error": "Please login first"}), 401
    if createBoardByUsername(username, board_name, description):
        return jsonify(True), 201
    else:
        return jsonify(False), 400

# editing the profile of the user
@app.route('/api/editProfile', methods=['POST'])
def editProfile():
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)

    data = request.form
    print(data)
    username = data.get('username')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    bio = data.get('bio')

    file_path = None

    # Handle profile picture if uploaded
    if 'profilePic' in request.files:
        file = request.files['profilePic']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Create folder if it doesn't exist
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            file.save(file_path)
        elif file.filename != '':
            return jsonify({"error": "Invalid file type"}), 400

    # Call to update profile in DB
    success = editUserProfile(username, firstname, lastname, bio, f"static/uploads/profile_pics/{filename}" if file_path else None)

    if success:
        return jsonify(True), 200
    else:
        return jsonify(False), 400

# flask route to serve the profile picture
@app.route('/uploads/profile_pics/<filename>')
def serve_profile_pic(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# flask route for the follow functionality
@app.route('/api/follow/<username>/<follower>', methods=['POST'])
def followUser(username, follower):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    # we will check on the frontend if the user is logged in or not
    if followUserByUsername(username, follower):
        return jsonify(True), 200
    else:
        return jsonify(False), 400

# route for unfollowing the user
@app.route('/api/unfollow/<username>/<follower>', methods=['POST'])
def unfollowUser(username, follower):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)

    print("unfollow")
    # we will check on the frontend if the user is logged in or not
    if unfollowUserByUsername(username, follower):
        return jsonify(True), 200
    else:
        return jsonify(False), 400

# route to check if the user is following the other user or not
@app.route('/api/checkfollow/<username>/<follower>', methods=['GET'])
def checkFollow(username, follower):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    # we will check on the frontend if the user is logged in or not
    result = checkIfUserFollowing(username, follower)
    return jsonify({"following": result})

# ----------leaderboard page---------------
@app.route('/api/leaderboardData', methods=['GET'])
def leaderboardData():
    leaderboard = fetchLeaderBoardData()
    return jsonify(leaderboard)

# -------community/ discussions page--------
@app.route('/api/communityData', methods=['GET'])
def communityData():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    community = fetchCommunityData()
    return jsonify(community)

# api routes for the main search bar 
# if no toggle button is selected 
# tested </
@app.route('/api/search/<query>', methods = ['GET'])
def mainSearchBarAllMedia(query):
    result = searchFromAllMedia(query)
    return jsonify(result)

# if any of the toggle button is selected
# tested </
@app.route('/api/search/<category>/<query>', methods = ['GET'])
def mainSearchBarOneMedia(query,category):
    result = searchFromOneCategory(query, category)
    return jsonify(result)

# api route for displaying the timeline range on the homepage 
# tested </
@app.route('/api/timelineRange', methods = ['GET'])
def timelineRange():
    eralist = fetchlistoferas()
    result = {}
    for era in eralist:
        result[era["name"]] = fetchTimelineRange(era['name'])
    return jsonify(result)

# api for the login state of the user
@app.route('/api/loginstatedata', methods = ['GET'])
def loginStateData():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    # the frontend will send the username in the headers
    username = request.headers.get('Username')
    # Check if the user is logged in
    if username == session.get('username'):
        return jsonify({"loggedIn": True})
    else:   
        return jsonify({"loggedIn": False}),401




# apis for the discussions page


# ---------singleDiscussionPage----------
@app.route('/api/discussionById/<discussion_id>', methods = ['GET'])
def singleDiscussionPage(discussion_id):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    data = fetchDataForSingleDiscussion(discussion_id)
    # Format the datetime object into a readable string
    if isinstance(data.get('created_at'), datetime):
        data['created_at'] = data['created_at'].strftime('%d %b %Y')
    if data is None:
        return jsonify({"error": "Discussion not found"}), 404
    return jsonify(data)

# api for the comments on the discussion
@app.route('/api/discussionById/<discussion_id>/comments', methods = ['GET'])
def getComments(discussion_id):     
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
        
    comments = fetchComments(discussion_id)
    return jsonify(comments)

# api for incrementing the like counts
@app.route('/api/incrementlikecount/<username>/<comment_id>', methods = ['GET'])
def incrementLikeCountofcomments(username, comment_id):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    
    return incrementLikeCount(username, comment_id)

# api for checking whether the current user has liked a specific comment or not 
@app.route('/api/checklike/<username>/<comment_id>', methods = ['GET'])
def checkLike(username, comment_id):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    result = checkIfUserLikedComment(username, comment_id)
    return jsonify({"liked": result})
# api for fetching the discussions for a specific media tag
@app.route('/api/discussionByMediatag/<mediatag>', methods = ['GET'])
def discussionsByMediaTag(mediatag):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    discussions = fetchDiscussionsByMediaTag(mediatag)
    return jsonify(discussions)

# api for saving the comment for the discussion 
@app.route('/api/addCommentToDiscussion', methods = ['POST'])
def addCommentToDiscussion():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    data = request.get_json()
    discussion_id = data.get('discussion_id')
    comment = data.get('comment')
    username = data.get('username')
    if username != session.get('username'):
        return jsonify("Please login first"),401
    if addComment(discussion_id, comment, username):
        return jsonify(True), 201
    else:
        return jsonify(False), 400

# api for the voting of the discussion
@app.route('/api/voteDiscussion/<username>/<discussion_id>', methods = ['GET'])
def voteDiscussion(username, discussion_id):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    # we will check on the frontend if the user is logged in or not
    return voteDiscussionById(discussion_id, username)


# check if the user has upvoted the discussion or not 
@app.route('/api/checkUpvoteDiscussion/<username>/<discussion_id>',methods = ['GET'])
def upvoteofdiscussion(username, discussion_id):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    # we will check on the frontend if the user is logged in or not
    return checkupvoteofdiscussion(username, discussion_id)


# --------user profile page----------

@app.route('/api/profile/<username>', methods = ['GET'])
def userProfile(username):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)  # Forbidden if not AJAX
    
    userdata = fetchAllUserData(username)
    followerCount = fetchFollowersCount(username)
    followingCount = fetchFollowingCount(username)

    data = {
            "userdata": userdata,
            "followerCount": followerCount,
            "followingCount": followingCount,
        }
    
    return jsonify(data)

# api to fetch the boards of the user
@app.route('/api/profile/<username>/boards', methods = ['GET'])
def userBoards(username):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    return fetchAllBoardsByUsername(username)
    
# api for fetching the milestones of the user
@app.route('/api/profile/<username>/milestones', methods = ['GET'])
def userMilestones(username):
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    result =  fetchUserMilestoneData(username)
    if result is None:
        return jsonify({"error": "Discussion not found"}), 404
    for milestone in result:
        if isinstance(milestone.get('date_achieved'), (datetime, date)):
            milestone['date_achieved'] = milestone['date_achieved'].strftime('%d %b %Y')
    
    return result
# --------------loign signup routes------------

# login route
# tested </
@app.route('/api/login', methods=['POST'])
def loginUser():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not verifyUsernameAndPassword(username, password):
        return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

    # Save user in session
    session['username'] = username
    logstateDatabase(username, True)
    return jsonify({'success': True, 'username': username})

# signup route
@app.route('/api/signup' , methods = ['POST'])
def signupUser():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)
    data = request.get_json()
    # assuming that no field is empty (checked on the frontend)
    username = data.get('username')
    if ifUserExist(username):
        return jsonify({"error":"username already exists"}), 400
    
    password = data.get('password')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    email = data.get('email')
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    bio = data.get('bio')
    if addUser(username, firstname, lastname, hashed_password, email, bio):
        session['username'] = username
        logstateDatabase(username, True)

        # sendmail(username, email)
        return jsonify({"success": "user added"}), 201
    else:
        return jsonify({"error": "user not added"}), 400


# logout route 
@app.route('/api/logout', methods=['GET'])
def logout():
    # Only allow AJAX (fetch) calls
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        abort(403)  # Forbidden if not AJAX
    username = session.get('username')
    
    if not username:
        return jsonify({"error": "Unauthorized logout request!"}), 403
    
    # Remove the username from the session to log out
    session.pop('username', None)
    
    # Update the database to mark the user as logged out
    logstateDatabase(username, False)
    
    # Return a JSON response for success
    return jsonify({"message": "Logout successful!"}), 200



# creating a decorator for the login_required
# now we will just use the decorator before the function name that is to be checked whether the user is logged in or not
# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'username' not in session:
#             return jsonify({'error': 'Unauthorized'}), 401
#         return f(*args, **kwargs)
#     return decorated_function




# uploading the profile picture
# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# fetch the username of the current logged in user
@app.route('/api/loggedinuser',methods = ['GET'])
def loggedinuser():
    if session.get('username'):
        return jsonify(session.get('username'))
    else:
        return jsonify({"error": "The user is not logged in"})

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug = True, threaded = True) 
