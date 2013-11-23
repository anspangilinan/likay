# Python Imports
import facebook

# Django Imports
from django.conf import settings


def share_to_facebook():
	"""
	This will automatically post to facebook as likayph
	"""
	access_token = settings.POST_ACCESS_TOKEN

	facebook_graph = facebook.GraphAPI(access_token)
	
	attach = {
		'name':'Test post',
		'link':'likay.ingenuity.ph',
		'caption':'test',
		'description':'blah3'
	}

	response = facebook_graph.put_wall_post('', attachment=attach, profile_id=settings.FACEBOOK_PAGE_ID)
