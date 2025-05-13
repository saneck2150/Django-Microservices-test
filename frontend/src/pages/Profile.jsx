import React, { useEffect, useState } from "react";
import api from "../api";

export default function Profile() {
  const [user, setUser] = useState(null);
  const [files, setFiles] = useState([]);
  const [loadingFiles, setLoadingFiles] = useState(true);

  useEffect(() => {
    api.get("me/")
      .then(res => setUser(res.data))
      .catch(err => console.error(err));

    api.get("my-files/")
      .then(res => setFiles(res.data))
      .catch(err => console.error("Files error:", err))
      .finally(() => setLoadingFiles(false));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("access");
    window.location.href = "/";
  };

  return (
    <div className="container">
      <h2>My Profile</h2>
      {user && (
        <>
          <p><strong>Username:</strong> {user.username}</p>
          <p><strong>Password:</strong> ********</p>
        </>
      )}

      <button onClick={handleLogout}>Logout</button>

      <h3 style={{ marginTop: "30px" }}>My Files</h3>

      {loadingFiles ? (
        <p>Loading files...</p>
      ) : files.length === 0 ? (
        <p>No files uploaded yet.</p>
      ) : (
        <ul>
          {files.map(file => (
            <li key={file.id}>
              <strong>{file.filename}</strong> ({file.content_type}) –{" "}
              <em>{new Date(file.uploaded_at).toLocaleString()}</em>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
