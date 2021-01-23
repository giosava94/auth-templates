import { Button, Grid } from "@material-ui/core";
import { useAuthDataContext } from "../system/auth-provider";
import { useSocketContext } from "../system/socket-provider";
import { useEffect } from "react";

/* 
  Home page. 
  This should be visible only if the user has signed in.
 */
function Home(props) {
  const { onLogout } = useAuthDataContext();
  const { socket } = useSocketContext();

  useEffect(() => {
    if (socket) {
      socket.on("my_response", (data) => {
        console.log(data);
      });
    }
  }, [socket]);

  const handleClick = () => {
    socket.emit("my_event", { d: "test" });
  };

  return (
    <Grid container direction="column" spacing={2}>
      <Grid item>
        <Button onClick={handleClick}>Send Socket Message</Button>
      </Grid>
      <Grid item>
        <Button onClick={onLogout}>Logout</Button>
      </Grid>
    </Grid>
  );
}

export default Home;
