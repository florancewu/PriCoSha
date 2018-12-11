from flask import Flask, flash, app, request, session, render_template, url_for,\
logging, redirect
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps
from datetime import datetime, timedelta
import pymysql.cursors
#username is the same as email

app = Flask(__name__)
app.secret_key = "database"

conn = pymysql.connect(host='127.0.0.1',
                         user='root',
                         password='',
                         port=3306,
                         db='project',
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)

@app.before_request #for security purposes
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
 

@app.route('/')
def index():

    if 'logged_in' in session:
        return redirect(url_for('mainPage'))
    return render_template('main.html')

class RegisterForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=50)])#conditions
    last_name = StringField('Last Name', [validators.Length(min=1, max=50)])
    username = StringField('Email', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords do not match'),
            validators.Length(min=5, max=100)
        ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        firstName = form.first_name.data
        lastName = form.last_name.data
        username = form.username.data
        password = form.password.data
        cur = conn.cursor()
        
        # Check if email in db
        query = 'SELECT * FROM Person WHERE email = %s'
        cur.execute(query, (username))

        data = cur.fetchone()

        if (data):
            flash('This email is already taken')
            cur.close()
            return redirect(url_for('register'))
        else:
            cur.execute("INSERT INTO Person(email, password, fname, lname)\
                    VALUES(%s, %s, %s, %s)", (username, password,firstName,lastName))
            #inserts user information into system
            conn.commit()
            cur.close()
            flash('You are now registered. Please log in.') 
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        cur = conn.cursor()

        #retrieves data from DB to check if in sys
        query = cur.execute("SELECT * FROM Person WHERE email = %s", [username])

        
        if(query > 0):
            data = cur.fetchone()
            password = data['password']

            # Compare 
            if (password_candidate == password): #input valid
                session['logged_in'] = True
                session['username'] = username
                flash("You are now logged in", "success")
                return redirect(url_for("mainPage"))
            else:
                error = "Incorrect password"
                return render_template("login.html", error=error)
            
            cur.close()
        else: #Can't validate
            error = "Email not found" 
            return render_template('login.html', error=error)
            cur.close()
    return render_template('login.html')

#logged in or not
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Not authorized, please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#to log out
@app.route("/logout")
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return render_template('main.html')

@app.route('/mainPage')
@is_logged_in
def mainPage():
    username = session['username']
    cursor = conn.cursor()
    query = 'SELECT post_time, item_name, item_id FROM ContentItem WHERE email_post = %s OR is_pub = 1 ORDER BY item_id DESC'
    cursor.execute(query, (username))
    data = cursor.fetchall()
    
    query2 = 'SELECT Comment.post_time, comment_text, Comment.item_id, Comment.email FROM Comment JOIN ContentItem on Comment.item_id = ContentItem.item_id WHERE is_pub = 1 or ContentItem.email_post = %s ORDER BY item_id DESC'    
    cursor.execute(query2, (username))
    comments = cursor.fetchall()
        
    query3 = 'SELECT Tag.tagtime, Tag.email_tagged,Tag.email_tagger, Tag.item_id, Person.fname, Person.lname FROM Tag NATURAL JOIN Person WHERE Tag.email_tagged = Person.email ORDER BY item_id DESC'
    cursor.execute(query3,)
    tags = cursor.fetchall()
    

    query4 = 'SELECT fg_name FROM FriendGroup WHERE owner_email = %s'
    cursor.execute(query4,(username))
    groups = cursor.fetchall()
    #only creator of the group has permission to share
   

    tagged_query = 'SELECT DISTINCT ContentItem.post_time, item_name, ContentItem.item_id FROM ContentItem JOIN Tag ON ContentItem.item_id = Tag.item_id WHERE (email_tagged = %s) AND (status = 1) ORDER BY post_time DESC'
    cursor.execute(tagged_query,(username))
    data2 = cursor.fetchall()

    tagged_comments = 'SELECT DISTINCT Comment.item_id, Comment.post_time, comment_text, Comment.email\
    FROM Comment JOIN Tag on Comment.item_id = Tag.item_id WHERE status = 1 and email_tagged= %s ORDER BY item_id DESC'
    cursor.execute(tagged_comments,(username))
    comments_tagged = cursor.fetchall()

    shared_query = "SELECT DISTINCT ContentItem.post_time, Share.item_id, item_name \
    from Share join ContentItem on Share.item_id = ContentItem.item_id JOIN Member on Share.fg_name = Member.fg_name \
    where Member.email = %s order by post_time desc"
    cursor.execute(shared_query,(username))
    shared_posts = cursor.fetchall()



    shared_comments = 'SELECT DISTINCT Comment.item_id, Comment.post_time, comment_text, Comment.email \
    FROM Comment JOIN Share on Comment.item_id = Share.item_id JOIN Member on Share.fg_name = Member.fg_name \
    where Member.email = %s order by post_time desc' 
    cursor.execute(shared_comments,(username))
    comments_shared = cursor.fetchall()

    cursor.close()
    
    return render_template('mainPage.html', username=username, posts=data,\
            comments=comments, tags = tags, taggedposts = data2, groups=groups,\
            shared_posts = shared_posts, comments_tagged = comments_tagged, \
            comments_shared = comments_shared)

@app.route('/managefriend', methods=['GET','POST'])
def manage_friend():
    return render_template('addfriend.html')

@app.route('/addfriends', methods=['GET','POST'])
def add_friends():
    username = request.form['username']
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    group_name = request.form["group_name"]
    owner = request.form["creator"]
    cur = conn.cursor()
    
    query2 = "SELECT * FROM Member WHERE email = %s && fg_name = %s"
    cur.execute(query2, (username, group_name))
    data = cur.fetchone()
    #checks if person is already friends with user
    if (data):
        flash('This friend is already in your friend group!', "danger")
        conn.commit()
        cur.close()
        return render_template('addfriend.html')
    else: #adds friend
        query1 = "INSERT INTO Member(email, fg_name, owner_email) VALUES(%s, %s, %s)"
        cur.execute(query1, (username, group_name, owner))
        conn.commit()
        cur.close()
        flash('Your friend has been added to your friend group!', "success")
        return render_template('addfriend.html')




#create post to share
@app.route('/post', methods=['GET', 'POST'])
def post():
    if 'logged_in' in session:
        #username
        username = session['username']
        cursor = conn.cursor()
        content_name = request.form['item_name']
        pub_status = False if request.form.get('pub_status') else True #public or private
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if pub_status == True:
            query = 'INSERT INTO ContentItem (item_name, email_post,post_time, is_pub) VALUES(%s, %s, %s, %s)'
            cursor.execute(query, (content_name, username, timestamp, pub_status))

            conn.commit()
            cursor.close()
            flash('You have successfully posted!', 'success')
            return redirect(url_for('mainPage'))

        elif pub_status == False:
            query = 'INSERT INTO ContenItem (item_name, email_post, post_time is_pub) VALUES(%s, %s, %s, %s)'
            cursor.execute(query, (content_name, username, timestamp, pub_status))

            maxValQuery = 'SELECT MAX(item_id) FROM ContentItem'
            cursor.execute(maxValQuery)
            maxVal = cursor.fetchone()
            maxVal = maxVal['MAX(item_id)']

            groupNames = request.form['groupNames']
            listOfGroupNames = groupNames.split(',')

            cursor = conn.cursor()
            for group in listOfGroupNames:
                query = 'INSERT INTO Share (item_id, fg_name, owner_email) VALUES (%s, %s, %s)'
                cursor.execute(query, (maxVal, group, username))
            conn.commit()
            cursor.close()
            flash('You have successfully posted to private group', 'success')
            return redirect(url_for('mainPage'))

    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))

