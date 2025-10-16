from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_from_directory,
    current_app,
)
from werkzeug.utils import secure_filename
import databaseManager as dbHandler
from datetime import datetime
from time import gmtime
import sqlite3
import uuid
import time
import os


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg", "gif"}
app.secret_key = "supersecretkey"
DB_PATH = "Code/leaf&LushDatabase.db"


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.context_processor
def injectUser():
    userId = session.get("user_id")
    return dict(userID=userId)


def makeUploadFolder(app, userID=None):
    base = os.path.join(app.root_path, "static", "uploads")
    os.makedirs(base, exist_ok=True)
    if userID:
        userDir = os.path.join(base, str(userID))
        os.makedirs(userDir, exist_ok=True)
        return userDir
    return base


def getDBConnection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/index.html")
@app.route("/")
def index():
    conn = getDBConnection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM postData WHERE type='recipe' ORDER BY time DESC LIMIT 10"
    )
    latestRecipes = cur.fetchall()
    cur.execute(
        "SELECT *, CASE WHEN upVote='' OR upVote IS NULL THEN 0 ELSE LENGTH(upVote) - LENGTH(REPLACE(upVote,'-','')) + 1 END AS upvote_count "
        "FROM postData WHERE type='produce' ORDER BY upvote_count DESC LIMIT 10"
    )
    bestRated = cur.fetchall()
    cur.execute(
        """
        SELECT *, 
               CASE WHEN star='' OR star IS NULL THEN 0 
                    ELSE LENGTH(star) - LENGTH(REPLACE(star,'-','')) + 1 
               END AS star_count 
        FROM postData 
        WHERE type='post' 
        AND (reply IS "None" OR reply = '')  -- Exclude posts with a reply
        ORDER BY star_count DESC 
        LIMIT 10
    """
    )
    mostStar = cur.fetchall()

    conn.close()

    return render_template(
        "index.html",
        latestRecipes=latestRecipes,
        bestRated=bestRated,
        mostLoved=mostStar,
    )


@app.route("/produce.html")
def produce():
    conn = getDBConnection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM postData WHERE type='produce' ORDER BY time DESC LIMIT 10"
    )
    latestRecipes = cur.fetchall()

    cur.execute(
        "SELECT *, CASE WHEN upVote='' OR upVote IS NULL THEN 0 ELSE LENGTH(upVote) - LENGTH(REPLACE(upVote,'-','')) + 1 END AS upvote_count "
        "FROM postData WHERE type='produce' ORDER BY upvote_count DESC LIMIT 10"
    )
    bestRated = cur.fetchall()

    cur.execute(
        "SELECT *, CASE WHEN star='' OR star IS NULL THEN 0 ELSE LENGTH(star) - LENGTH(REPLACE(star,'-','')) + 1 END AS star_count "
        "FROM postData WHERE type='produce' ORDER BY star_count DESC LIMIT 10"
    )
    mostStar = cur.fetchall()

    conn.close()

    return render_template(
        "produce.html",
        latestRecipes=latestRecipes,
        bestRated=bestRated,
        mostLoved=mostStar,
    )


@app.route("/latestposts.html")
def latestposts():
    conn = getDBConnection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM postData WHERE type='post' ORDER BY time DESC LIMIT 10")
    latestRecipes = cur.fetchall()

    cur.execute(
        """
        SELECT *, 
               CASE WHEN upVote='' OR upVote IS NULL THEN 0 
                    ELSE LENGTH(upVote) - LENGTH(REPLACE(upVote,'-','')) + 1 
               END AS upvote_count 
        FROM postData 
        WHERE type='post' 
        AND (reply IS "None" OR reply = '')  -- Exclude posts with a reply
        ORDER BY upvote_count DESC 
        LIMIT 10
    """
    )
    bestRed = cur.fetchall()

    cur.execute(
        """
        SELECT *, 
               CASE WHEN star='' OR star IS NULL THEN 0 
                    ELSE LENGTH(star) - LENGTH(REPLACE(star,'-','')) + 1 
               END AS star_count 
        FROM postData 
        WHERE type='post' 
        AND (reply IS "None" OR reply = '')  -- Exclude posts with a reply
        ORDER BY star_count DESC 
        LIMIT 10
    """
    )
    mostStar = cur.fetchall()

    conn.close()

    return render_template(
        "latestposts.html",
        latestRecipes=latestRecipes,
        bestRated=bestRed,
        mostLoved=mostStar,
    )


