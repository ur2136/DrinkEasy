import React, {useRef} from "react";
import ExploreCard, {ExploreBarCard} from "./exploreCard";
import "./exploreSection.css";

const ExploreSection = ({ restaurants, category, collectionName }) => {
  console.log(restaurants);
  return (
    <div id = "hi" className="max-width explore-section">
      <div className="collection-title">{collectionName}</div>
      <div className="explore-grid">
        {restaurants.map((restaurant, i) => (
          <ExploreBarCard restaurant = {restaurant} i={i} />
        ))}
      </div>
    </div>
  );
};

export default ExploreSection;