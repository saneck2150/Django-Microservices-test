import React, { useState, useRef } from "react";
import api from "../api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState({ text: "", type: "" });
  const fileInputRef = useRef(null);
  const STATUS_TIMEOUT = 3000;

  const resetInput = () => {
    setFile(null);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const flashStatus = (text, type) => {
    setStatus({ text, type });
    setTimeout(() => setStatus({ text: "", type: "" }), STATUS_TIMEOUT);
  };

  const handleUpload = async () => {
    if (!file) {
      flashStatus("Choose a file first", "error");
      return resetInput();
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      await api.post("upload/", formData);
      flashStatus("File uploaded successfully", "success");
    } catch (err) {
      let reason = "Upload failed";
      if (err.response) {
        const data = err.response.data;
        if (typeof data === "string") reason = data;
        else if (data.detail) reason = data.detail;
        else if (data.message) reason = data.message;
        else if (data.error) reason = data.error;
      } else if (err.message) {
        reason = err.message;
      }
      flashStatus(reason, "error");
    } finally {
      resetInput();
    }
  };

  return (
    <>
      <div style={styles.wrapper}>
        <h2 style={styles.title}>Upload File</h2>

        <div style={styles.row}>
          <input
            ref={fileInputRef}
            type="file"
            onChange={(e) => setFile(e.target.files[0] ?? null)}
            style={styles.input}
          />

          <button onClick={handleUpload} style={styles.button}>
            Upload
          </button>
        </div>
      </div>

      {/* статус-сообщение — ВНЕ wrapper'а */}
      {status.text && (
        <p
          style={{
            ...styles.status,
            color: status.type === "success" ? "#28a745" : "#dc3545",
            textAlign: "center",
            marginTop: 12,
          }}
        >
          {status.text}
        </p>
      )}
    </>
  );
}

const styles = {
  wrapper: {
    maxWidth: 700,
    margin: "40px auto",
    padding: 24,
    borderRadius: 12,
    background: "#e6e9ec",
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  title: { margin: 0 },
  row: {
    display: "flex",
    gap: 16,
    alignItems: "center",
    flexWrap: "wrap",
  },
  input: {
    flex: 1,
    padding: "6px 12px",
  },
  button: {
    minWidth: 120,
    padding: "10px 18px",
    border: "none",
    borderRadius: 8,
    fontWeight: 600,
    cursor: "pointer",
    background: "#007bff",
    color: "#fff",
  },
  status: {
    fontWeight: 500,
  },
};
