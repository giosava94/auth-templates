import axios from "axios";

const axiosWithCredentials = axios.create({
  withCredentials: true,
  baseURL:
    process.env.NODE_ENV === "development"
      ? "http://localhost:5000"
      : undefined,
});

export { axiosWithCredentials };
