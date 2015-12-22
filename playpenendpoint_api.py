"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import logging
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

WEB_CLIENT_ID = '255310283450-o8dbs2vq1p2gdqspb79fp05a9dtpl304.apps.googleusercontent.com'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'PlaypenEndpoint' #This is used by the underlying ProtoRpc when creating names for the ProtoRPC messages you create. This package name will show up as a prefix to your message class names in the discovery doc and client libraries

# message classes to be used in the requests and responses
class Greeting(messages.Message):
  """Greeting that stores a message."""
  message = messages.StringField(1)


class GreetingCollection(messages.Message):
  """Collection of Greetings."""
  items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world app public api response for appversion 2!'),
    Greeting(message='goodbye world public api response for appversion 2!'),
])

#we are adding an API named playpenEndpoint that has two methods serving GET requests, one that returns all Greetings and one that returns only the specified greeting
@endpoints.api(name='playpenEndpoint', version='v1', 
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                     IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class PlaypenEndpointApi(remote.Service):
  """PlaypenEndpointApi API v1."""

 

 
  
  MULTIPLY_METHOD_RESOURCE = endpoints.ResourceContainer(
       Greeting,
       times=messages.IntegerField(2, variant=messages.Variant.INT32,
                                required=True))

  @endpoints.method(MULTIPLY_METHOD_RESOURCE, Greeting,
                path='hellogreeting/{times}', http_method='POST',
                name='greetings.multiply')
  def greetings_multiply(self, request):
       logging.info("GET greetings.multiply")
       return Greeting(message=request.message * request.times)    

  @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='hellogreeting', http_method='GET',
                      name='greetings.listGreeting')
  def greetings_list(self, unused_request):
        logging.info("GET greetings.listGreeting")
        return STORED_GREETINGS
  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  @endpoints.method(ID_RESOURCE, Greeting,
                    path='hellogreeting/{id}', http_method='GET',
                    name='greetings.getGreeting')
  def greeting_get(self, request):
    try:
      logging.info("GET greetings.getGreeting")
      return STORED_GREETINGS.items[request.id]
    except (IndexError, TypeError):
      raise endpoints.NotFoundException('Greeting %s not found.' %
                                        (request.id,))
    
  @endpoints.method(message_types.VoidMessage, Greeting,
                  path='authed', http_method='POST',
                  name='greetings.authed')
  def greeting_authed(self, request):
    current_user = endpoints.get_current_user()
    email = (current_user.email() if current_user is not None
           else 'Anonymous')
    return Greeting(message='hello %s' % (email,))

#start service API classes

#Community classes
class Community(messages.Message):
  """Coummity that store name."""
  description = messages.StringField(1)
  id = messages.StringField(2)


class CommunityCollection(messages.Message):
  """Collection of Communities."""
  msg = messages.StringField(1, required=True)
  items = messages.MessageField(Community, 2, repeated=True)

STORED_COMMUNITIES = CommunityCollection(items=[
    Community(description='mtv1', id='3'),
    Community(description='mtv_ie', id='4'),
])

#Product classes
class Product(messages.Message):
  """Product that store name."""
  description = messages.StringField(1)
  id = messages.StringField(2)


class ProductCollection(messages.Message):
  """Collection of Products."""
  community = messages.StringField(1, required=True)
  items = messages.MessageField(Product, 2, repeated=True)

STORED_PRODUCTS = ProductCollection(items=[
    Product(description='product 1', id='1'),
    Product(description='product 2', id='2'),
])

#Resource Container for request parameters passed to GET /communities
PRODUCTS_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    communityid=messages.StringField(1, required=True))

#Campaign classes
class Campaign(messages.Message):
  """Campaign store"""
  id = messages.StringField(1)
  name = messages.StringField(2)
  isactive = messages.BooleanField(3)
  products = messages.MessageField(Product, 4, repeated=True)

class CampaignCollection(messages.Message):
  """Collection of Campaigns."""
  community = messages.StringField(1, required=True)
  campaigns = messages.MessageField(Campaign, 2, repeated=True)

STORED_CAMPAIGNS = CampaignCollection(campaigns=[
    Campaign(id='1',name='campaign 1', isactive=True, products=[Product(description='product 2', id='2'), Product(description='product 3', id='3')]),
    Campaign(id='2',name='campaign 2', isactive=False),
])

#Resource Container for request parameters passed to GET /communities
CAMPAIGNS_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    communityid=messages.StringField(1, required=True))



#API ENDPOINT DEFINITION



#serviceapi_root = endpoints.api(name='serviceapi', version='v1', 
#               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
#                                     IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
#               audiences=[ANDROID_AUDIENCE],
#               scopes=[endpoints.EMAIL_SCOPE], description='Service API v1')

serviceapi_root = endpoints.api(name='serviceapi', version='v2', 
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE], description='Service API v1')


@serviceapi_root.api_class()
class CommunitiesApi(remote.Service):
 

  @endpoints.method(message_types.VoidMessage, CommunityCollection,
                      path='communities', http_method='GET',
                      name='communities.listCommunities')
  def communities_list(self, unused_request):
        logging.info("GET communities.listCommunities")
        return STORED_COMMUNITIES

  @endpoints.method(message_types.VoidMessage, CommunityCollection,
                      path='communitiesauthd', http_method='GET',
                      name='communities.listCommunitiesAuthd')
  def communities_listAuthd(self, unused_request):
        logging.info("GET communities.listCommunitiesAuthd")
        logging.info("user is  %s" % endpoints.get_current_user() )
        STORED_COMMUNITIES.msg = "user is  %s" % endpoints.get_current_user()
        return STORED_COMMUNITIES

@serviceapi_root.api_class()
class ProductsApi(remote.Service):
  @endpoints.method(PRODUCTS_GET_REQUEST, ProductCollection,
                      path='communities/{communityid}/products', http_method='GET',
                      name='products.listProducts')
  def communities_list(self, request):
        logging.info("GET products.listProducts  %s" % request.communityid)
        STORED_PRODUCTS.community = request.communityid
        return STORED_PRODUCTS



@serviceapi_root.api_class()
class CampaignsApi(remote.Service):
  @endpoints.method(CAMPAIGNS_GET_REQUEST, CampaignCollection,
                      path='communities/{communityid}/campaigns', http_method='GET',
                      name='campaigns.listCampaigns')
  def communities_list(self, request):
        logging.info("GET campaigns.listCampaigns  %s" % request.communityid)
        STORED_CAMPAIGNS.community = request.communityid
        return STORED_CAMPAIGNS
    

 #end service API classes
   


#the API server code. The casing of APPLICATION in this line must match the casing in the app.yaml file in the line script: helloworld_api.APPLICATION.
APPLICATION = endpoints.api_server([PlaypenEndpointApi, serviceapi_root])

