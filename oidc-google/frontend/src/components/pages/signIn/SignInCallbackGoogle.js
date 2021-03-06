import { useEffect, useState } from "react";
import { Redirect } from "react-router-dom";
import { Loading } from "..";
import { useAuthDataContext } from "../../system/auth-provider";
import { redirect_uri } from "../../routing/AuthCallbackRoute";
import { axiosWithCredentials } from "../../system/axios-settings";

function SignInCallbackGoogle(props) {
  const { location } = props;
  const { user, onLogin } = useAuthDataContext();
  const [error, setError] = useState(false);

  useEffect(() => {
    const myLogin = async () => {
      const code = (location.search.match(/code=([^&]+)/) || [])[1];
      const userDetails = "username picture email uuid";
      const scopes = "openid profile email";
      const qParams = [
        `code=${code}`,
        `scope${scopes}`,
        `redirect_uri=${redirect_uri}`,
        `user_details=${userDetails}`,
      ].join("&");
      try {
        const resp = await axiosWithCredentials.get(`/api/login?${qParams}`);
        onLogin(resp.data);
      } catch (err) {
        console.log(err);
        setError(true);
      }
    };
    myLogin();
  }, [location]);

  let component;
  if (user) {
    const state = (location.search.match(/state=([^&]+)/) || [])[1];
    const prevPage = decodeURIComponent(state);
    if (error) {
      component = <div key="error">Login error</div>;
    } else {
      component = <Redirect key="redirect" to={prevPage} />;
    }
  }

  return [component, <Loading key="loading" open={!user} />];
}

export default SignInCallbackGoogle;
