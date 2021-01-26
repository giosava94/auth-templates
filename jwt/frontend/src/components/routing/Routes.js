import { Redirect, Route, Switch } from "react-router-dom";
import { AuthCallbackRoute, PrivateRoute } from ".";
import { Public, Home, Loading } from "../pages";
import { useAuthDataContext } from "../system/auth-provider";

/* Main routing component. User-Developer customizable. */
function Routes(props) {
  const { fetching } = useAuthDataContext();
  return [
    <Switch key="switch">
      {/* Generic public route. Always accessible */}
      <Route exact path="/public" component={Public} />

      {/* 
          Generic private route. 
          When authentication and authorization are not enabled they are always accessible. 
          When authentication and authorization are enabled they are accessible only if the user is authenticated.
          If the user is not authenticated they are redirected to the correct login page.
          */}
      <PrivateRoute exact path="/home" component={Home} />

      {/* User-Developer additional page for their custom auth process */}
      <AuthCallbackRoute path="/signin_callback" />

      <Redirect to="/home" />
    </Switch>,
    <Loading key="loading" open={fetching} />,
  ];
}

export default Routes;
