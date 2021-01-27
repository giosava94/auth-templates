# AUTH-TEMPLATES

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

How can we develop a good authentication flow for our web applications? How can we limit users operations through a safe authorization system?

In this example project we will show some authentication and authorization examples. Examples differs based on the communication type establish between the web client and the web server.

In this project we will use a REACT web client and a PYTHON (Flask) web server. A set of docker containers is given in order to simplify the project execution but they are not mandatory.

In this project we present a project structure that is designed to present a standard authentication method and foresees the implementation of multiple authentication methods to be used in a mutually exclusive way. This does not imply that one of the custom authentication method can't provide multiple authentication solutions (external provider with other providers).

Usually the authentication logic may change but how user data are managed in the application should not depend on this. For this reason we present a set of sub-projects with a customizable authentication logic which does not impact on how this data are used inside the web application.

The sub-projects architecture has been designed to tempt developers not to change the already present files but to add new files, with their custom logic, with few constraints required for the project to correctly use them.

Moreover in this project we will deal with the following web client-web server communication type:

- A web client will periodically execute requests to a web server to retrieve information -> RESTful APIs.
- A web client establishes a full-duplex communication with the web server -> WebSocket connection.

Which is the main difference between these approaches, from an authentication and authorization point of view?

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

When the socket connection is opened we can skip the authentication check but we can add an authorization check to verify user permissions to perform specific action. In fact, through the session ID we can retrieve the user authorizations stored in the local DB.

When we close the connection the user remains logged id, this way when refreshing the page the **AuthDataContext** performs a request (REST call) to the web server which, using information stored in the _session cookie_, can respond with the user information if the user is authenticated. If the user is not authenticated the session cookie is cleared.

When the users signs-out the connection is also closed.

# ADD CUSTOM AUTHENTICATION

Often developers want to integrate their custom authentication logic or use external authentication provider. These changes can affect both the web client and the web server.

In both **JWTs** and **session** based sub-projects we arrange a simple authentication system which can be easily expanded by developers. In the proposed logic developers don't have to change the default files. They have a subset of templates to copy and implement with their logic. If they follow the instructions correctly all should work.

