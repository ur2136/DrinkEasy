import React from "react";
import "./exploreCard.css";

const ExploreBarCard = ({ restaurant, i }) => {
  const name = restaurant?.Name;
  const coverImg = "https://bar-photos-2021.s3.amazonaws.com/"+restaurant?.Id+".png";
  const rating = restaurant?.Rating;
  const approxPrice = restaurant?.PriceLevel;
  const number = restaurant?.PhoneNumber;
  const LGBTQ = (restaurant?.LGBTQ == "1");
  const crowd = restaurant?.Crowdedness;
  const Url = restaurant?.Url;
  const categories = restaurant?.Categories;
  const bottomContainers = "https://img.icons8.com/office/64/000000/wine-glass.png";
  const proOff = 10;
  const goldOff = 20;
  const discount = 20;
  var rows = [];
  if (parseInt(crowd) == 0){
    rows  = <img src="https://img.icons8.com/ios-filled/50/000000/closed-sign.png" style = {{ height : "24px"}}/>
  }
  else{
  for (var i = 0; i < parseInt(crowd); i++) {
      rows.push( <img
        src={bottomContainers}
        alt="wine"
        style={{ height: "18px" }}
       />);
  }
}
  var priceMap = {
    1: '$',
    2: '$$',
    3: '$$$',
    4: '$$$$',
  }
  console.log(LGBTQ);
  var newapproxPrice = priceMap[approxPrice];
  return (
    <div className={`explore-card cur-po ${i < 3 ? "explore-card-first" : ""}`}>
      <div className="explore-card-cover">
        <img 
          src={coverImg}
          className="explore-card-image"
          alt={restaurant.Name}
        />
        <div>
        <a href={Url} target="_blank">
        <img className= "delivery-time" src="https://img.icons8.com/external-justicon-lineal-color-justicon/64/000000/external-map-map-and-location-justicon-lineal-color-justicon-2.png" height = "20px" width = "20px"/>
        </a>
        </div>
        {/* {LGBTQ && <div className="gold-off"><img src="https://img.icons8.com/color/48/000000/lgbt-flag.png"/></div>} */}
        {/* div className="gold-off absolute-center"><img src="https://img.icons8.com/color/48/000000/lgbt-flag.png"/></div>} */}
        {/* {discount && <div className="discount absolute-center">{discount}</div>} */}
      </div>
      <div className="res-row">
        <div className="res-name">{name}</div>
        {rating && (
          <div className="res-rating absolute-center">
            {rating}  <i className="fi fi-sr-star absolute-center" />
            <img src="https://img.icons8.com/fluency/64/000000/star.png" height= "15px"/>
          </div>
        )}
      </div>
      <div className="res-row">
        <div className="res-price">{newapproxPrice}</div>
        {LGBTQ && <div className="res-cuisine"><img height="35px" width="35px" src="https://img.icons8.com/color/48/000000/lgbt-flag.png"/></div>}
      </div>
        <div>
          <div className="card-separator"></div>
          <div className="explore-bottom">
              <span className="res-cuisine-tag">
                {rows}
              </span>
            <div className="res-bottom-text"><i className="fi fi-rr-phone absolute-center" /> {number}</div>
          </div>
        </div>
    </div>
  );
};


export {ExploreBarCard};
