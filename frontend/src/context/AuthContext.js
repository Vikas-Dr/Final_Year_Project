import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);

const getStoredUser = () => JSON.parse(localStorage.getItem("ai_eval_user") || "null");
const getStoredToken = () => localStorage.getItem("ai_eval_token");

export function AuthProvider({ children }) {
  const [user, setUser] = useState(getStoredUser);
  const [token, setToken] = useState(getStoredToken);

  const login = ({ user: nextUser, accessToken }) => {
    localStorage.setItem("ai_eval_user", JSON.stringify(nextUser));
    localStorage.setItem("ai_eval_token", accessToken);
    setUser(nextUser);
    setToken(accessToken);
  };

  const logout = () => {
    localStorage.removeItem("ai_eval_user");
    localStorage.removeItem("ai_eval_token");
    setUser(null);
    setToken(null);
  };

  const value = useMemo(() => ({ user, token, login, logout }), [token, user]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