@app.route('/sharepost', methods=['GET', 'POST'])
def sharepost():
    if 'logged_in' in session:
        username = session['username']
        contentID = request.form['contentID']
        group_name = request.form['group_name']

        cursor = conn.cursor()

        q1 = 'INSERT INTO Share(item_id, fg_name, owner_email) VALUES (%s, %s, %s)'
        cursor.execute(q1,(contentID, group_name, username))
        flash('You have successfully shared the post with your group!', 'success')
        conn.commit()
        cursor.close()
        return redirect(url_for('mainPage') )

    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))

#only allowed to delete posts that the user created
@app.route('/deletepost', methods=['GET', 'POST'])
def deletepost():
    if 'logged_in' in session:
        contentID = request.form['contentID']

        cur=conn.cursor()

        #checks through everything to delete
        q1 = "DELETE FROM Tag WHERE item_id = %s"
        cur.execute(q1,(contentID))

        q2 = "DELETE FROM Comment WHERE item_id = %s"
        cur.execute(q2, (contentID))

        q4 = "DELETE FROM Share WHERE item_id = %s"
        cur.execute(q4,(contentID))

        q3 = "DELETE FROM ContentItem WHERE item_id = %s"
        cur.execute(q3,(contentID))

        flash('You have deleted your post!', 'success')
        conn.commit()
        cur.close()
        return redirect(url_for('mainPage'))

    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))


