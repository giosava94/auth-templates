import {
  Avatar,
  Button,
  Dialog,
  DialogContent,
  DialogTitle,
  Grid,
  makeStyles,
  TextField,
} from "@material-ui/core";
import { Https } from "@material-ui/icons";
import { useState } from "react";
import { Loading } from "..";
import { useAuthDataContext } from "../../system/auth-provider";
import { axiosWithCredentials } from "../../system/axios-settings";

const useStyles = makeStyles((theme) => ({
  dialog: {
    margin: theme.spacing(2),
  },
}));

/* Standard sign-in page */
function SingInStandard(props) {
  const [loading, setLoading] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMsg, setErrorMsg] = useState("");
  const classes = useStyles();
  const { onLogin } = useAuthDataContext();

  const handleSubmit = async (e) => {
    if (username !== "" && password !== "") {
      setLoading(true);
      try {
        const resp = await axiosWithCredentials.post("/api/login", {
          username: username,
          password: password,
        });
        onLogin(resp.data);
      } catch (e) {
        console.log(e);
        setErrorMsg("Login failed");
      }
      setUsername("");
      setPassword("");
      setLoading(false);
    } else {
      setErrorMsg("Required")
    }
  };

  const handleUsername = (e) => {
    if (errorMsg) {
      setErrorMsg("");
    }
    setUsername(e.target.value);
  };

  const handlePassword = (e) => {
    if (errorMsg) {
      setErrorMsg("");
    }
    setPassword(e.target.value);
  };

  return [
    <Dialog key="dialog" open={!loading}>
      <DialogTitle align="center">Sing In</DialogTitle>
      <DialogContent className={classes.dialog}>
        <Grid container direction="column" spacing={2} alignItems="center">
          <Grid item>
            <Avatar>
              <Https />
            </Avatar>
          </Grid>
          <Grid item>
            <TextField
              id="username"
              label="Username"
              required
              value={username}
              onChange={handleUsername}
              autoComplete="off"
              error={errorMsg !== ""}
              helperText={errorMsg}
            />
          </Grid>
          <Grid item>
            <TextField
              id="password"
              label="Password"
              type="password"
              required
              value={password}
              onChange={handlePassword}
              autoComplete="off"
              error={errorMsg !== ""}
              helperText={errorMsg}
            />
          </Grid>
          <Grid item>
            <Button
              id="submit-button"
              variant="contained"
              color="primary"
              onClick={handleSubmit}
            >
              Submit
            </Button>
          </Grid>
        </Grid>
      </DialogContent>
    </Dialog>,
    <Loading key="loading" open={loading} />,
  ];
}

export default SingInStandard;
