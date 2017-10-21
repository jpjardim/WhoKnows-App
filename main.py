
#### Imports ####
import webapp2
import cgi, logging
import webapp2_extras.appengine.auth.models
from gaesessions import get_current_session
from google.appengine.ext import ndb
from google.appengine.api import users
from gaesessions import delete_expired_sessions
import time

#### HTML Pages ####
#### Header - Used to not have to repeat the header in all pages ####
#### Includes the Jquery Mobile to the project ####
header = """
<script>
    function goBack() {
        $.mobile.changePage("/Profile",{ changeHash: true});
    }
</script>

<script>
    function goLogin() {
        $.mobile.changePage("/",{ changeHash: true});
    }
</script>

<script>
    function goProfile() {
        $.mobile.changePage("/Profile",{ changeHash: true});
    }
</script>

<script>
    function goAsk() {
        $.mobile.changePage("/askQuestion",{ changeHash: true});
    }
</script>

<script>
    function goAnswer() {
        $.mobile.changePage("/answerQuestion",{ changeHash: true});
    }
</script>

<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>WhoKnows</title>
        <link rel="stylesheet" type="text/css" href="css/stylesheet.css">
        <link rel="stylesheet" href="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css" />
        <script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
        <script src="http://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js"></script>
    </head>
"""

script = """
<script>
    function goProfile() {
        $.mobile.changePage("/Profile",{ changeHash: true});
    }
</script>
"""

script2 = """
<script>
    function goLogin() {
        $.mobile.changePage("/",{ changeHash: true});
    }
</script>
"""

#### Index page with Login and link to Signup ####
html = header + """
<body>
    <div data-role="page" data-url="{{"/"}}>
        <div role="main" class="ui-content centre">
            <br><br><br><br><br>
            <img src="images/logo.png" id="logo">
            <h1 id="l">WhoKnows</h1>
            <form action="" method="post" >
                <div class="ui-field-contain">
                    <input type="email" name="email" placeholder="Email" data-corners="true" autofocus required>
                    <input type="password" name="password" placeholder="Password" data-corners="true" required>
                    <input type="submit" value="Login" data-icon="lock" data-corners="true" >
                </div>
            </form>
            <a href="/Signup" class="ui-nodisc-icon ui-btn ui-shadow ui-corner-all ui-btn-b ui-btn-icon-left">Sign Up</a>
        </div>
    </div>
</body>
"""

#### Signup page with Register details and link to Login ####
html2 = header + """
<body>
    <div data-role="page" >
    
        <div data-role="header">
            <img src="images/brandName1.png">
        </div>
        
        <div role="main" class="ui-content centre">
            <h1 id="l">Signup</h1>
            <p id="l">It's free.</p><hr width="70%">
            <form action ="Signup" method="post">
                <div class="ui-field-contain">
                    <input type="text" name="username" placeholder="Username" data-corners="true" autofocus minlength="4" required>
                    <input type="email" name="email" placeholder="Email" data-corners="true" required>
                    <input type="text" name="password" placeholder="Password" data-corners="true" minlength="4" required><br>
                    <fieldset data-role="controlgroup" data-type="horizontal">
                        <legend>Interests:</legend>
                        <label for="restaurants">Restaurants</label>
                        <input type="radio" name="interests" id="restaurants" value="restaurants" checked="checked">
                        <label for="nightclub">Night Club</label>
                        <input type="radio" name="interests" id="nightclub" value="nightclub  ">
                        <label for="attractions">Attractions</label>
                        <input type="radio" name="interests" id="attractions" value="attractions"> 
                    </fieldset>
                    <input type="submit" value="Submit" data-corners="true" data-icon="check" onClick="goLogin()">
                </div>
            </form>
            <br><br><br><a href="/" class="ui-nodisc-icon ui-btn ui-shadow ui-corner-all ui-btn-b ui-icon-back ui-btn-icon-left" >Cancel</a>
        </div>
    </div>
</body>

"""

