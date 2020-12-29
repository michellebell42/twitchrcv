
from twitchAPI.pubsub import PubSub
from twitchAPI.twitch import Twitch
from pprint import pprint
from uuid import UUID
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import serial
import private_const
import time
from playsound import playsound

# Import Adafruit IO REST client.
from Adafruit_IO import Client, Feed

# music files - filenames must match files in the same folder as this code
raid_song = 'Zelda_Lost_Woods_Remix_Cut.mp3'
party_song = 'Animal_Crossing_remix_DJ_KK_Cut.mp3'
christmas_song = "jinglebellsremix.mp3"

# adafruit IO feed name to publish data to
aio_feed = 'ledfeed'

def callback_channel_points(uuid: UUID, data: dict):
    # print('got callback for UUID ' + str(uuid))
    # pprint(data)
    
    # get the title 
    title = data['data']['redemption']['reward']['title']

    # uncomment this if you want to retreive the username of the person who redeemed
    # user = data['data']['redemption']['user']['display_name']

    if title == "change LED color":
        # this reward has a user input field, retreive the input data
        user_input = data['data']['redemption']['user_input']
        print ("change color redeemed, input:", user_input)

        # send color data to adafruit IO
        aio.send_data(aio_feed, user_input)

    elif title == "party mode!!!":
        # send mode command to adafruit IO
        aio.send_data(aio_feed, "mparty")
        print("party mode redeemed")

        # code will pause until is song is complete
        playsound(party_song)
        
    elif title == "christmas mode!":
        # send mode command to adafruit IO
        aio.send_data(aio_feed, "mchristmas")
        print("christmas mode redeemed")

        # code will pause until is song is complete
        playsound(christmas_song)
    else:
        # other redemption, print and do nothing
        print ("other redemption:", title)


# Press the green triangle button on the top right of the VSCode window to run the script.


if __name__ == '__main__':
    
    print('~starting script~')

    # Create an instance of the REST client.
    aio = Client(private_const.ADAFRUIT_IO_USERNAME, private_const.ADAFRUIT_IO_KEY)
    feed = Feed(name="ledfeed")

    # create instance of twitch API
    twitch = Twitch(private_const.app_id, private_const.app_secret)
    twitch.authenticate_app([])

    # get ID of user
    user_info = twitch.get_users(logins=[private_const.username])
    user_id = user_info['data'][0]['id']

    # set up channel point redemption pubsub
    target_scope = [AuthScope.CHANNEL_READ_REDEMPTIONS]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    twitch.set_user_authentication(token, target_scope, refresh_token)

    pubsub = PubSub(twitch)
    pubsub.start()
    # you can either start listening before or after you started pubsub.

    print('~connected to twitch~')

    # listen to channel points. enter callback function when redemption occurs 
    uuid = pubsub.listen_channel_points(user_id, callback_channel_points)

    # two ways to end code: press ENTER or ctrl+c in terminal
    try:
        input('listening. press ENTER to close when done streaming...\n')
        
        # you do not need to unlisten to topics before stopping but you can listen and unlisten at any moment you want
        pubsub.unlisten(uuid)
        pubsub.stop()

        #dev.close()

        print('twitch pubsub stopped!')
    except KeyboardInterrupt:
        print(" run cancelled.")
        pubsub.unlisten(uuid)
        pubsub.stop()
        print('twitch pubsub stopped!')

