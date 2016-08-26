#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
import re
import copy


form = """
<!DOCTYPE html>

<html>
    <head>
        <title>Sign Up</title>
        <style type="text/css">
            .label {text-align: left}
            .error {
                color: red;
            }
        </style>

    </head>

    <body>
        <h1>Signup</h1>
        <form method="post">
            <table>
                <tr>
                    <td class="label">
                        Username
                    </td>
                    <td>
                        <input type="text" name="username" value="%(username)s">
                    </td>
                    <td class="error">
                        %(nameerror)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        <span>Password</span>
                    </td>
                    <td>
                        <input type="password" name="password" value="">
                    </td>
                    <td class="error">
                        %(passworderror)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Verify password
                    </td>
                    <td>
                        <input type="password" name="verify" value="">
                    </td>
                    <td class="error">
                        %(verifyerror)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        Email (optional)
                    </td>
                    <td>
                        <input type="text" name="email" value="%(email)s">
                    </td>
                    <td class="error">
                        %(emailerror)s
                    </td>
                </tr>
            </table>

            <input type="submit">
        </form>
    </body>

</html>
"""

welcomepage = """
<html>
    <head>
        <title>Welcome</title>
    </head>

    <body>
        <h2>Welcome, %s!</h2>
    </body>
</html>
"""

nameerror = "That's not a valid username."
passworderror = "That wasn't a valid password."
verifyerror = "Your passwords didn't match."
emailerror = "That's not a valid email."

infolist = {'username':'',
    'nameerror': '',
    'passworderror':'',
    'verifyerror':'',
    'email':'',
    'emailerror':''}

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form % infolist)

    def post(self):
        infolist1 = copy.deepcopy(infolist)
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        infolist1['username'] = username
        infolist1['email'] = email

        ok = True
        if not self.valid_username(username):
            infolist1['nameerror'] = nameerror
            ok = False
        if not self.valid_password(password):
            infolist1['passworderror'] = passworderror
            ok = False
        if not self.valid_verify(password,verify):
            infolist1['verifyerror'] = verifyerror
            ok = False
        if email and not self.valid_email(email):
            infolist1['emailerror'] = emailerror
            ok = False

        if ok:
            self.redirect('/welcome?username=' + username)
        else:
            self.response.write(form % infolist1)



    def valid_username(self,username):
        USER_RE = re.compile("^[a-zA-Z0-9_-]{3,20}$")
        return USER_RE.match(username)

    def valid_password(self,password):
        PASSWORD_RE = re.compile("^.{3,20}$")
        return PASSWORD_RE.match(password)

    def valid_verify(self,password,verify):
        return password == verify

    def valid_email(self,email):
        EMAIL_RE = re.compile("^[\S]+@[\S]+\.[\S]+$")
        return EMAIL_RE.match(email)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.write(welcomepage % username)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome',WelcomeHandler)
], debug=True)
