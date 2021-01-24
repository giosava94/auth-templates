# AUTH-TEMPLATES

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

How can we develop a good authentication flow for our web applications? How can we limit users operations through a safe authorization system?

In this example project we will show some authentication and authorization examples, Examples differs based on the communication type establish between the web client and the web server.

In this project we will use a REACT web client, a PYTHON (Flask) web server and, when required, a MONGODB database. A set of docker containers is given in order to simplify the project execution but they are not mandatory.

In this project we will deal with the following web client-web server communication type:

- A web client will periodically execute requests to a web server to retrieve information -> RESTful APIs.
- A web client establishes a full-duplex communication with the web server -> WebSocket connection.

Which is the main difference between this approaches, from an authentication and authorization point of view?

RESTful APIs are stateless whereas WebSocket connections are stateful.

The key difference between stateful and stateless applications is that stateless applications usually don’t _store_ data whereas stateful applications require backing storage.

In the first case, every time the web client executes a request it needs to send additional information about its identity and its authorizations. This can be achieved through **Json Web Tokens (JWTs)**. A **JWT** embeds encoded information and can have an expiration time to limit access.

In the latter, when the user authenticates itself, the web server can store user information on a local database, but it needs a key to retrieve that information. For this reason **sessions** exist. The web server stores the key to retrieve the data inside a _session cookie_.

In both cases, to store user information on the **localStorage** is a bad practice because it is prone to _XSS_ (Cross-Site Scripting) attacks. A good solution is to use **cookies** which remain between different browser sessions, but they can, again, be prone to _CSRF_ (Cross-Site Request Forgery) attacks. For these reason we will use **HttpOnly cookies**. Javascript programs can't read their content which is accessible only by the web server. But remember that nothing is certain in this life!

In any case we will use _httponly cookies_ to store **JWTs** and **Session ID**.

# WEB CLIENT (COMMON LOGIC)

Based on the communication type the web client will execute different tasks but there are common sections. We describe them.

## AUTHENTICATION CONTEXT

A context named **AuthDataContext** stores and provides the user data and the common functions to sign-in and sign-out from the application. Moreover every time the page is refreshed or it is opened for the first time, the **AuthDataContext** checks if the user is already authenticated. Both sign-in and sign-out functions and the authentication check on page reload use a customized instance of **axios** to perform requests, accepting cookies, to the web server.

The **AuthDataContext** provides a **context provider** which will wrap all the project components. This way, the data stored in the **AuthDataContext** will be accessible to all components.

Below the **AuthDataContext** (from a hierarchical point of view) there are the app routes. They can be public or private. The component **Routes** contains all. This component will contains also the user defined routes which can be both public or private.

## PRIVATE ROUTES

Public routes can be accessed by any user, but the access to private routes is restricted to authorized users. If a user is not authenticated it is redirected to the sign-in page. If the user is authenticated and has the correct rights he can see the page content, but, if he is not authorized, he is redirect to an error page. The component **PrivateRoute** manage this logic.

When the **AuthDataContext** updates it's state lower components are re-rendered. This logic allows the **PrivateRoute** to immediately redirect authenticated and authorized users to the correct page or redirect them to the sign-in page.

## SIGN-IN AND SIGN-OUT

The **SignIn** component shows a standard sign-in page. When users fills and submit the login form with their data, these data are sent, through the **AuthDataContext** _onLogin_ function to the web server. If the sign-in procedure succeeds the web server responds with the user data required to the web client and the **AuthDataContext** will store them in a _state_ variable; if the request does not succeeds the web server raises an exception and the web client shows error page or message.

When the user sign-out through the _onLogout_ function of **AuthDataContext**, it performs a request to the web server, which will clear browser cookies, and then clears the user data stored in the context.