@app.route("/recipes.html")
def recipes():
    conn = getDBConnection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM postData WHERE type='recipe' ORDER BY time DESC LIMIT 10"
    )
    latestRecipes = cur.fetchall()

    cur.execute(
        "SELECT *, CASE WHEN upVote='' OR upVote IS NULL THEN 0 ELSE LENGTH(upVote) - LENGTH(REPLACE(upVote,'-','')) + 1 END AS upvote_count "
        "FROM postData WHERE type='recipe' ORDER BY upvote_count DESC LIMIT 10"
    )
    bestRated = cur.fetchall()

    cur.execute(
        "SELECT *, CASE WHEN star='' OR star IS NULL THEN 0 ELSE LENGTH(star) - LENGTH(REPLACE(star,'-','')) + 1 END AS star_count "
        "FROM postData WHERE type='recipe' ORDER BY star_count DESC LIMIT 10"
    )
    mostStar = cur.fetchall()

    conn.close()

    return render_template(
        "recipes.html",
        latestRecipes=latestRecipes,
        bestRated=bestRated,
        mostLoved=mostStar,
    )


@app.route("/signin", methods=["GET", "POST"])
def signin():
    userID = session.get("user_id")
    if userID != None:
        return redirect(url_for("account"))
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = getDBConnection()
        user = conn.execute(
            "SELECT * FROM userData WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
        conn.close()

        if user:
            flash(f"Welcome back, {username}!", "success")
            session["user_id"] = username
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for("signin"))

    return render_template("signin.html", userID=userID)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    userID = session.get("user_id")
    if userID:
        return redirect(url_for("account"))

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        email = request.form["email"].strip()
        phone = request.form.get("phone", "").strip()
        dob = request.form.get("dob", "").strip()
        bio = request.form.get("bio", "").strip()

        conn = getDBConnection()
        existingUser = conn.execute(
            "SELECT * FROM userData WHERE username = ?", (username,)
        ).fetchone()

        if existingUser:
            conn.close()
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for("signup"))

        conn.execute(
            """
            INSERT INTO userData (username, password, email, phone, dob, bio)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                password,
                email,
                phone,
                dob,
                bio,
            ),
        )
        conn.commit()
        conn.close()

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for("signin"))

    return render_template("signup.html", userID=userID)


@app.route("/account.html", methods=["GET", "POST"])
def account():
    userID = session.get("user_id")
    if not userID:
        return redirect(url_for("signin"))

    conn = getDBConnection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT * FROM userData WHERE username = ?", (userID,))
    userInfo = cur.fetchone()

    cur.execute("SELECT * FROM postData WHERE username = ?", (userID,))
    userPosts = cur.fetchall()
    totalPosts = len(userPosts)

    stats = {
        "totalPosts": totalPosts,
        "repliesMade": 0,
        "repliesReceived": 0,
        "postsYouLiked": 0,
        "postsYouDisliked": 0,
        "postsYouLoveReacted": 0,
        "postsYouFunnyReacted": 0,
        "postsYouIdeaReacted": 0,
        "postsYouStarred": 0,
        "upvotesReceived": 0,
        "downvotesReceived": 0,
        "loveReceived": 0,
        "funnyReceived": 0,
        "ideaReceived": 0,
        "starsReceived": 0,
        "likeDislikeRatio": 0,
        "likeDislikeReceivedRatio": 0,
        "bestPost": "N/A",
        "bestPostRatio": "N/A",
        "favouriteUser": "N/A",
        "biggestFan": "N/A",
    }

    cur.execute(
        "SELECT COUNT(*) FROM postData WHERE reply != 'None' AND username = ?",
        (userID,),
    )
    stats["repliesMade"] = cur.fetchone()[0]

    cur.execute(
        "SELECT COUNT(*) FROM postData WHERE reply IN (SELECT username FROM postData WHERE username = ?)",
        (userID,),
    )
    stats["repliesReceived"] = cur.fetchone()[0]

    cur.execute("SELECT * FROM postData")
    allPosts = cur.fetchall()

    for post in userPosts:

        def countVotes(field):
            return len(post[field].split("-")) if post[field] else 0

        stats["upvotesReceived"] += countVotes("upVote")
        stats["downvotesReceived"] += countVotes("downVote")
        stats["loveReceived"] += countVotes("loveVote")
        stats["funnyReceived"] += countVotes("funnyVote")
        stats["ideaReceived"] += countVotes("ideaVote")
        stats["starsReceived"] += countVotes("star")

    for post in allPosts:
        for field, statKey in [
            ("upVote", "postsYouLiked"),
            ("downVote", "postsYouDisliked"),
            ("loveVote", "postsYouLoveReacted"),
            ("funnyVote", "postsYouFunnyReacted"),
            ("ideaVote", "postsYouIdeaReacted"),
            ("star", "postsYouStarred"),
        ]:
            votes = post[field].split("-") if post[field] else []
            if userID in votes:
                stats[statKey] += 1

    stats["likeDislikeRatio"] = (
        round(stats["postsYouLiked"] / stats["postsYouDisliked"], 2)
        if stats["postsYouDisliked"] != 0
        else stats["postsYouLiked"]
    )
    stats["likeDislikeReceivedRatio"] = (
        round(stats["upvotesReceived"] / stats["downvotesReceived"], 2)
        if stats["downvotesReceived"] != 0
        else stats["upvotesReceived"]
    )

    bestPost = None
    bestRatio = 0
    for post in userPosts:
        up = len(post["upVote"].split("-")) if post["upVote"] else 0
        down = len(post["downVote"].split("-")) if post["downVote"] else 0
        ratio = up / down if down else up
        if ratio > bestRatio:
            bestRatio = ratio
            bestPost = post["title"]
    stats["bestPost"] = bestPost or "N/A"
    stats["bestPostRatio"] = round(bestRatio, 2) if bestPost else "N/A"

    userUpvoteCount = {}
    for post in allPosts:
        if userID in (post["upVote"] or ""):
            author = post["username"]
            userUpvoteCount[author] = userUpvoteCount.get(author, 0) + 1
    stats["favouriteUser"] = (
        max(userUpvoteCount, key=userUpvoteCount.get) if userUpvoteCount else "N/A"
    )

    fanCount = {}
    for post in userPosts:
        if post["upVote"]:
            for voter in post["upVote"].split("-"):
                if voter.strip():
                    fanCount[voter] = fanCount.get(voter, 0) + 1
    stats["biggestFan"] = max(fanCount, key=fanCount.get) if fanCount else "N/A"

    conn.close()

    if request.method == "POST" and request.form.get("action") == "signout":
        session.pop("user_id", None)
        flash("You have been signed out.", "success")
        return redirect(url_for("signin"))

    return render_template(
        "account.html", userID=userID, userInfo=userInfo, stats=stats
    )


@app.route("/posts.html", methods=["GET", "POST"])
def posts():
    conn = getDBConnection()
    userID = session.get("user_id")

    if request.method == "POST":
        action = request.form.get("action")

        if action == "new_post":
            row = conn.execute(
                "SELECT postID FROM postData ORDER BY postID DESC LIMIT 1"
            ).fetchone()
            postID = (row["postID"] if row else 0) + 1

            username = userID
            title = request.form.get("title", "").strip()
            content = request.form.get("content", "").strip()
            timeStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            type = request.form.get("type")
            imagePath = "None"

            file = request.files.get("image_file")
            if file and allowed_file(file.filename):
                origFilename = secure_filename(file.filename)
                uploadDir = makeUploadFolder(current_app, userID)
                uniqueName = f"{int(time.time())}_{uuid.uuid4().hex[:8]}_{origFilename}"
                savePath = os.path.join(uploadDir, uniqueName)
                file.save(savePath)
                imagePath = f"/static/uploads/{userID}/{uniqueName}"

            if username and title and content:
                conn.execute(
                    """
                    INSERT INTO postData (postID, username, title, content, image, time, reply, type)
                    VALUES (?, ?, ?, ?, ?, ?, 'None', ?)
                    """,
                    (postID, username, title, content, imagePath, timeStr, type),
                )
                conn.commit()
                flash("Post submitted successfully!", "success")
            else:
                flash("All fields are required.", "error")
            conn.close()
            return redirect(url_for("posts"))

        elif action == "reply":
            if not userID:
                conn.close()
                return redirect(url_for("posts"))

            parentPostID = request.form.get("postID")
            replyText = request.form.get("reply", "").strip()
            timeStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if replyText:
                row = conn.execute(
                    "SELECT postID FROM postData ORDER BY postID DESC LIMIT 1"
                ).fetchone()
                newReplyID = (row["postID"] if row else 0) + 1
                conn.execute(
                    """
                    INSERT INTO postData (postID, username, title, content, time, reply)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        newReplyID,
                        userID,
                        f"Reply to post {parentPostID}",
                        replyText,
                        timeStr,
                        parentPostID,
                    ),
                )
                conn.commit()

            conn.close()
            return redirect(url_for("posts", postID=parentPostID))

        elif action == "vote":
            postID = request.form.get("postID")
            voteType = request.form.get("voteType")

            if not userID:
                conn.close()
                return redirect(url_for("posts", postID=postID))

            if not postID or not voteType:
                conn.close()
                return redirect(url_for("posts"))

            row = conn.execute(
                f"SELECT {voteType} FROM postData WHERE postID = ?", (postID,)
            ).fetchone()

            if not row:
                conn.close()
                return redirect(url_for("posts"))

            existingVotes = row[voteType] or ""
            voteList = [v for v in existingVotes.split("-") if v]

            if str(userID) in voteList:
                voteList.remove(str(userID))

            else:
                voteList.append(str(userID))

            updatedVotes = "-".join(voteList)
            conn.execute(
                f"UPDATE postData SET {voteType} = ? WHERE postID = ?",
                (updatedVotes, postID),
            )
            conn.commit()
            conn.close()
            return redirect(url_for("posts", postID=postID))

    q = request.args.get("q", "").strip().lower()
    sort = request.args.get("sort", "newest")

    sql = "SELECT * FROM postData WHERE reply = 'None'"
    params = []

    q = request.args.get("q", "").strip().lower()
    sort = request.args.get("sort", "newest")
    typeFilter = request.args.get("typeFilter", "")
    starredOnly = request.args.get("starredOnly")

    if q:
        sql += " AND (LOWER(title) LIKE ? OR LOWER(content) LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])

    if typeFilter:
        sql += " AND type = ?"
        params.append(typeFilter)

    if starredOnly and userID:
        sql += " AND star LIKE ?"
        params.append(f"%{userID}%")

    if sort == "oldest":
        sql += " ORDER BY datetime(time) ASC"
    elif sort == "title":
        sql += " ORDER BY LOWER(title) ASC"
    else:
        sql += " ORDER BY datetime(time) DESC"

    posts = conn.execute(sql, params).fetchall()

    selectedPostID = request.args.get("postID")
    selectedPost = None
    replies = []

    if selectedPostID:
        selectedPost = conn.execute(
            "SELECT * FROM postData WHERE postID = ?", (selectedPostID,)
        ).fetchone()
        replies = conn.execute(
            """
            SELECT * FROM postData
            WHERE reply = ?
            ORDER BY datetime(time) ASC
            """,
            (selectedPostID,),
        ).fetchall()

    conn.close()

    return render_template(
        "posts.html",
        posts=posts,
        selectedPost=selectedPost,
        replies=replies,
        userID=userID,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
