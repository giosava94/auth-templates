import { Button, Grid } from "@material-ui/core";
import { useAuthDataContext } from "../system/auth-provider";
import { axiosWithCredentials } from "../system/axios-settings";

/* 
  Home page. 
  This should be visible only if the user has signed in.
 */
function Home(props) {
  const { onLogout } = useAuthDataContext();

  const handlePublic = async () => {
    const resp = await axiosWithCredentials.get("/api/public");
    console.log(resp);
  };

  const handlePrivate = async () => {
    const resp = await axiosWithCredentials.get("/api/private");
    console.log(resp);
  };

  return (
    <Grid container direction="column" spacing={2}>
      <Grid item>
        <Button onClick={handlePrivate}>Execute Private Request</Button>
      </Grid>
      <Grid item>
        <Button onClick={handlePublic}>Execute Public Request</Button>
      </Grid>
      <Grid item>
        <Button onClick={onLogout}>Logout</Button>
      </Grid>
    </Grid>
  );
}

export default Home;
