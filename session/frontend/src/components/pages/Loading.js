import { Backdrop, CircularProgress, makeStyles } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  backdrop: { zIndex: theme.zIndex.drawer + 1, color: "#fff" },
}));

/* Loading page */
function Loading(props) {
  const { open } = props;
  const classes = useStyles();
  return (
    <Backdrop key="loading" className={classes.backdrop} open={open}>
      <CircularProgress color="inherit" />
    </Backdrop>
  );
}
export default Loading;