@app.route('/comment', methods=['GET','POST'])
def comment():
    if 'logged_in' in session:
        username = session['username']
        commentID = request.form['commentID']
        comment_text = request.form['comment']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cur = conn.cursor()
        query2 = 'INSERT INTO Comment (item_id, email,post_time, comment_text) VALUES(%s, %s, %s, %s)'
        cur.execute(query2, (commentID, username, timestamp, comment_text))
        flash('You have successfully added comment to this content!', 'success')

        return redirect(url_for('mainPage'))

    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))

#tag function
@app.route('/tag', methods=['GET' , 'POST'])
def tag():
    if 'logged_in' in session:
        tagger = session['username']
        taggee = request.form['taggee']
        contentID = request.form['contentID']
        selectContent = request.form.get('selectContent')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cur = conn.cursor()

        query = cur.execute('SELECT * FROM Person WHERE email = %s',\
                [taggee])

        if (query > 0):
            TagData = cur.execute('SELECT * FROM Share join ContentItem on Share.item_id = ContentItem.item_id \
            join Member on Share.fg_name = Member.fg_name \
            WHERE Member.email = %s and Share.item_id = %s', (taggee, contentID))
            PublicData = cur.execute('SELECT * FROM ContentItem WHERE is_pub=1 and item_id=%s',(contentID))
            
            if (not TagData and not PublicData):
                flash("User is not allowed to view Content, so can't be tagged",'danger')
                cur.close()
                return redirect(url_for("mainPage"))
            
            
            #self-tagging
            if taggee == tagger:
        
                query = cur.execute('INSERT INTO Tag (item_id, email_tagger, email_tagged, status, tagtime)\
                VALUES(%s, %s, %s, %s, %s)' , (contentID, tagger, tagger, True, timestamp ))

                flash('You have tagged yourself in this content!', 'success')
            #tag other
            else:
                query = cur.execute('INSERT INTO Tag (item_id, email_tagger, email_tagged, status, tagtime)\
                VALUES(%s, %s, %s, %s, %s)',(contentID, tagger, taggee, False, timestamp)) #needs approval first by other user
                flash('You have tagged ' + taggee + ' in this content!','success')
            conn.commit()
            cur.close()
            return redirect(url_for('mainPage'))
        else:
            flash("User does not exist", "danger")
            cur.close()
            return redirect(url_for("mainPage"))

    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))

#tags that need to be approved
@app.route("/tags")
def tags():
    if 'logged_in' in session:
        username = session['username']
        cur = conn.cursor()
        cur.execute('SELECT email_tagger, ContentItem.item_id, item_name, email_tagged \
        FROM Tag JOIN ContentItem\
        ON ContentItem.item_id = Tag.item_id\
        WHERE email_tagged = %s AND status = 1', username)
        pendingTags = cur.fetchall()
        conn.commit()
        cur.close()

        return render_template("tags.html", pendingTags=pendingTags)
    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))

