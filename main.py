import webapp2
import re

page_header = """
    <html>
    <head>
        <title>User Sign-up</title>
        <style type="text/css">
            .error {
                color: red;
            }
            .label {
                text-align: right;
            }
        </style>
    </head>
    <body>
        <h1>
            <a href="/">User Sign-up</a>
        </h1>
"""

main_body = """
    <html>
    <head>
        <title>User Sign-up</title>
        <style type="text/css">
            .error {
                color: red;
            }
            .label {
                text-align: right;
            }
        </style>
    </head>
    <body>
        <h1>
            <a href="/">User Sign-up</a>
        </h1>
    <form method='post'>
        <table>
            <tr>
                <td class='label'>
                    Username:
                    </td>
                    <td>
                    <input type='text' name='username' value='%(username)s'>
                </td>
                <td class='error'>
                    %(error1)s
                </td>
            </tr>

            <tr>
                <td class='label'>
                    Password:
                </td>
                <td>
                    <input type='password' name='password' value=''>
                </td>
                <td class='error'>
                    %(error2)s
                </td>
            </tr>

            <tr>
                <td class='label'>
                    Verify Password:
                </td>
                <td>
                    <input type='password' name='verify' value=''>
                </td>
                <td class='error'>
                %(error3)s
                </td>
            </tr>

            <tr>
                <td class='label'>
                    Email (Optional):
                </td>
                <td>
                    <input type='text' name='email' value='%(email)s'>
                </td>
                <td class='error'>
                %(error4)s
                </td>
            </tr>
        </table>
        <input type='submit'>
    </form>
    </body>
    </html>
"""

page_footer = """
    </body>
    </html>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username='',password='', verify='', email='',error1='',error2='',error3='', error4=''):
        self.response.out.write(main_body % {'username' : username, 'password' : password,
                                               'verify' : verify, 'email' : email, 'error1' : error1,
                                               'error2' : error2, 'error3' : error3, 'error4' :error4 })

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        error = False
        error1 = ''
        error2 = ''
        error3 = ''
        error3 = ''
        error4 = ''

        if not valid_username(username):
            error1 = 'That is not a valid username'
            error = True

        if not valid_password(password):
            error2 = 'That is not a valid password'
            error = True

        elif password != verify:
            error3 = 'Your passwords did not match'
            error = True

        if not valid_email(email):
            error4 = 'That is not a valid email'
            error = True

        if error:
            self.write_form(username, password, verify, email, error1, error2, error3, error4)
        else:
            self.redirect('/welcome?username=%s' % username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        content = page_header + "Welcome, " + username + "!" + page_footer
        self.response.out.write(content)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
