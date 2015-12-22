/**
 * @fileoverview
 * Provides methods for the Hello Endpoints sample UI and interaction with the
 * Hello Endpoints API.
 */

/** google global namespace for Google projects. */
var google = google || {};

/** appengine namespace for Google Developer Relations projects. */
google.appengine = google.appengine || {};

/** samples namespace for App Engine sample code. */
google.appengine.samples = google.appengine.samples || {};

/** hello namespace for this sample. */
google.appengine.samples.hello = google.appengine.samples.hello || {};

/**
 * Client ID of the application (from the APIs Console).
 * @type {string}
 */
google.appengine.samples.hello.CLIENT_ID =
    '255310283450-o8dbs2vq1p2gdqspb79fp05a9dtpl304.apps.googleusercontent.com';

/**
 * Scopes used by the application.
 * @type {string}
 */
google.appengine.samples.hello.SCOPES =
    'https://www.googleapis.com/auth/userinfo.email';

/**
 * Whether or not the user is signed in.
 * @type {boolean}
 */
google.appengine.samples.hello.signedIn = false;


/**
 * Initializes the application.
 * @param {string} apiRoot Root of the API's path.
 */
google.appengine.samples.hello.init = function (apiRoot) {
    // Loads the OAuth and  playpenEndpoint APIs asynchronously, and triggers login
    // when they have completed.
    var apisToLoad;
    var callback = function () {
        if (--apisToLoad == 0) {
            google.appengine.samples.hello.enableButtons();
            google.appengine.samples.hello.signin(true,google.appengine.samples.hello.userAuthed);

        }
    }

    apisToLoad = 2; // must match number of calls to gapi.client.load()
    gapi.client.load('playpenEndpoint', 'v1', callback, apiRoot);
    gapi.client.load('oauth2', 'v2', callback);
};
/**
 * Enables the button callbacks in the UI.
 */
google.appengine.samples.hello.enableButtons = function () {
    var getGreeting = document.querySelector('#getGreeting');
    getGreeting.addEventListener('click', function (e) {
        google.appengine.samples.hello.getGreeting(
            document.querySelector('#id').value);
    });

    var listGreeting = document.querySelector('#listGreeting');
    listGreeting.addEventListener('click',
        google.appengine.samples.hello.listGreeting);

  var authedGreeting = document.querySelector('#authedGreeting');
  authedGreeting.addEventListener('click',
      google.appengine.samples.hello.authedGreeting);

  var signinButton = document.querySelector('#signinButton');
  signinButton.addEventListener('click', google.appengine.samples.hello.auth);
};


/**
 * Prints a greeting to the greeting log.
 * param {Object} greeting Greeting to print.
 */
google.appengine.samples.hello.print = function (greeting) {
    var element = document.createElement('div');
    element.classList.add('row');
    element.innerHTML = greeting.message;
    document.querySelector('#outputLog').appendChild(element);
};

/**
 * Handles the auth flow, with the given value for immediate mode.
 * @param {boolean} mode Whether or not to use immediate mode.
 * @param {Function} callback Callback to call on completion.
 */
google.appengine.samples.hello.signin = function(mode, callback) {
  gapi.auth.authorize({client_id: google.appengine.samples.hello.CLIENT_ID,
      scope: google.appengine.samples.hello.SCOPES, immediate: mode},
      callback);
};

/**
 * Presents the user with the authorization popup.
 */
google.appengine.samples.hello.auth = function() {
  if (!google.appengine.samples.hello.signedIn) {
    google.appengine.samples.hello.signin(false,
        google.appengine.samples.hello.userAuthed);
  } else {
    google.appengine.samples.hello.signedIn = false;
    document.querySelector('#signinButton').textContent = 'Sign in';
    document.querySelector('#authedGreeting').disabled = true;
  }
};


/**
 * Loads the application UI after the user has completed auth.
 */
google.appengine.samples.hello.userAuthed = function() {
  var request = gapi.client.oauth2.userinfo.get().execute(function(resp) {
    if (!resp.code) {
      google.appengine.samples.hello.signedIn = true;
      document.querySelector('#signinButton').textContent = 'Sign out';
      document.querySelector('#authedGreeting').disabled = false;
    }
  });
};

/**
 * Greets the current user via the API.
 */
google.appengine.samples.hello.authedGreeting = function(id) {
  gapi.client.helloworld.greetings.authed().execute(
      function(resp) {
        google.appengine.samples.hello.print(resp);
      });
};

/**
 * Gets a numbered greeting via the API.
 * @param {string} id ID of the greeting.
 */
google.appengine.samples.hello.getGreeting = function (id) {
    alert("google.appengine.samples.hello.getGreeting")
    gapi.client.playpenEndpoint.greetings.getGreeting({ 'id': id }).execute(
        function (resp) {
            alert("google.appengine.samples.hello.getGreeting CALLBACK")
            if (!resp.code) {
                google.appengine.samples.hello.print(resp);
            }
        });
};

/**
 * Lists greetings via the API.
 */
google.appengine.samples.hello.listGreeting = function () {
    gapi.client.playpenEndpoint.greetings.listGreeting().execute(
        function (resp) {
            if (!resp.code) {
                resp.items = resp.items || [];
                for (var i = 0; i < resp.items.length; i++) {
                    google.appengine.samples.hello.print(resp.items[i]);
                }
            }
        });
};