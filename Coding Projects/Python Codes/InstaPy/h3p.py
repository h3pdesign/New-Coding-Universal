from instapy import InstaPy

#if you don't provide arguments, the script will look for INSTA_USER and INSTA_PW in the environment
session = instagram_bot(username='h3palpha', password='Icarus14!?')

"""Logging in"""
#logs you in with the specified username and password
session.login()

"""Comment util"""
#default enabled=True,  ~ every 4th image will be commented on
session.set_do_comment(enabled=True, percentage=35)
session.set_comments(['Awesome', 'Really Cool', 'I love your Images', 'You have some sublime Images here!', 'Simply stunning', 'So awesome', 'Nice, I really like it'])

"""Follow util"""
#default enabled=False, follows ~ every 10th user from the images
session.set_do_follow(enabled=True, percentage=10)

"""Image Check with Image tagging api"""
#default enabled=True
#enables the checking with the clarifai api (image tagging)
#if secret and proj_id are not set, it will get the environment Variables
# 'Clarifai_SECRET' and 'CLARIFAI_ID'
session.set_use_clarifai(enabled=True, secret='d7GfOyk0Eb6PwuPeWj2F3kPbA_oGvxQGOGgOcWRQ', proj_id='createurb&w')
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
session.clarifai_check_img_for(['architecture_view', 'blackandwhite'], comment=True, comments=['Exceptionell!', 'I like that atmosphere! This is really great captured light'])
session.clarifai_check_img_for(['blackandwhite', 'urbanarchitecture', 'schwarzweiss','minimalism'], comment=True, comments=['So wonderful!!', 'Sublime!!!'])

"""Like util"""
#searches the description for the given words and won't
# like the image if one of the words are in there
session.set_dont_like(['food', 'eat', 'meal', 'selfie', 'cat', 'dog'])
#will ignore the don't like if the description contains
# one of the given words
session.set_ignore_if_contains(['glutenfree', 'french', 'tasty', 'cat', 'dog'])

"""Unfollow util"""
#will prevent commenting and unfollowing your good friends
session.set_dont_include(['nicoleashley'])

"""Different tasks"""
# you can put in as much tags as you want, likes 100 of each tag
session.like_by_tags(['blackandwhite', 'blackandwhitephotography', 'blacknwhite', 'blacknwhiteperfection', 'schwarzweiss'], amount=100)

#get's the tags from the description and likes 100 images of each tag
session.like_from_image(url='www.instagram.com/p/BTbvD6Xg_12/', amount=100)

session.unfollow_users(amount=0) #unfollows 10 of the accounts your following -> instagram will only unfollow 10 before you'll be 'blocked
#  for 10 minutes' (if you enter a higher number than 10 it will unfollow 10, then wait 10 minutes and will continue then)

"""Ending the script"""
#clears all the cookies, deleting you password and all information from this session
session.end()