In the **oidc-google** sub-project we give an example of a custom authentication using google as an external **OpenID Connect** (OIDC) provider. For a description of the code flow when performing an OIDC authentication look at the [OIDC authorization code flow](#OIDC_AUTH_CODE_FLOW).

At first we will talk about the web server, then about the client server. We use this order because changes to the first may not implies changes to the latter, whereas changes to the web client will (most probably) implies changes to the web server. In the **oidc-google** example changes to the web server requires changes to the web client.

## WEB SERVER

All authentication and authorizations customizable endpoints and related functions are stored in the **backend/app/auth/providers** folder.

In this folder the _local.py_ module contains the standard endpoints and functions for the local authentication.

The _example.py_ module is a template with the instructions to write a new module with the custom authentication functions and endpoints. As the description said, developers should _copy_ this file and _implement_:

- **Login endpoint**: if no changes are required it can be imported from another module already implementing it (for example _local.py_) or it can be written from zero. The unique requirement for this endpoint is the usage of _get_tokens_ or _start_user_session_ functions (it depends on the communication type between the web server and the web client).
- **Refresh endpoint**: this should be imported from _local.py_. If developers want to write their own refresh endpoint, they must take as reference the one implemented in _local.py_.
- **Logout endpoint**: if no changes are required it can be imported from another module already implementing it (for example _local.py_) or it can be written from zero. The unique requirement for this endpoint is that it has to clear all **JWTs** or **Session** cookies (it depends on the communication type between the web server and the web client).
- **add_auth_routes**: this function is essential because it will be used by the _main.py_ module in the **backend** folder. This function is in charge to add to the APIs all (or a part) of the endpoints defined in this file.

Developers can add to this file as much functions and enpoints as they want (be consistent on what you add to this file!).

The _google.py_ module is a working example of what developers should do to implement external authentication and authorization with an OIDC provider.

This module uses the standard logout and refresh enpoints, but it implements a custom login endpoint based on multiple functions. The login endpoints does not expect a _PUT_ request (as the one implemented into _local.py_) but a _GET_ request with specific params. Moreover it implements another endpoints to get the correct link to redirect the user to the Google's authentication and authorization page.
Finally, as required by _example.py_, it implements the _add_auth_routes_ function adding the defined resources to the web server APIs.

This example shows how various can be the authentication procedures.

> How can _main.py_ import the correct _add_auth_routes_ function? Developers have to set the **REACT_APP_AUTHN** environment variable in the _.env_ file with the name of their custom authentication procedure, in our example **google**.
>
> This name must be equal to the module name!
>
> In fact the _main.py_ module searches in the **backend/app/auth/providers** a module with the name stored in the environment variable. If it finds the module it loads from it the _add_auth_routes_ otherwise it loads _add_auth_routes_ from _local.py_.

## WEB CLIENT

All sing-in pages are stored in the **src/components/pages/singIn** folder.

In this folder there is the **SignInStandard** component which is the standard login page. This page, on form submit, executes a _POST_ request to the web server sending username and password. Once the component receives the response it uses the _onLogin_ function of the authentication provider to store in the context the user data retrieved from the database.

Developers can implement their own sign-in components and can make requests to the web server as they please. Based on the authentication settings (_.env_ file), **PrivateRoute** will load the correct **SignIn** page.

Developers can implement multiple sign-in components recalling themeselves. For example when implementing an OIDC authentication the external provider requires a _callback endpoint_ on the web client to land when the access to the user data, through the external provider, has been granted ([OIDC authorization code flow](#OIDC_AUTH_CODE_FLOW)). At the _callback enpoint_ the web client will render another component which will execute the remaining authentication passages.

Because OIDC providers usage is common all the sub-projects already provides an **AuthCallbackRoute** component that, based on the authentication settings (_.env_ file), loads the correct _sing-in-callback_ component (which must be implemented). The landing endpoint for the external provider is already calculated in the **AuthCallbackRoute** (based on the application base url) and can be used (imported) into other components.

These are the requirements when implementing custom authentication components:

- The first component to render when the authentication procedure begins must be exported from the _index.js_ as a named component with the _SignIn_ prefix (i.e. **SignInCustom**).
- At the end of the authentication procedure (which may involve multiple components), the component must receive a response from the web server with the user data and call the _onLogin_ function of **AuthDataProvider** to save those data in the context.
- When writing a sign-in-callback component, it must be exported from the _index.js_ as a named component with the _SignInCallback_ prefix and the same suffix of the corresponding _SignInPage_ (i.e. **SignInCallbackCustom**).
- Use **axiosWithCredentials** when performing requests to the web server. This _axios_ instance already has the correct base url and it is instructed to send and receive _cookies_.

In the **oidc-google** sub-project we add a **SignInGoogle** component. This component makes a request to get the correct url to redirect the user to the external provider authentication and authorization page. Once the response arrives it redirects the user to that page.

When the external provider redirects the user to the web client callback page, **AuthCallabackRoute** renders **SignInCallbackGoogle**. This component reads the code, received as params in the current url, and executes a _GET_ request to web server login endpoint (adding all required params). When the web server returns the user data **SignInCallbackGoogle** calls the _onLogin_ function to update user data in the web client. It is duty of your component to redirect the user to the home page or the protected page! In our case we can return to the private page we were trying to access before the login; this is possible because we sent to the OIDC provider a state with the correct path and when the provider gave us the response it returned again that params. 

> The exports addition in the _index.js_ file are mandatory in order to allow the **PrivateRoute** and **AuthCallbackRoute** logic to load the correct sign-in page.

> How can PrivateRoute and AuthCallbackRoute import the correct component? Developers have to set the **REACT_APP_AUTHN** environment variable in the _.env_ file with the name of their custom authentication procedure, in our example **google**.
>
> These components import, from the _src/components/pages/signIn/index.js_ file, all the components defined in the _signIn_ folder and, based on the environment variable load the correct component to render.
>
> In our example we load the **SignInGoogle** and **SignInCallbackGoogle** components. If the name specified in the environemnt variable does not match any of the exported components the app renders the **SingInStandard** component.

# RUN THE EXAMPLES

Each sub-project has its own folder with all the required files and dependencies.

| Architecture | Folder          |
| ------------ | --------------- |
| RESTful APIs | **jwt**         |
| SESSION      | **session**     |
| OIDC GOOGLE  | **oidc-google** |

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

> In the **jwt** sub-project when authentication is disabled you can't execute requests to the private endpoint because you have not the **JWTs**. If you want to update this logic you have to implement a custom decorator.

> The **oidc-google** sub-project requires the **GOOGLE_CLIENT_ID** and **GOOGLE_SECRET** environment variables. We do not provide a default value for them. Moreover, when you launch the web server locally, you need to accept the ssl certificate every time you relaunch it (https://localhost:5000).

## CONTAINERS

Here we will describe the containers structure.

### DEVELOPMENT

- **WEB CLIENT**: It uses a node image to start a development instance of the react app. It install all required npm packages then the src and public folder are mounted as volumes in the container; this strategy allows automatic page refresh when developers update a file in those folders.

### PRODUCTION

- **WEB CLIENT**: At first it build a node instance with the web client similarly to what we have done in development mode, then it start nginx server running the web client instance. When the nginx instance is ready the build part is dropped lowering the image size. This container has no volumes attached.

- **WEB SERVER**: **jwt** and **oidc-google** projects use the tiangolo/uwsgi-nginx-flask image which starts a uwsgi flask instance inside an ngnix server. When bulding the image we install the python packages listed in _requirements.txt_. On the other side **session** project uses use a standard python image to run the web server because Flask-SocketIO already provides a production ready server based on *gevent* or *eventlet* (which must be installed on the docker image).

- **TRAEFIK**: ...

# FURTHER EXPLANATIONS

## OIDC AUTH CODE FLOWS

...

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
- OAuth 2.0 with Google APIs - OIDC: https://developers.google.com/identity/protocols/oauth2/openid-connect
- REACT: https://reactjs.org/
- Traefik: https://doc.traefik.io/traefik/
