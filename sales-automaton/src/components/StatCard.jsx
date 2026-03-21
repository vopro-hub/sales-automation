import React from "react";

const StatCard = ({ label, value }) => {
  return (
    <div
      style={{
        padding: "16px",
        border: "1px solid #e5e7eb",
        borderRadius: "8px",
        minWidth: "180px",
      }}
    >
      <div
        style={{
          fontSize: "14px",
          color: "#6b7280",
          marginBottom: "4px",
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontSize: "28px",
          fontWeight: 600,
        }}
      >
        {value}
      </div>
    </div>
  );
};

export default StatCard;
