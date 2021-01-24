import { Redirect, Route } from "react-router-dom";
import { useAuthDataContext } from "../system/auth-provider";
import * as SignIns from "../pages/signIn";

const base_url = process.env.REACT_APP_BASE_URL
  ? process.env.REACT_APP_BASE_URL
  : "localhost:3000";
const redirect_uri = "http://" + base_url + "/signin_callback";

/**
 * Route where the user is redirect to after he has signed-in in an
 * external authentication provider requiring a fallback page.
 * Based on user preferences (specified in the environment variable)
 * it redirects the user to the correct sign-in-callback page.
 * When the user is authenticated the user is automatically redirect
 * to the home page.
 */
const AuthCallbackRoute = ({ ...options }) => {
  const { user } = useAuthDataContext();
  if (!user) {
    let finalComponent;
    if (
      process.env.REACT_APP_AUTHN !== undefined &&
      process.env.REACT_APP_AUTHN !== null
    ) {
      const capitalizeFirstLetter = (string) => {
        return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase();
      };

      finalComponent =
        SignIns[
          "SignInCallback" + capitalizeFirstLetter(process.env.REACT_APP_AUTHN)
        ];
    } else {
      finalComponent = SignIns.SignInCallbackCustom;
    }
    return <Route {...options} component={finalComponent} />;
  } else {
    return <Redirect to="/" />;
  }
};

export default AuthCallbackRoute;
export { redirect_uri };
