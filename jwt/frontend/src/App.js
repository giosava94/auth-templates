import { BrowserRouter } from "react-router-dom";
import { Routes } from "./components/routing";
import AuthDataProvider from "./components/system/auth-provider";

function App() {
  return (
    <AuthDataProvider>
      <BrowserRouter>
        <Routes />
      </BrowserRouter>
    </AuthDataProvider>
  );
}

export default App;
