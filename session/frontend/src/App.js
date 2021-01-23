import { BrowserRouter } from "react-router-dom";
import { Routes } from "./components/routing";
import AuthDataProvider from "./components/system/auth-provider";
import SocketProvider from "./components/system/socket-provider";

function App() {
  return (
    <SocketProvider>
      <AuthDataProvider>
        <BrowserRouter>
          <Routes />
        </BrowserRouter>
      </AuthDataProvider>
    </SocketProvider>
  );
}

export default App;
