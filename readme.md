# Twitch Channel Point / Adafruit IO Utility
Listens to Twitch channel point redemptions and sends messages to Adafruit IO 

## Set up python environment

1. Do the following steps from this link: https://code.visualstudio.com/docs/python/python-tutorial
- "Install Visual Studio Code and the Python Extension" section
- "Install a Python interpreter" / Windows section. IMPORTANT: for some reason this code seems to only work on Python 3.7, so install that one
2. Make a folder somewhere in your Documents for this code 
3. In VSCode, use File > Open Folder to select and open the folder you just made
4. Select View > Command Pallette (or use Ctrl+Shift+P), then start typing "Python: Select Interpreter" and select it 
5. This should show a list of your python interpreters at the top of the window, select the Python 3.7 option.
- Note: if a little box pops up on the bottom right at any point that says "Linter pylint is not installed.", click the install button
6. Open the 'main.py' file and the 'private_constants.py' file
7. If you don't see a tab on the bottom of the window that says "Terminal", open one with Terminal > New Terminal 
8. At the terminal, install the necessary libraries by entering the following one at a time:
- pip install twitchAPI
- pip install playsound
- pip install adafruit-io
- (i think that's it??? if you have errors on the "from" lines, i may have missed one)

## Set up twitch extension for authentication and Adafruit IO
1. go to dev.twitch.tv/console
2. login with twitch 
3. in the Applications panel, click "Register your Application" button
4. name and category can be whatever you want, OAuth Redirect URLs must be http://localhost:17563 
5. this will give you a Client ID and a Client Secret. IMPORTANT: keep the Client Secret somewhere safe. You will not be able to access this again. If you lose it, you can generate a new one but it will need to be updated wherever you use it (i.e. in the code).
6. Rename private_const_template.py to private_const.py
7. In private_const.py file: (NOTE: do not remove the ''s)
- replace YOUR_APP_ID with the Twitch application Client ID
- YOUR_APP_SECRET with the Twitch application Client Secret 
- YOUR_TWITCH_USERNAME with your Twitch username
- YOUR_ADAFRUIT_IO_KEY with your Adafruit IO key
- YOUR_ADAFRUIT_IO_USERNAME with your Adafruit IO username

## Running/testing!
1. Click the green triangle button in the top right of the VSCode window
2. A window that says "Thanks for Authenticating with pyTwitchAPI! You may now close this page." should pop up in your web browser. This means your script is now authenticated with Twitch and you can close the window. 
3. Test by going into your own chat (dashboard.twitch.tv) and redeeming a channel point reward. The terminal in VSCode should show a printout of the redemption. If it's a redemption set up with Adafruit IO, you should see the appropriate message appear in your feed.
- NOTE: your redemption titles must be equivalent to the titles in the code. You can change the code to match.
4. When done, hit the ENTER key or ctrl+c in the terminal window to end the run!

## Editing the script

To edit the channel point rewards, change/add/remove cases to the if/elif statement in the callback_channel_points function. title == "YOUR_REDEMPTION" where the channel point redemption name on Twitch must match the YOUR_REDEMPTION field exactly. 

To edit/add sounds: pick a sound you want (I download mine as .mp3 clips from stream-safe youtube videos). mp3s definitely work, I don't know if .wav or other types will work. Put the clip in the same folder as this code. Set the title of the file to a variable your_song_variable = 'your_song_filename.mp3'. Use playsound(your_song_variable) to play.