html3 = header + """
<body>
    <div data-role="page" data-url="{{"/Profile"}}>
        <div data-role="header">
            <img src="images/brandName1.png">
            <a href="/Settings" class="ui-btn ui-icon-gear ui-btn-right ui-corner-all ui-shadow ui-btn-icon-notext"></a>
        </div>
        <div data-role="main" class="ui-content centre">
            <h1 id="l">Welcome to your Profile, <b>%s</b></h1><br>
            <img src="images/Elephant.png" id="logo"><br>
            <p id="l"><b>%s </b>points</p>
            <a href="/askQuestion" class="ui-nodisc-icon ui-btn ui-corner-all ui-btn-a ui-btn-icon-left" >Ask a question</a>
            <a href="/answerQuestion" class="ui-nodisc-icon ui-btn ui-corner-all ui-btn-a ui-btn-icon-left" >Answer a question</a><br><br> 
            <a href="#popupDialog" data-rel="popup" data-position-to="window" data-transition="pop" class="ui-btn ui-corner-all ui-shadow ui-btn-b">Logout</a>
            <div data-role="popup" id="popupDialog" data-overlay-theme="a" data-theme="a" data-dismissible="false" style="max-width:400px;">
                <div data-role="header" data-theme="a">
                <h1>Logout?</h1>
                </div>
            <div role="main" class="ui-content">
                <h3 class="ui-title">Are you sure you want to Logout from your Profile?</h3>
                <a href="#" class="ui-btn ui-corner-all ui-shadow ui-btn-inline ui-btn-b" data-rel="back">Cancel</a>
                <a href="/Logout" class="ui-btn ui-corner-all ui-shadow ui-btn-inline ui-btn-b">Logout</a>
            </div>
        </div>
        </div>
    </div>
    
    
</body>

"""

html4 = header + """
<body>
    <div data-role="page">
        <div data-role="header" >
            <img src="images/brandName1.png">
        </div>
        <div data-role="main" class="ui-content centre" >
            <h1 id="l">Ask a Question</h1>
            <form method="post" action="/askQuestion">
                <fieldset class="ui-field-contain">
                    <p id="l">Area of Interest</p>
                    <select name="interest" id="interest">
                        <option value="restaurant">Restaurants</option>
                        <option value="attractions">Attractions</option>
                        <option value="nightclub">Night Clubs</option>
                    </select>
                </fieldset>
                <p id="l">What is your question?</p>
                <textarea name="question" id="question" data-corners="true" required></textarea><br><br>
                <input type="submit" value="Submit" data-corners="true" id="submit">
            </form>
            <button onClick="goBack()" class="ui-btn ui-icon-back ui-btn-icon-left ui-btn-b">Back</button>
        </div>
    </div>
</body>



"""

html5 = header + """
<body>
    <div data-role="page">
        <div data-role="header" >
            <img src="images/brandName1.png">
        </div>
        <div data-role="main" class="ui-content centre">
            <h1 id="l">Answer a Question</h1>
            <p><b><u> %s</u> </b>Asked a question about <b><u>%s</u></b>: <br> %s</p>
            <p><b><u> %s</u> </b>Answered: <br> %s </p>
            <form method="post" action="/answerQuestion">
                <input type="text" name="answer" placeholder="Answer" data-corners="true" autofocus required>
                
                <input type="hidden" name="id" id="id" value="%s"/>
                <input type="submit" value="Submit" data-corners="true" id="submit">
                
                
            </form>
            <button onClick="goBack()" class="ui-btn ui-icon-back ui-btn-icon-left ui-btn-b">Back</button>
        </div>
    </div>
</body>

"""

settings = header + """
<body>
    <div data-role="page" data-url="{{"/Settings"}}>
        <div data-role="header">
            <img src="images/brandName1.png">
        </div>
        <div data-role="main" class="ui-content centre">
            <h1 id="l"><b>%s's</b> Avatar Settings</h1><br>
            <img src="images/Elephant.png" id="logo"><br>
                <div class="ui-field-contain">
                    <label for="select-native-1"><b>Mood:</label>
                    <select name="select-native-1" id="select-native-1">
                        <option value="1">The 1st Option</option>
                        <option value="2">The 2nd Option</option>
                        <option value="3">The 3rd Option</option>
                        <option value="4">The 4th Option</option>
                    </select>
                </div>
                <div class="ui-field-contain">
                    <label for="select-native-1"><b>Accessories:</label>
                    <select name="select-native-1" id="select-native-1">
                        <option value="1">The 1st Option</option>
                        <option value="2">The 2nd Option</option>
                        <option value="3">The 3rd Option</option>
                        <option value="4">The 4th Option</option>
                    </select>
                </div>
                <div class="ui-field-contain">
                    <label for="select-native-1"><b>HairStyle:</label>
                    <select name="select-native-1" id="select-native-1">
                        <option value="1">The 1st Option</option>
                        <option value="2">The 2nd Option</option>
                        <option value="3">The 3rd Option</option>
                        <option value="4">The 4th Option</option>
                    </select>
                </div><br>
            <button onClick="#" class="ui-btn ui-icon-check ui-btn-icon-left">Apply Changes</button>
            <button onClick="goBack()" class="ui-btn ui-icon-back ui-btn-icon-left ui-btn-b">Back</button>
        </div>
    </div>
</body>


"""

