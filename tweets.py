import tweepy

def get_keys():

	with open('twitterdevkeys.txt', 'r') as f:
		txt = f.readlines()

	elements = [a.split(',') for a in txt]
	keys = {}
	for a in elements:
		keys[a[0]] = a[1].rstrip()
		
	return keys

def authorise(keys):	
	auth = tweepy.OAuthHandler(keys['API key'], keys['API key secret'])
	auth.set_access_token(keys['Access token'], keys['Access token secret'])

	api = tweepy.API(auth)

	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")

def to_ordinal(cardinal):
    suffices = ["th", "st", "nd", "rd"]

    if cardinal % 10 in [1, 2, 3] and cardinal not in [11, 12, 13]:
        return suffices[cardinal % 10]
    else:
        return suffices[0]

def get_time_str(time):
    string = f"{time.hour}:{time.minute} on {time.day}{to_ordinal(time.day):s} {time.strftime('%b %Y')}"
    return string

def thank(s):
    ack_str = '. Data from @JHUSystems'
    return s + ack_str

def tweet_pic_with_thanks(fname, msg, time_now, reply_id=None):
    time_str = get_time_str(time_now)
    message_with_time = msg + f' at {time_str}'
    full_message = thank(message_with_time)
    
    if reply_id is None:
        t = api.update_with_media(fname, full_message)
    else:
        t = api.update_with_media(fname, '@a_good_brew' + full_message, reply_id)
    return t

def tweet():
	time_now = datetime.datetime.now()
	time_str = get_time_str(time_now)
	user = '@a_good_brew' + ' '
	
	t1 = tweet_pic_with_thanks('deaths.png', '#COVID19 death stats', time_now)
	t2 = tweet_pic_with_thanks('deaths_doubling_times.png', '#COVID19 death doubling times', time_now)
	t3 = tweet_pic_with_thanks('deaths_days_to_n.png', '#COVID19 death predictions', time_now)
	t4 = tweet_pic_with_thanks('confirmed_days_to_n.png', '#COVID19 case number predictions', time_now)
