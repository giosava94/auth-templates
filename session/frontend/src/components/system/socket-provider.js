import { io } from "socket.io-client";
import { createContext, useState, useMemo, useContext } from "react";

export const SocketContext = createContext(null);

const SocketProvider = (props) => {
  const baseURL =
    process.env.NODE_ENV === "development"
      ? "http://localhost:5000"
      : undefined;
  const namespace = "";

  const [socket, setSocket] = useState(null);

  const onStartSocketConnection = () => {
    setSocket(io(baseURL + namespace, { transports: ["websocket"] }));
  };

  const onCloseSocketConnection = () => {
    if (socket) {
      socket.disconnect();
    }
    setSocket(null);
  };

  const socketDataValue = useMemo(
    () => ({ socket, onStartSocketConnection, onCloseSocketConnection }),
    [socket]
  );

  return <SocketContext.Provider value={socketDataValue} {...props} />;
};

export const useSocketContext = () => useContext(SocketContext);

export default SocketProvider;
