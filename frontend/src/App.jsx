import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Upload from "./pages/Upload";
import Profile from "./pages/Profile";
import Register from "./pages/Register";


// Функция проверки валидности токена
function isTokenValid() {
  const token = localStorage.getItem("access");
  if (!token) return false;

  try {
    const [, payloadBase64] = token.split(".");
    const payload = JSON.parse(atob(payloadBase64));
    const now = Math.floor(Date.now() / 1000);
    return payload.exp > now;
  } catch (e) {
    return false;
  }
}

// Обёртка для защищённых маршрутов
const PrivateRoute = ({ children }) => {
  return isTokenValid() ? children : <Navigate to="/login" />;
};

export default function App() {
  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            isTokenValid() ? <Navigate to="/dashboard" /> : <Navigate to="/login" />
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute><Dashboard /></PrivateRoute>
          }
        />
        <Route
          path="/upload"
          element={
            <PrivateRoute><Upload /></PrivateRoute>
          }
        />
        <Route
          path="/profile"
          element={
            <PrivateRoute><Profile /></PrivateRoute>
          }
        />

        {/* fallback */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}
