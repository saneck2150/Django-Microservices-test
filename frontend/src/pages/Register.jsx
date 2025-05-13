import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    password: "",
    password2: "",
    email: "",
    full_name: ""
  });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");

  useEffect(() => {
    localStorage.removeItem("access");
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setErrors({});
    setMessage("");

    if (form.password !== form.password2) {
      setErrors({ password2: "Passwords do not match" });
      return;
    }

    api.post("register/", form)
      .then(() => {
        setMessage("Registration successful. You can now log in.");
        setTimeout(() => navigate("/login"), 1500);
      })
      .catch(err => {
        if (err.response?.data) {
          setErrors(err.response.data);
        } else {
          setMessage("Registration failed. Try again.");
        }
      });
  };

  return (
    <div style={{ maxWidth: 500, margin: "40px auto", padding: 20, background: "white", borderRadius: 10 }}>
      <h2>Register</h2>
      <form onSubmit={handleSubmit}>
        {['username', 'email', 'full_name', 'password', 'password2'].map((field, i) => (
          <div key={i} style={{ marginBottom: 16 }}>
            <label>{field.replace("_", " ").replace(/\b\w/g, c => c.toUpperCase())}:</label>
            <input
              type={field.includes("password") ? "password" : "text"}
              name={field}
              value={form[field]}
              onChange={handleChange}
              style={{ width: "90%" }}
            />
            {errors[field] && <div style={{ color: "red", fontSize: "0.9em" }}>{errors[field]}</div>}
          </div>
        ))}
        <button type="submit">Register</button>
        {message && <p style={{ marginTop: 10 }}>{message}</p>}
      </form>
    </div>
  );
}
