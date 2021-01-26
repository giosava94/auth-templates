import { createContext, useState, useEffect, useMemo, useContext } from "react";
import { axiosWithCredentials } from "./axios-settings";

export const AuthDataContext = createContext(null);

const initialAuthData = {};

const AuthDataProvider = (props) => {
  const [authData, setAuthData] = useState(initialAuthData);
  const [fetching, setFetching] = useState(false);

  const onLogin = (userData) => {
    setAuthData({ user: userData });
  };

  const onLogout = async () => {
    try {
      await axiosWithCredentials.get("/api/logout");
    } catch (e) {
      console.log(e);
    }
    setAuthData(initialAuthData);
  };

  /* The first time the component is rendered, it tries to
   * fetch the auth data from the backend.
   */
  useEffect(() => {
    const getAuthData = async () => {
      setFetching(true);
      try {
        const resp = await axiosWithCredentials.get("/api/refresh");
        if (resp) {
          setAuthData({ user: resp.data });
        } else if (authData) {
          setAuthData(initialAuthData);
        }
      } catch (e) {
        console.log(e);
        if (e.response !== undefined && e.response.status === 401) {
          onLogout();
        }
      }
      setFetching(false);
    };

    // Authentication and authorization enabled
    if (
      process.env.REACT_APP_AUTH_ENABLED &&
      process.env.REACT_APP_AUTH_ENABLED.toLowerCase() === "true"
    ) {
      getAuthData();
    }
  }, []);

  const authDataValue = useMemo(
    () => ({ ...authData, fetching, onLogin, onLogout }),
    [authData, fetching]
  );

  return <AuthDataContext.Provider value={authDataValue} {...props} />;
};

export const useAuthDataContext = () => useContext(AuthDataContext);

export default AuthDataProvider;
