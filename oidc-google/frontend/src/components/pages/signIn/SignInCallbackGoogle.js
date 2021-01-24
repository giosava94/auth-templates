import { useEffect, useState } from "react";
import { Loading } from "..";
import { useAuthDataContext } from "../../system/auth-provider";
import { redirect_uri } from "../../routing/AuthCallbackRoute";
import { axiosWithCredentials } from "../../system/axios-settings";

function SignInCallbackGoogle(props) {
  const { location } = props;
  const { onLogin } = useAuthDataContext();
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
        onLogin({ user: resp.data });
      } catch (err) {
        console.log(err);
        setError(true);
      }
    };
    myLogin();
  }, [location]);

  return [
    <div key="error">{error ? "Login error" : ""}</div>,
    <Loading key="loading" loading={!error} />,
  ];
}

export default SignInCallbackGoogle;
