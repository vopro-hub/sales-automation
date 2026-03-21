import React from "react";

const AlertBadge = ({ count }) => {
  if (count === 0) return null;

  return (
    <span
      style={{
        backgroundColor: "#ef4444",
        color: "#fff",
        borderRadius: "999px",
        padding: "4px 10px",
        fontSize: "12px",
        marginLeft: "8px",
      }}
    >
      {count}
    </span>
  );
};

export default AlertBadge;