In this project we provided a really basic authentication logic, but we develop the project to allow users to add their custom sing-in logic. See [Add custom authentication](#ADD-CUSTOM-AUTHENTICATION) for more details.

# WEB SERVER COMMON LOGIC

As for the web client there are some web settings and functionalities that are commons. Here the details.

The presence of _sign-in_, _sing-out_ and _check already authenticated_ procedures is independent of the web client-web server communication type.

If the user is authenticated the _check already authenticated_ retrieves the correct user data, from a secure source, every time the browser loads the app for the first time or refreshes the page.

Through the usage of the extension **Flask-RESTful**, the web server instantiates three common endpoints providing the _sign-in_, _sign-out_ and _check already authenticated_ functionalities.

The implementation of these endpoints on the communication type and the app requirements!

To allow our web client to communicate with the defined endpoints we need to use the **Flask-CORS** extension to set the cross origin resources (_CORS_RESOURCES_) and to allow cookies exchange (_CORS_ALLOW_CREDENTIALS_).

# RESTFUL API - JWT COOKIES

In this section we will dig in into the **RESTful APIs** version of this project. We will analyze both the web client and the web server main details and how we use the **JWTs**.

When the user signs-in in the web client, it sends a payload with username and password to the web server.

The web server, once it has verified the user identity, generates an _access token_, and eventually a _refresh token_. The _access token_ stores the user identity details and its authorizations, whereas the _refresh token_ allows to generate new access tokens when they expire.

Then it sends back to the web client a response within the user details and the cookies with the **JWTs**.

Every time the web client will execute a request to the web server, it will attach the _access token_ to the request.

When the user sings-out, cookies are cleared.

This logic is well managed by the **Flask-JWT-Extended** extension. It provides useful decorators and functions to generate tokens, decode them, store them into cookies and protect endpoints. It already implements protection from _CSRF_ attacks.

About endpoints protection, endpoints can be public or protect. If a generic protect endpoint does not receive the _access token_ it raises an **unauthorized** exception avoiding the user to access that route. When a valid _access token_ is received, a further manual check can be done decoding the **JWT** and verifying the user authorizations; if the check fails the operation is aborted.

When reloading the browser, the **AuthDataProvider** performs a request to the _refresh_ endpoint to generate a new _access token_ from the _refresh token_ (this logic automatically check user authenticity). If this operation succeeds the user is authenticated otherwise the user is logged out and cookies are cleared.

# WEBSOCKET - SESSION COOKIES

Here we will describe the project using socket-io connection to implement a websocket connection.

Above the **AuthDataContext** we create a **SocketContext** which will contain the socket object and the functions to start and stop a socket connection. Components below this provider will have access to those functions and the socket object to generate socket events.

**Flask-SocketIO** is the flask extension used to create a websocket connection between the web client and the web server on server side, whereas the web client uses the **socket.io-client** npm package. With these libraries the web client and the web server do not use requests and responses, for this reason we can't use JWT cookies as shown before.

When the user signs-in in the web client, it sends a payload with username and password to the web server.

The web server, once it has verified the user identity, thanks to a combination of **Flask-Session** and **Flask-Login** _locally signs-in_ the user, starts a user session in the flask context and return the user details required by the web client.

To _locally sign-in_ a user we need to implement a _User_ class able to store and retrieve user data, starting from an ID, into a DB (or a file).

The ID used to retrieve the user data from the DB is stored in a _session cookie_. The session is hierarchically placed above the socket connection.

When the web client receives the user data it can now open a socket connection. When opening this connection the web server checks if the user is authenticated through the ID retrieved from the _session cookie_.

when the socket connection is open we can skip the authentication check but we can add an authorization check to verify user permissions to perform specific action. In fact, through the session ID we can retrieve the user authorizations stored in the local DB.

When we close the connection the user remains logged id, this way when refreshing the page the **AuthDataContext** performs a request (REST call) to the web server which, using information stored in the _session cookie_, can respond with the user information if the user is authenticated. If the user is not authenticated the session cookie is cleared.

When the users signs-out the connection is also closed.

# RUN THE EXAMPLES

Each sub-project has its own folder with all the required files and dependencies.

| Architecture | Folder      |
| ------------ | ----------- |
| RESTful APIs | **jwt**     |
| SESSION      | **session** |

## DOCKER-COMPOSE EXECUTION

We suggest to use the provided docker-compose files to run the projects. Before starting check you have docker-compose installed on your OS. All the following commands must be execute from the sub-project main folder (_jwt_ or _session_ directory).

Create a _.env_ file. This will be used by the docker-compose to check environment variables. _example.env_ file contains a set of possible environment variables.

    touch .env

To run the production mode type:

    docker-compose build
    docker-compose up -d

The -d flag will run the docker instance in background.

> Before running the project in production mode you must set in the _.env_ file the **REACT_APP_BASE_URL** variable with your site name. This is mandatory to allow the reverse-proxy and the web client to correctly work. See the _example.env_ file for an example.

To run the development mode type:

    docker-compose -f docker-compose-dev.yml up -d

When all containers are ready you can find at http://localhost:3000 which is the standard location for react application in development mode.

The development instance does not automatically start the backend because, for development purposes it is more convenient to run it locally. If you have the correct packages (see the _requirements.txt_ file in _backend_ folder) installed on your OS you can start the backend typing:

    cd backend
    python3 main.py

Otherwise you can use **conda** to create a virtual environment, install the packages listed in the _requirements.txt_ and run the backend.

The python web server is accessible at http://localhost:5000.

To run the web client outside its container, check you have _npm_ and _nodejs_ installed on your OS. Then type:

    cd frontend
    npm i
    npm start

By default authentication is disabled. To enable authentication add to the _.env_ file the string **REACT_APP_AUTH_ENABLED=TRUE**, export this value as an environment variable directly on your OS if you are not using the docker-compose files.

## CONTAINERS

Here we will describe the containers structure.

### DEVELOPMENT

- **WEB CLIENT**: It uses a node image to start a development instance of the react app. It install all required npm packages then the src and public folder are mounted as volumes in the container; this strategy allows automatic page refresh when developers update a file in those folders.

### PRODUCTION

- **WEB CLIENT**: At first it build a node instance with the web client similarly to what we have done in development mode, then it start nginx server running the web client instance. When the nginx instance is ready the build part is dropped lowering the image size. This container has no volumes attached.

- **WEB SERVER**: It uses the tiangolo/uwsgi-nginx-flask which starts a uwsgi flask instance inside an ngnix server. When bulding the image we install the python packages listed in _requirements.txt_.

- **TRAEFIK**: ...

# ADD CUSTOM AUTHENTICATION

# REFERENCES

- Authentication methods: https://testdriven.io/blog/web-authentication-methods/
- Conda: https://docs.conda.io/en/latest/
- Docker: https://www.docker.com/
- Docker-compose: https://docs.docker.com/compose/
- Flask-CORS: https://flask-cors.corydolphin.com/en/latest/index.html
- Flask-Login: https://flask-login.readthedocs.io/en/latest/
- Flask-RESTful: https://flask-restful.readthedocs.io/en/latest/
- Flask-Session: https://flask-session.readthedocs.io/en/latest/
- Flask-SocketIO: https://flask-socketio.readthedocs.io/en/latest/
- Json Web Tokens: https://testdriven.io/blog/web-authentication-methods/
- REACT: https://reactjs.org/
- Traefik: https://doc.traefik.io/traefik/