#### Python Logic of the program ####
#### Main page with Login ####
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(html)
        
    def post(self):
        authenticate = False
        emailX = self.request.get('email')
        passwordX = self.request.get('password')
        
        session = get_current_session()
        data = Users.query()
        for j in data:
            if j.email == emailX and j.password == passwordX:
                auth = True
                
                if auth == True:
                    user = Users.query(Users.email == emailX)
                    for j in user:
                        session['username'] = j.username
                        session['email'] = j.email
                        session['interest'] = j.interests
                        session['points'] = j.points
                        self.redirect("/Profile")
                        
            if j.email != emailX and j.password != passwordX:
                self.redirect("/")
            
            


#### Signup Page ####
class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.write(html2)

    def post(self):
        usernameX = self.request.get('username')
        passwordX = self.request.get('password')
        emailX = self.request.get('email')
        interestsX = self.request.get('interests')
        
        u = Users(username=usernameX, password=passwordX, email=emailX, interests=interestsX, points=0)
        k = u.put()
        
        self.redirect("/")
        #Users(username=usernameX, password=passwordX, email=emailX, interests=interestsX, points=0).put()
        

#### Profile Page ####
class Profile(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        user = cgi.escape(session.get('username', ''), quote = True)
        mail = cgi.escape(session.get('email', ''), quote = True)
        interests = cgi.escape(session.get('interest', ''), quote = True)
        points = str(session.get('points', ''))

        self.response.write(html3 %(user, points))
        
        
#### Ask a Question Page ####
class askQuestion(webapp2.RequestHandler):
    def get(self):
        self.response.write(html4)
        
    def post(self):
        session = get_current_session()
        i1 = self.request.get('interest')
        q1 = self.request.get('question')
        mail = cgi.escape(session.get('email', ''), quote = True)
        
        Questions(question=q1, interest=i1, email=mail).put()
        time.sleep(1)
        self.response.write(script)
        self.redirect("/Profile")
        
#### Logout Page ####
class Logout(webapp2.RequestHandler):
    def get(self):
        while not delete_expired_sessions():
            pass
        
        time.sleep(1)
        self.response.write(script)
        self.redirect("/")
        
        
        
 #### Settings Page ####
class Settings(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        user = cgi.escape(session.get('username', ''), quote = True)
        self.response.write(settings %(user))
    
        
        
        
#### Answer a Question Page ####
class answerQuestion(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        i1 = cgi.escape(session.get('interest', ''), quote = True)
        e1 = self.request.get('email')
        
        data = Questions.query()
        entity = data.get()
        if entity is not None:
            a = ''
            b = ''
            c = ''
            d = ''
            e = ''

            for x in data:
                a = x.question
                b = str(x.key.id())
                c = x.answer
                d = x.email
                e = x.email2
                f = x.interest

            self.response.write(html5 %(d, f, a, e, c, b))
            
        if entity is None:
            time.sleep(1)
            self.redirect("/Profile")
        
    def post(self):
        session = get_current_session()
        mail = cgi.escape(session.get('email', ''), quote = True)
        id = self.request.get('id')
        answer = self.request.get('answer')
        logging.info('id:' + str(id))
        logging.info('answer: ' + str(answer))
        x = Questions.get_by_id(int(id))
        x.answer = answer
        x.email2 = mail
        x.put()
        
        time.sleep(1)
        self.redirect("/Profile")
        
        
        
#### NDB database Users ####
class Users(ndb.Model): 
    username = ndb.StringProperty()
    password = ndb.StringProperty()
    email = ndb.StringProperty()
    interests = ndb.StringProperty()
    points = ndb.IntegerProperty()

#### NDB database Questions ####
class Questions(ndb.Model): 
    question = ndb.StringProperty()
    interest = ndb.StringProperty()
    email = ndb.StringProperty()
    answer = ndb.StringProperty()
    email2 = ndb.StringProperty()

#### Controller ####
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Signup', Signup),
    ('/Profile', Profile),
    ('/askQuestion', askQuestion),
    ('/answerQuestion', answerQuestion),
    ('/Settings', Settings),
    ('/Logout', Logout)
], debug=True)
