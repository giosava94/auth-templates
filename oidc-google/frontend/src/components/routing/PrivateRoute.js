import { Route } from "react-router-dom";
import { NotAuthorized } from "../pages";
import { useAuthDataContext } from "../system/auth-provider";
import * as SignIns from "../pages/signIn";

/* 
  Private Route.
  This page is always accessible when the auth process is not enabled.
  If the auth process is enabled users can access to this page only if they are authenticated. #TODO and possess the correct authorizations?
  If not they are redirected to the correct sing-in page.
  The sign-in page change based on the environment variable with the authentication method type
  (if not specified it is the default one).
  */
const PrivateRoute = ({ component, authorized, ...options }) => {
  const { user } = useAuthDataContext();

  let finalComponent;

  // Authentication and authorization enabled
  if (
    process.env.REACT_APP_AUTH_ENABLED &&
    process.env.REACT_APP_AUTH_ENABLED.toLowerCase() === "true"
  ) {
    // User has signed in
    if (user) {
      // No roles restrictions for this page or user is authorized
      if (!authorized || user.role in authorized) {
        finalComponent = component;
      }
      // Current user is forbidden to see this page
      else {
        finalComponent = NotAuthorized;
      }
    }
    // Redirect to a custom sign-in page
    else if (
      process.env.REACT_APP_AUTHN !== undefined &&
      process.env.REACT_APP_AUTHN !== null
    ) {
      const capitalizeFirstLetter = (string) => {
        return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
      };

      finalComponent =
        SignIns["SignIn" + capitalizeFirstLetter(process.env.REACT_APP_AUTHN)];
    }
    // Redirect to standard sign-in page
    else {
      finalComponent = SignIns.SignInStandard;
    }
  }
  // Authentication and authorization disabled
  else {
    finalComponent = component;
  }

  return <Route {...options} component={finalComponent} />;
};

export default PrivateRoute;
