import kivy
kivy.require('1.0.6')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.checkbox import CheckBox
import fbconsole
from twitter import *
import os
import pickle

class MyApp(App):
	
	def build(self):
		global root
		root = BoxLayout(orientation="vertical")
		
		#some art/whatsoever
		root.add_widget(Label(text="Whirl it Away"))
		
		#enable Facebook
		fb = Button(text="Login to Facebook")
		fb.bind(on_press = self.login_facebook)
		root.add_widget(fb)
		
		#enable Twitter
		twit = Button(text="Login to Twitter")
		twit.bind(on_press = self.login_twitter)
		root.add_widget(twit)
		
		login_button_area = AnchorLayout(anchor_x = 'right', anchor_y='bottom')
		login_button = Button(text="Let's go")
		login_button.bind(on_press = self.login)
		login_button_area.add_widget(login_button)
		
		
		root.add_widget(login_button_area)
		
		return root
	
	def on_enter(instance, value):
		print ('User pressed enter in', value.text)

	def login_facebook(self, instance):
		fbconsole.AUTH_SCOPE = ['publish_stream', 'read_stream', 'status_update']
		fbconsole.authenticate()
		
	def login_twitter(self, instance):
		print "we are here"
		CONSUMER_KEY = 	"cwSZjDHLZ9PgJrdeQjtLfQ"
		CONSUMER_SECRET = "W7TrsdB7fYgOY3wT6wIZjBblxrC87cUA1pP4QagS1Qc"

		MY_TWITTER_CREDS = os.path.expanduser('my_app_credentials')

		temp1 = oauth_dance("msgB", CONSUMER_KEY, CONSUMER_SECRET, MY_TWITTER_CREDS)
		oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)
		global twitter
		twitter = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))
		
	
	def login(self, instance):
		root.clear_widgets()
		self.build2()
	
	def build2(self):
		textinput = TextInput(text='Type the broadcast message here', multiline=False)
		textinput.bind(on_text_validate=self.broadcast_now)
		root.add_widget(textinput)
		
		enable_fb = AnchorLayout(anchor_x = 'right', anchor_y='bottom')
		box1 = BoxLayout(orientation="vertical")
		tick_fb = Label(text="fb")
		box1.add_widget(tick_fb)
		post_to_facebook = CheckBox()
		post_to_facebook.bind(active=self.on_facebook_active)
		box1.add_widget(post_to_facebook)
		enable_fb.add_widget(box1)
		
		enable_twit = AnchorLayout(anchor_x = 'right', anchor_y='bottom')
		box1 = BoxLayout(orientation="vertical")
		tick_fb = Label(text="twtr")
		box1.add_widget(tick_fb)
		post_to_facebook = CheckBox()
		post_to_facebook.bind(active=self.on_twitter_active)
		box1.add_widget(post_to_facebook)
		enable_twit.add_widget(box1)
		
		post_root = BoxLayout(orientation="horizontal")
		post_root.add_widget(enable_fb)
		post_root.add_widget(enable_twit)
		root.add_widget(post_root)
		
		button = Button(text="Submit")
		button.bind(on_press = self.broadcast_now)
		root.add_widget(button)
		
		#Facebook posts
		posts = BoxLayout(orientation="horizontal")
		fb_posts = BoxLayout(orientation="vertical")
		fb_posts_header = Label(text="Status Messages")
		fb_posts.add_widget(fb_posts_header)
		fb_posts.add_widget(self.build3(fb_posts))
		posts.add_widget(fb_posts)
		
		#Twitter posts
		twit_posts = BoxLayout(orientation="vertical")
		twit_posts_header = Label(text="Tweets")
		twit_posts.add_widget(twit_posts_header)
		twit_posts.add_widget(self.build4())
		posts.add_widget(twit_posts)
		
		root.add_widget(posts)
		
	def build3(self, child):
		last5_data = fbconsole.fql("SELECT status_id, message from status WHERE uid = me() LIMIT 5")
		last5_status_id = []
		last5_status_message = []

		for x in range(0,5):
			last5_status_id.append(str(last5_data[x]["status_id"])[:-1])
			last5_status_message.append(last5_data[x]["message"])
		
		posts = last5_status_message
		subroot = BoxLayout(orientation="vertical")
		for x in range(0,5):
			indv_post = Button(text=posts[x])
			subroot.add_widget(indv_post)
			
		return subroot
		
		
	def build4(self):
		x = twitter.statuses.user_timeline(count = 5)
		tweets = []

		for y in range(0,5):
			tweets.append(x[y]['text'])
			
		subroot = BoxLayout(orientation="vertical")
		for x in range(0,5):
			indv_post = Button(text=tweets[x])
			subroot.add_widget(indv_post)
		return subroot
		
	def on_enter(instance, value):
		print ("User pressed enter in", str(value))
	
	def on_facebook_active(checkbox, value, sth):
		if value:
			global fb_on
			fb_on = True
		else:
			global fb_on
			fb_on = False
	
	def on_twitter_active(checkbox, value, sth):
		if value:
			global twit_on
			twit_on = True
		else:
			global twit_on
			twit_on = False
			
	def broadcast_now(self, value):
		update = root.children[3].text
		if fb_on:
			try:
				fbconsole.post('/me/feed', {'message':update})
			except:
				print "Error while posting to FB"
		
		if twit_on:
			try:
				twitter.statuses.update(status=update)
			except:
				print "Error while psoting to Twitter"
				
			

		
	 
	
	def tester(instance, value):
		print "in"

if __name__ == '__main__':
	MyApp().run()