@app.route('/manageTags', methods=['GET', 'POST'])
def manageTags():
    if 'logged_in' in session:
        taggee = session['username']
        tagger = request.form['tagger']
        id = request.form['id']
        approvalStatus = request.form['approval']
        cur = conn.cursor()
        
        if approvalStatus == "accept":
            cur.execute('UPDATE Tag SET status = 1 WHERE item_id = %s AND email_tagged = %s AND email_tagger = %s', (id, taggee, tagger))
            flash('The tag has been approved', 'success')
        else:
            cur.execute('DELETE FROM Tag WHERE item_id = %s AND email_tagged = %s AND email_tagger = %s', (id, taggee, tagger))
            flash('The tag has been deleted', 'success')

        cur.execute('SELECT email_tagger, item_id FROM Tag WHERE email_tagged = %s AND status = 0', taggee)
        pendingTags = cur.fetchall()

        conn.commit()
        cur.close()
        return render_template("tags.html", pendingTags=pendingTags)
    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))



@app.route('/deletegroups', methods=['GET', 'POST'])
def delete_group():
    if 'logged_in' in session:
        # check for create group action
        #if request.form['mems']:
        cursor = conn.cursor()
        username = session['username']
        group_name = request.form['group_name']
        cursor = conn.cursor()
        
        query1 = 'SELECT * FROM FriendGroup WHERE email = %s AND fg_name = %s'
        query2 = 'SELECT username FROM FriendGroup WHERE fg_name = %s'
        cursor.execute(query2, group_name)
        data = cursor.fetchone()
        #check if the group exists
        if (cursor.execute(query1, (username, group_name)) == 0):
            flash("The group doesn't exist!", "danger")
            conn.commit()
            return redirect(url_for('creategroup'))
        
        elif (data["username"] != username):
            flash("You do not have the permission to delete this group!", "danger")
            conn.commit()
            return redirect(url_for('creategroup'))
        
        else:
            query3 = 'SELECT * FROM Member WHERE fg_name = %s'
            cursor.execute(query3, group_name)
            data2 = cursor.fetchall()
            
            #delete all members
            for mem in data2:
                mem_username = mem["username"]
                query4 = 'DELETE from Member WHERE email = %s AND fg_name = %s'
                cursor.execute(query4, (mem_username, group_name))
        
            #delete member 
            query5 = 'DELETE from FriendGroup WHERE fg_name = %s AND email = %s'
            cursor.execute(query5, (group_name, username))
            
            conn.commit()
            cursor.close()
            
            flash("Your friend group was successfully deleted!", "success")
            return redirect(url_for('mainPage'))
    
    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))



@app.route('/creategroup')
def creategroup():
    return render_template('groups.html')

#create fg
@app.route('/addgroups', methods=['GET','POST'])
def add_groups():
    if 'logged_in' in session:
        cursor = conn.cursor()
        owner= session['username']
        group_name = request.form['group_name']
        description = request.form['description']
        mems = request.form['mems']
        cursor = conn.cursor()
        #checks if user exists 
        query1 = 'SELECT COUNT(*) FROM Member WHERE email = %s AND fg_name = %s'
        if (cursor.execute(query1, (owner, group_name)) == 0):
           query2 = 'INSERT INTO Member (email, fg_name, owner_email)\VALUES(%s, %s, %s)'
           query3 = 'INSERT INTO FriendGroup (fg_name, owner_email, description)\VALUES(%s, %s, %s)'
           cursor.execute(query2, (owner, group_name, owner))
           cursor.execute(query3, (group_name, owner, description))
           conn.commit()
        
        query4 = 'INSERT INTO FriendGroup (fg_name, owner_email, description) VALUES(%s, %s, %s)'
        cursor.execute(query4, (group_name, owner, description))
        
        listMems = mems.split(', ') #splits list of friends to be added
        
        invalidMems = []
        for mem in listMems:
            #checks if member exists
            query5 = 'SELECT * FROM Person WHERE email = %s'
            val = cursor.execute(query5, mem)
            if (val == 1):
                query6 = 'INSERT INTO Member (email, fg_name, owner_email) VALUES(%s, %s, %s)'
                cursor.execute(query6, (mem, group_name, owner))
            else:
                invalidMems.append(mem)
    
        conn.commit()
        cursor.close()
        #gives results
        if (len(invalidMems)!= 0):
            error = "Following friends could not be added: "
            for mem in invalidMems:
                error = error + str(mem) + " "
            flash(error, "danger")
        else:
            flash('The friend group has been successfully added!', "success")

        return redirect(url_for('mainPage'))
            
    else:
        flash('Timed out, please login again', 'danger')
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = "database"
    app.run(debug=True)
