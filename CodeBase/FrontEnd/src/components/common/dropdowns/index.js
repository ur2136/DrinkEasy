import React from "react";
import DropdownItem from "./dropdownItem";
import "./dropdowns.css";

const Dropdowns = ({ dropdownList }) => {
  return (
    <div className="dropdowns">
      {dropdownList &&
        dropdownList.map((dropdown) => {
          return <DropdownItem dropdown={dropdown} key={dropdown.id} />;
        })}
    </div>
  );
};

export default Dropdowns;