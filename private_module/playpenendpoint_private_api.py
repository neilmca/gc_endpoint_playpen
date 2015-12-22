"""Hello World API implemented using Google Cloud Endpoints.

Defined here are the ProtoRPC messages needed to define Schemas for methods
as well as those methods defined in an API.
"""

import logging
import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID

package = 'PlaypenEndpointPrivateApi' #This is used by the underlying ProtoRpc when creating names for the ProtoRPC messages you create. This package name will show up as a prefix to your message class names in the discovery doc and client libraries

# message classes to be used in the requests and responses
class Greeting(messages.Message):
  """Greeting that stores a message."""
  message = messages.StringField(1)


class GreetingCollection(messages.Message):
  """Collection of Greetings."""
  items = messages.MessageField(Greeting, 1, repeated=True)


STORED_GREETINGS = GreetingCollection(items=[
    Greeting(message='hello world private api response for appversion 2!'),
    Greeting(message='goodbye world private api response for appversion 2!'),
])

#we are adding an API named playpenEndpoint that has two methods serving GET requests, one that returns all Greetings and one that returns only the specified greeting
@endpoints.api(name='playpenEndpointPrivate', version='v2', 
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                     IOS_CLIENT_ID, endpoints.API_EXPLORER_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE],
               scopes=[endpoints.EMAIL_SCOPE])
class PlaypenEndpointPrivateApi(remote.Service):
  """PlaypenEndpointPrivateApi API v1."""

  

  @endpoints.method(message_types.VoidMessage, GreetingCollection,
                      path='privatehellogreeting', http_method='GET',
                      name='greetings.listGreeting')
  def greetings_list(self, unused_request):
        logging.info("GET greetings.listGreeting")
        return STORED_GREETINGS
  ID_RESOURCE = endpoints.ResourceContainer(
      message_types.VoidMessage,
      id=messages.IntegerField(1, variant=messages.Variant.INT32))

  

#the API server code. The casing of APPLICATION in this line must match the casing in the app.yaml file in the line script: helloworld_api.APPLICATION.
APPLICATION = endpoints.api_server([PlaypenEndpointPrivateApi])

