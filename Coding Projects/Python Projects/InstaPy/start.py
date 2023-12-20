from instagram_bot import InstagramBot

insta_username = 'createurdeimagination'
insta_password = 'Icarus14!?'

# if you want to run this script on a server,
# simply add nogui=True to the InstagramBot() constructor
session = InstagramBot(username=insta_username,
                       password=insta_password, bypass_suspicious_attempt=True,
                       headless_browser=True)
session.login()

# set up all the settings
session.set_upper_follower_count(limit=2500)
session.set_do_comment(True, percentage=10)
session.set_comments(['aMEIzing!', 'So much fun!!', 'Nicey!'])
session.set_dont_include(['friend1', 'friend2', 'friend3'])
session.set_dont_like(['pizza', 'girl'])

# do the actual liking
session.like_by_tags(['natgeo', 'world'], amount=100)

# end the bot session
session.end()
