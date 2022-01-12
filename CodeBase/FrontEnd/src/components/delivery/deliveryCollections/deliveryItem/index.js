import React from "react";
import "./deliveryItem.css";
const DeliveryItem = ({ item }) => {
  return (
    <div>
      <div className="delivery-item-cover">
        <img
          src={"https://bar-photos-2021.s3.amazonaws.com/"+item.Id+".png"}
          className="delivery-item-image"
          alt={item.Name}
        />
      </div>
      <div className="delivery-item-title">{item.Name}</div>
    </div>
  );
};

export default DeliveryItem;