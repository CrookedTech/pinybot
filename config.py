# This file holds pinylib's configuration.
# Use a prefix, if you plan on adding your own.
# Settings info https://github.com/nortxort/pinylib/wiki/Settings

# Set the bot to run without allowing any input into the console.
ON_SERVER = False

# Automatically use the information provided below to connect.
AUTO_INFO = False
# The room to connect to.
ROOM_NAME = ''
# Nickname to use in a room.
NICK_NAME = ''
# Tinychat account.
ACCOUNT = ''
# Password for account
PASSWORD = ''

# The swf version that tinychat is currently using.
SWF_VERSION = '0675'
# Log chat messages and events.
CHAT_LOGGING = False
# Show additional info/errors in console.
DEBUG_MODE = False
# Log debug info to file.
DEBUG_TO_FILE = False
# Logging level for the debug file.
DEBUG_LEVEL = 30
# Use colors for the console.
CONSOLE_COLORS = True
# Enable auto job (recommended)
ENABLE_AUTO_JOB = True
# Time format.
USE_24HOUR = True
# Reset the run time after a reconnect.
RESET_INIT_TIME = False
# Reconnect delay in seconds.
RECONNECT_DELAY = 60
# Auto job interval in seconds.
AUTO_JOB_INTERVAL = 300
# The name of pinylib's debug log file.
DEBUG_FILE_NAME = 'pinylib_debug.log'
# The path to the config folder.
CONFIG_PATH = 'rooms/'

# This section holds the bot's configuration.

# The prefix used for bot commands.
B_PREFIX = '!'
# Bot controller key.
B_KEY = 'light'
# Bot super key.
B_SUPER_KEY = 'energy'
# Public commands enabled.
B_PUBLIC_CMD = True
# Greet user when joining.
B_GREET = True
# The message to greet the user with in the public chat-box.
B_GREET_MESSAGE = ''
# Greet user with a private message.
B_GREET_PRIVATE = False
# The message to greet the user with in the private chat-box
B_GREET_PRIVATE_MESSAGE = ''
# Greet users who broadcast their camera/microphone.
B_GREET_BROADCAST = False
# The message to greet the broadcasting users with in the chat-box.
B_GREET_BROADCAST_MESSAGE = ''
# Allow newuser to join the room.
B_ALLOW_NEWUSERS = True
# Allow broadcasting.
B_ALLOW_BROADCASTS = True
# Allow guests to enter the room.
B_ALLOW_GUESTS = True
# Allow lurkers to enter the room.
B_ALLOW_LURKERS = True
# Allow guest nicks.
B_ALLOW_GUESTS_NICKS = False
# Forgive auto bans.
B_FORGIVE_AUTO_BANS = True
# The file name of nick bans.
B_NICK_BANS_FILE_NAME = 'nick_bans.txt'
# A list of all the nick bans.
B_NICK_BANS = []
# The file name of account bans.
B_ACCOUNT_BANS_FILE_NAME = 'account_bans.txt'
# A list of account bans.
B_ACCOUNT_BANS = []
# The file name of string(words) bans.
B_STRING_BANS_FILE_NAME = 'string_bans.txt'
# The file name of the blocked media.
# B_BLOCKED_MEDIA_FILE_NAME = 'blocked_media.txt'
# A list of the blocked media.
# B_BLOCKED_MEDIA = []
# A list of string bans.
B_STRING_BANS = []
# The name of the bot's debug file.
B_DEBUG_FILE_NAME = 'tinybot_debug.log'

#
ROOM_EVENT_INFORMATION = True

##
#
B_SANITIZE_MESSAGES = True
#
B_UNICODE_SPAM = True
#
B_TINYCHAT_ROOM_LINK_SPAM = True
#
B_CAPITAL_CHARACTER_LIMIT = False
#
B_CAPITAL_CHARACTER_LIMIT_LENGTH = 50

##
#
B_BAN_MOBILES = False
#
B_AUTO_CLOSE = False
#
B_ALLOW_SNAPSHOTS = True
#
B_BOT_REPORT_KICK = False

##
#
B_AUTO_GREENROOM = False
#
B_AUTO_URL_MODE = True
#
B_CLEVERBOT = True
#
B_INSTANT_CLEVERBOT = True

##
#
B_MEDIA_LIMIT_PUBLIC = False
#
B_MEDIA_LIMIT_PLAYLIST = False
#
B_MEDIA_LIMIT_DURATION = 0
#
B_PLAYLIST_MODE = True
#
B_PUBLIC_MEDIA_MODE = False
#
B_RADIO_CAPITAL_FM_AUTO_PLAY = False
