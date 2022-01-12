import React, {Component} from "react";
import { dining } from "../../data/dining";
import Collection from "../common/collection";
import ExploreSection from "../common/exploreSection";
import Dropdowns from "../common/dropdowns";
import "./diningOut.css";

//const diningList = dining;
const diningFilters = [
  {
    id: 2,
    title: "Crowdedness",
    icon: <i className="fi fi-rr-apps-sort absolute-center"></i>,
    options:<div>
        <select name="crowd" id="crowd">
        <option value="none" selected disabled hidden></option>
          <option value="1">1</option>
          <option value="2">2</option>
          <option value="3">3</option>
          <option value="4">4</option>
          <option value="5">5</option>
        </select>
        </div>
  },
  {
    id: 3,
    title: "Date",
    icon: <i className="fi fi-rr-calendar absolute-center"></i>,
    options: <input type="date" name = "date" id = "date"></input>

  },
  {
    id: 4,
    title: "Time",
    icon: <i className="fi fi-rr-clock absolute-center"></i>,
    options: <input type="time" id="time" name="time"
    min="09:00" max="18:00"/>
  },
  {
    id: 5,
    title: "Rating",
    icon: <img src="https://img.icons8.com/ios/50/fa314a/rating.png" height = "20px"/>,//<i className="fi fi-rr-rating absolute-center"></i>,
    options:<div>
    <select name="rate" id="rate">
    <option value="none" selected disabled hidden></option>
      <option value="1">1.0+</option>
      <option value="2">2.0+</option>
      <option value="3">3.0+</option>
      <option value="4">4.0+</option>
    </select>
    </div>

  },
  {
    id: 6,
  title: "Pricing",
  icon: <img src="https://img.icons8.com/external-kiranshastry-lineal-kiranshastry/64/fa314a/external-dollar-charity-kiranshastry-lineal-kiranshastry-1.png" height = "20px"/>,//<i className="fi fi-rr-rating absolute-center"></i>,
  options:<div>
  <select name="price" id="price">
    <option value="none" selected disabled hidden></option>
    <option value="1">$</option>
    <option value="2">$$</option>
    <option value="3">$$$</option>
    <option value="4">$$$$</option>
  </select>
  </div>

}
];

class DiningOut extends Component{

 state = {
    diningList: [],
    category: "none"
  };

childCallBack=(value) =>{
this.setState({diningList: value});
}

render () {
  return (
    <div>
      <Collection passToParent={this.childCallBack}/>
      <div className="max-width">
        <Dropdowns dropdownList={diningFilters} />
        {/* <button type="submit" id="search-btn">Search</button> */}
      </div>
      <ExploreSection
        restaurants={this.state.diningList}
        category = {this.state.category}
        collectionName="Bars/Pubs in Manhattan"
      />
    </div>
  );
};
}

export default DiningOut;
