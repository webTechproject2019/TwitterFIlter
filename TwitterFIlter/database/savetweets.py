from __future__ import print_function
import tweepy
import json
import MySQLdb 
from dateutil import parser

WORDS = ['#bigdata', '#AI', '#datascience', '#machinelearning', '#ml', '#iot']


ACCESS_TOKEN = '1111425621656252416-ZuJOxl3GkKyb3NXKi3DJub1XSxwLeV'
ACCESS_SECRET = 'sOIyBGr93FGxO4eP1ZAr092bMUqK5QwBaT8r2kwwfmLim'
CONSUMER_KEY = 'Bq8L7AYhWdovkEHrxId8vxVG7'
CONSUMER_SECRET = 'NYDkINrS9l4s93eFWuj0XcxMWHifinmt4l1P4MW4l9VA5nJpaG'

HOST = "localhost"
USER = "id9394687_webtech"
PASSWD = "Project2019"
DATABASE = "id9394687_webtechdb"

# This function takes the 'created_at', 'text', 'screen_name' and 'tweet_id' and stores it
# into a MySQL database
def store_data(created_at, text, screen_name, tweet_id):
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DATABASE, charset="utf8")
    cursor = db.cursor()
    insert_query = "INSERT INTO twitter (tweet_id, screen_name, created_at, text) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (tweet_id, screen_name, created_at, text))
    db.commit()
    cursor.close()
    db.close()
    return

class StreamListener(tweepy.StreamListener):    
    #This is a class provided by tweepy to access the Twitter Streaming API. 

    def on_connect(self):
        # Called initially to connect to the Streaming API
        print("You are now connected to the streaming API.")
 
    def on_error(self, status_code):
        # On error - if an error occurs, display the error / status code
        print('An Error has occured: ' + repr(status_code))
        return False
 
    def on_data(self, data):
       
        try:
           
            datajson = json.loads(data)
            
            
            text = datajson['text']
            screen_name = datajson['user']['screen_name']
            tweet_id = datajson['id']
            created_at = parser.parse(datajson['created_at']) 

            
            print("Tweet collected at " + str(created_at))
            
            
            store_data(created_at, text, screen_name, tweet_id)
        
        except Exception as e:
           print(e)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True)) 
streamer = tweepy.Stream(auth=auth, listener=listener)
print("Tracking: " + str(WORDS))
streamer.filter(track=WORDS)