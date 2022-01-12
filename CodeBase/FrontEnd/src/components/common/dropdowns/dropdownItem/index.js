import React from "react";
import "./dropdownItem.css";

const dropdownItem = ({ dropdown }) => {
  return (
    <div className="dropdown-item">
      {dropdown.icon && dropdown.icon}
      <div className="dropdown-name">{dropdown.title}</div>
      {dropdown.options}
    </div>
  );
};

export default dropdownItem;