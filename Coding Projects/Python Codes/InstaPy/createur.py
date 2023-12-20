from instagram_bot import instagram_bot

#if you don't provide arguments, the script will look for INSTA_USER and INSTA_PW in the environment
session = instagram_bot(username='', password='')

"""Logging in"""
#logs you in with the specified username and password
session.login()

"""Comment util"""
#default enabled=True,  ~ every 4th image will be commented on
session.set_do_comment(enabled=True, percentage=35)
session.set_comments(['Awesome and simply amzaing work on your part! The light and atmosphere are catching!', 'This is indeed proper awesome photography', 'I indeed love your Images!', 'You have some really sublime Images here!', 'Simply stunning!', 'So awesome image and work!', 'Nice, I really like it'])

"""Follow util"""
#default enabled=False, follows ~ every 10th user from the images
session.set_do_follow(enabled=True, percentage=1)

"""Image Check with Image tagging api"""
#default enabled=True
#enables the checking with the clarifai api (image tagging)
#if secret and proj_id are not set, it will get the environment Variables
# 'Clarifai_SECRET' and 'CLARIFAI_ID'
session.set_use_clarifai(enabled=True, secret='k_G6bITL7lT6wlStO00bHefj2dgKJvBT4TGyhxH8', proj_id='createur')
#                                        ^
# ^If specified once, you don't need to add them again

session.set_use_clarifai(enabled=False)
session.set_use_clarifai(enabled=True) #<- will use the one from above

#uses the clarifai api to check if the image contains nsfw content
# Check out their homepage to see which tags there are -> won't comment on image
# (you won't do this on every single image or the 5000 free checks are wasted very fast)
session.clarifai_check_img_for(['nsfw'], comment=False) # !if no tags are set, use_clarifai will be False

#checks the image for keywords landscape and urban, if found, sets the comments possible comments
#to the given comments
session.clarifai_check_img_for(['goldenhour', 'urban'], comment=True, comments=['Exceptionell!', 'I like that atmosphere! This is really great captured light'])
session.clarifai_check_img_for(['mountains', 'landscape', 'beach','minimalism'], comment=True, comments=['So wonderful!!', 'Sublime!!!'])

"""Like util"""
#searches the description for the given words and won't
# like the image if one of the words are in there
session.set_dont_like(['food', 'eat', 'meal', 'selfie', 'cat', 'dog', 'car'])
#will ignore the don't like if the description contains
# one of the given words
session.set_ignore_if_contains(['urban', 'minimalism'])

"""Unfollow util"""
#will prevent commenting and unfollowing your good friends
session.set_dont_include(['musematschka', 'me_hamburg', 'vikingshipmuseum'])

"""Different tasks"""
# you can put in as much tags as you want, likes 100 of each tag
session.like_by_tags(['goldenhour', 'awesomeearth', 'longexposure', 'landscape', 'minimalism', 'earthlandscape', 'urban'], amount=100)

#get's the tags from the description and likes 100 images of each tag
session.like_from_image(url='www.instagram.com/p/BTbvD6Xg_12/', amount=100)

session.unfollow_users(amount=2) #unfollows 10 of the accounts your following -> instagram will only unfollow 10 before you'll be 'blocked
#  for 10 minutes' (if you enter a higher number than 10 it will unfollow 10, then wait 10 minutes and will continue then)

"""Ending the script"""
#clears all the cookies, deleting you password and all information from this session
session.end()
