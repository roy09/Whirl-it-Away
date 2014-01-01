import fbconsole
import pickle

#getting authorization
def login():
	fbconsole.AUTH_SCOPE = ['publish_stream', 'read_stream', 'status_update']
	fbconsole.authenticate()

#setting a status update
def update_status(update):
	status = fbconsole.post('/me/feed', {'message':update})
	
	#print status

	#last status update id
	#status = status[10:-2]
	#print type(status)

#last 5 posts
def get_posts():
	last5_data = fbconsole.fql("SELECT status_id, message from status WHERE uid = me() LIMIT 5")
	print last5_data
	last5_status_id = []
	last5_status_message = []

	for x in range(0,5):
		last5_status_id.append(str(last5_data[0]["status_id"])[:-1])
		last5_status_message.append(last5_data[0]["message"])
	return last5_status_message


#getting the comments, given the status id
def get_comments(post_id):
	comment_data = fbconsole.fql("SELECT text FROM comment WHERE post_id = %s" %(post_id))
	no_of_comments = len(comment_data)

	comments = []
	for y in range(0, no_of_comments - 1):
		comments.append(comment_data[y]['text'])
	
	return comments

#getting the comments, given the status id
def get_comments(post_id):
	comment_data = fbconsole.fql("SELECT text FROM comment WHERE post_id = %s" %(post_id))
	no_of_comments = len(comment_data)

	comments = []
	for y in range(0, no_of_comments - 1):
		comments.append(comment_data[y]['text'])
	
	return comments

def get_name(id):
	userid_data = fbconsole.fql("SELECT name FROM profile WHERE id = %s" %(id))
	print userid_data[0]["name"]
	
def get_comments_poster(post_id):
	comment_data = fbconsole.fql("SELECT fromid FROM comment WHERE post_id = %s" %(post_id))
	no_of_comments = len(comment_data)

	posters = []
	for z in range(0, no_of_comments):
		posters.append(get_name(str(comment_data[z]['fromid'])))
		
	return posters


#getting the username from the uid
#username = fbconsole.fql("SELECT name FROM profile WHERE id = 100001853351818")
#print username


#print type(username)
#pickle.dump(data, open("newdata.p", "wb"))

login()
print get_posts()
