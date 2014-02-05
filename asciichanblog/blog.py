import os
import re # importing regular expressions
import webapp2 # standard handler 
import jinja2 # allows for template implementation and variable calling

from google.appengine.ext import db # importing google app engine & db

template_dir = os.path.join(os.path.dirname(__file__), 'templates') 
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True) 

"""sets the path of the templetes and also where the jinja enviroment is
it also is set true for html escaping"""

class baseHandler(webapp2.RequestHandler): 
  
  """ super class """
  
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw) 
    
    """ Taking the text from a given attribute {{value}} and then putting
    the string into a database with **kw(keywords) and writing it back
    out"""
  
  def render_str(self, template, **params): 
    t = jinja_env.get_template(template)    
    return t.render(params)                 
  
  """ Enviroment of jinja is loaded and renders out a given file from
  a set templete folder. t.render then returns any kw recieved which is
  called from an action below"""
  
  def render(self, template, **kw): 
    self.response.out.write(self.render_str(template, **kw))
    #needed self.render as it was not a global name
    
  """ Rendering out procedure, which combines webapp 2 and jinja2
  this is writing out the keywords, but also calling the render_str
  function (this allows for the templates folder to be used"""
  
class Eric(db.Model):
  title = db.StringProperty(required = True)
  # Title field set to String, with constrain that it has no instance without
  # a title
  post = db.TextProperty(required = True)
  # Post field which has a text property as it adds more than 500 characters
  created = db.DateTimeProperty(auto_now_add = True)
  # adds date and time, which is inputed with the auto set the current time
  
  
class MainPage(baseHandler):
  
  def render_front(self, title="", post="", error=""):
    jane = db.GqlQuery("SELECT * FROM Eric "
                        "ORDER BY created DESC")
    self.render("blog.html", title=title, post=post, error=error, jane=jane)
  
  """ sending in empty variables, which will be remembered, when the
  user types in information and it is wrong"""
    
    
  
  def get(self):
    #self.render("blog.html") - replaced by new def
    self.render_front()
    
  """ this sends and recieves the request of the html file 
  displays it!"""
    
  def post(self):
    title = self.request.get("title")
    post = self.request.get("post")
    
    if title and post:
      #self.write("Thanks for Posting!")
      p = Eric(title = title, post = post)
      # will return a blank form 
      p.put()
      # This will place new article to the bottom of our page
      
      self.redirect("/")
      # will direct/refresh the main page for new items
    else:
      error = "I need both a title and a post, dude!"
      #self.render("blog.html", error = error) - replaced by new def
      self.render_front(title, post, error = error)
      # information from post is now passed back to render
    
  """ sending the information set by the user in the title and post
  sections of my html. Sending a get from the server and posting it
  
  Also an error checking was set, if title and text don't have inputs
  then write a value which has been set"""
  
  
  
  
  
  
app = webapp2.WSGIApplication([('/', MainPage)],debug=True)