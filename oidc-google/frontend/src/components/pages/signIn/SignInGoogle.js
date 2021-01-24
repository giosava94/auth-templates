import { useEffect, useState } from "react";
import { Loading } from "..";
import { redirect_uri } from "../../routing/AuthCallbackRoute";
import { axiosWithCredentials } from "../../system/axios-settings";

function SignInGoogle(props) {
  const [fetching, setFetching] = useState(true);
  const [link, setLink] = useState();
  const [error, setError] = useState(false);

  useEffect(() => {
    const getRedirectLink = async () => {
      setFetching(true);
      const scopes = "openid profile email";
      const qParams = [
        `redirect_uri=${redirect_uri}`,
        `scope=${scopes}`,
        "prompt=select_account",
        `state=google`,
      ].join("&");
      try {
        const response = await axiosWithCredentials.get(
          `/api/auth-url?${qParams}`
        );
        setLink(response.data);
      } catch (e) {
        console.log(e);
        setError(true);
      }
      setFetching(false);
    };
    getRedirectLink();
  }, []);

  if (link !== undefined) {
    window.location.assign(link);
  }

  return [
    <div key="error">{error ? "Error while retrieving sign-in link" : ""}</div>,
    <Loading key="loading" loading={fetching} />,
  ];
}

export default SignInGoogle;
