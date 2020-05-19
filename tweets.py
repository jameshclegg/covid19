import tweepy
import datetime
import os
import pytz

TZ = pytz.timezone('Europe/London')

def get_keys():
	
	path_to_keys = os.path.join('..', '..', 'twitterdevkeys.txt')
	with open(path_to_keys, 'r') as f:
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
		
	return api

def to_ordinal(cardinal):
    suffices = ["th", "st", "nd", "rd"]

    if cardinal % 10 in [1, 2, 3] and cardinal not in [11, 12, 13]:
        return suffices[cardinal % 10]
    else:
        return suffices[0]

def get_time_str(time):
	clock_time = time.strftime('%H:%M %Z on ')
	month_year = time.strftime('%b %Y')
	string = clock_time + f"{time.day}{to_ordinal(time.day):s} " + month_year
	return string

def thank(s):
    ack_str = '. Data from @JHUSystems'
    return s + ack_str

def tweet(api, folder_name, test=False):
	time_now = datetime.datetime.now(TZ)
	time_str = get_time_str(time_now)
	user = '@a_good_brew' + ' '
	
	def tweet_pic_with_thanks(fname, msg, reply_id=None):
		time_str = get_time_str(time_now)
		message_with_time = msg + f' at {time_str}'
		full_message = thank(message_with_time)
		
		path_to_pic = os.path.join(folder_name, fname)
		
		if test:
			print(full_message)
		else:
			if reply_id is None:
				t = api.update_with_media(path_to_pic, full_message)
			else:
				t = api.update_with_media(path_to_pic, '@a_good_brew' + full_message, reply_id)
			return t

	t1 = tweet_pic_with_thanks('deaths.png', '#COVID19 death stats', time_now)
	t2 = tweet_pic_with_thanks('confirmed.png', '#COVID19 confirmed cases', time_now)
	#t2 = tweet_pic_with_thanks('deaths_doubling_times.png', '#COVID19 death doubling times', time_now)
	#t3 = tweet_pic_with_thanks('deaths_days_to_n.png', '#COVID19 death predictions', time_now)
	#t4 = tweet_pic_with_thanks('confirmed_days_to_n.png', '#COVID19 case number predictions', time_now)

def initialise_and_tweet(folder_name):
	
	keys = get_keys()
	api = authorise(keys)
	
	tweet(api, folder_name)


def main():
	tweet(None, '2020-03-25', test=True)
	
if __name__ == "__main__":
	main()
