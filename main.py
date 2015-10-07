import datetime
import logging
import os
import webapp2

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.api import mail

def render_template(handler, templatename, templatevalues={}):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)


def get_user_email():
  result = None
  user = users.get_current_user()
  if user:
    result = user.email()
  return result


class MainPageHandler(webapp2.RequestHandler):
  def get(self):
    email = get_user_email()
    if email:
      comment = self.request.get('comment1')

    page_params = {
      'user_email': email,
      'login_url': users.create_login_url(),
      'logout_url': users.create_logout_url('/')
    }
    render_template(self, 'index.html', page_params)

class ContactHandler(webapp2.RequestHandler):
	def post(self):
		name = "Name: " + self.request.get('name') + "\n"
		email = "Email: " + self.request.get('email') + "\n"
		comment = "Feedback: " + self.request.get('comment') + "\n"
		comment = name + email + comment
		admin_emails = ["boni1331@gmail.com", "JosephDMcclain@gmail.com", "matthewrlobrien@gmail.com", "thorff1@gmail.com"]
		if mail.is_email_valid(email):
			for admin in admin_emails:		
				message = mail.EmailMessage(
					sender=admin,
					subject="Feedback",
					to=admin,
					body=comment)
				message.send()			
		self.redirect('/')


mappings = [
  ('/', MainPageHandler),
  ('/contact', ContactHandler)
]
app = webapp2.WSGIApplication(mappings, debug=True)