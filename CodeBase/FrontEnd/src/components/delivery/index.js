import React, {Component} from 'react';
import Filters from '../common/filters';
import Dropdowns from '../common/dropdowns';
import DeliveryCollections from './deliveryCollections';
import './delivery.css';
import TopBrands from "./topBrands";
import { restaurants,restaurants_new, restaurants_trending } from "../../data/restaurants";
import ExploreSection from "../common/exploreSection";

const deliveryFilters = [
    {
      id: 1,
      title: "LGBTQ+ Friendliness",
      options: <input type="checkbox" id="lgbtq" name="lgbtq"></input>
    },
    {
      id: 2,
      title: "Crowdedness",
      icon: <i className="fi fi-rr-apps-sort absolute-center"></i>,
      options:<div>
          <select name="crowd" id="crowd">
            <option value = "none" selected disabled hidden></option>
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
        <option value = "none" selected disabled hidden></option>
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
    <option value = "none" selected disabled hidden></option>
      <option value="1">$</option>
      <option value="2">$$</option>
      <option value="3">$$$</option>
      <option value="4">$$$$</option>
    </select>
    </div>

  }
  ];

class Delivery extends Component{
  state = {
    queryParams: "",
    restaurantsList: [],
    toprestaurantsList: [],
    trendList : []

  };

getData(queryParams){
  console.log(queryParams);
  const url = `https://61m1zj5co5.execute-api.us-east-1.amazonaws.com/v1/getbar?lgbtq=${queryParams.lgbtq}&zip_code=${queryParams.zip_code}&rating=${queryParams.rating}&price_level=${queryParams.price_level}&day=${queryParams.day}&time=${queryParams.time}&crowd=${queryParams.crowd}&category=${queryParams.category}`;
  fetch(url,{
    method : 'POST'
  })
  .then(res => res.json())
  .then(
    (result) => {
      console.log('Normal data',result);
      this.setState({
        restaurantsList: result
      });
    }
  )
}
getTopData(queryParams){
  console.log(queryParams);
  const url = `https://61m1zj5co5.execute-api.us-east-1.amazonaws.com/v1/getbar?lgbtq=${queryParams.lgbtq}&zip_code=${queryParams.zip_code}&rating=${queryParams.rating}&price_level=${queryParams.price_level}&day=${queryParams.day}&time=${queryParams.time}&crowd=${queryParams.crowd}&category=${queryParams.category}`;
  fetch(url,{
    method : 'POST'
  })
  .then(res => res.json())
  .then(
    (result) => {
      console.log('Top data',result);
      this.setState({
        toprestaurantsList: result
      });
    }
  )
}

getTrendingData(queryParams){
  console.log(queryParams);
  const url = `https://61m1zj5co5.execute-api.us-east-1.amazonaws.com/v1/getbar?lgbtq=${queryParams.lgbtq}&zip_code=${queryParams.zip_code}&rating=${queryParams.rating}&price_level=${queryParams.price_level}&day=${queryParams.day}&time=${queryParams.time}&crowd=${queryParams.crowd}&category=${queryParams.category}`;
  fetch(url,{
    method : 'POST'
  })
  .then(res => res.json())
  .then(
    (result) => {
      console.log('Trending data',result);
      this.setState({
        trendList: result
      });
    }
  )
}

handleSearch(){

  //Getting date
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); 
  var yyyy = today.getFullYear();
  var now = today.getHours();
  today = yyyy + '-' + mm + '-' + dd;
  console.log(document.getElementById("time").value);
  const lgbtq = document.getElementById("lgbtq").checked;
  const zipcode =  document.getElementById("loc").value == "" ? "10027" : document.getElementById("loc").value;
  const date = document.getElementById("date").value == "" ? today : document.getElementById("date").value;
  const input_time = document.getElementById("time").value
  if (input_time == ""){
    var time = now;
  }
  else{
    var time = input_time.substring(0,2)
  }
  console.log(time);
  var queryParams = {
    'lgbtq': lgbtq,
    'crowd' : document.getElementById("crowd").value,
    'day' : date,//document.getElementById("date").value,
    'time' : time,
    'zip_code' : zipcode,
    'rating' : document.getElementById("rate").value,
    'price_level' : document.getElementById("price").value,
    'category' : "none"
  };


  var topQueryParams = {
    'lgbtq': false,
    'crowd' : 'none',//document.getElementById("crowd").value,
    'day' : today,
    'time' : now,
    'zip_code' : zipcode,
    'rating' : 4,
    'price_level' : "none",
    'category' : "none"
  };

  var trendingQueryParams = {
    'lgbtq': false,
    'crowd' : 5,
    'day' : today,
    'time' : now,
    'zip_code' : zipcode,
    'rating' : "none",
    'price_level' : "none",
    'category' : "none"
  };
  // console.log('Debug');
  // console.log(queryParams);
  // console.log(topQueryParams);
  this.setState({queryParams: queryParams});
  this.getData(queryParams);
  this.getTopData(topQueryParams);
  this.getTrendingData(trendingQueryParams);
}


componentDidMount(){
  if("geolocation" in navigator){        
  console.log("Available");
  }
  else{
  console.log("not available");
  }
  var latitude;
  var longitude;
  // navigator.geolocation.getCurrentPosition(function(position) {
  //         var latitude = position.coords.latitude;
  //         var longitude = position.coords.longitude;
  //         console.log(latitude);
  //         const url = `http://api.geonames.org/findNearbyPostalCodesJSON?lat=${latitude}&lng=${longitude}&username=demo&radius=1`
  //         const url2 = `https://maps.googleapis.com/maps/api/geocode/json?latlng=${latitude},${longitude}&key=AIzaSyBpiTf5uzEtJsKXReoOKXYw4RO0ayT2Opc`
  //         fetch(url2,{
  //           method : 'GET'
  //         })
  //         .then(res => res.json())
  //         .then(
  //           (result) => {
  //             var zip_code = result.results[0].address_components[7].long_name;
  //             document.getElementById("loc").value = zip_code;
  //             //this.setState({zip_code:zip_code});
  //           }
  //         )
  //       });

  //Getting date
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth() + 1).padStart(2, '0'); 
  var yyyy = today.getFullYear();
  var now = today.getHours();
  today = yyyy + '-' + mm + '-' + dd;

  const zipcode =  document.getElementById("loc").value == "" ? "10027" : document.getElementById("loc").value;
  const lgbtq =  document.getElementById("lgbtq").checked;
  const crowd =  document.getElementById("crowd").value;
  const input_time = document.getElementById("time").value
  if (input_time == ""){
    var time = now;
  }
  else{
    var time = input_time.substring(0,2)
  }
  const rating =  document.getElementById("rate").value;
  const price_level =  document.getElementById("price").value;

  console.log(time);
  var queryParams={
    'lgbtq': lgbtq,
    'crowd' : crowd,
    'day' : today,
    'time' : time,
    'zip_code' : zipcode,
    'rating' : rating,
    'price_level' : price_level,
    'category': "none"
  };

  var topQueryParams = {
    'lgbtq': false,
    'crowd' : "none",
    'day' : today,
    'time' : now,
    'zip_code' : zipcode,
    'rating' : 4,
    'price_level' : "none",
    'category' : "none"
  };

  var trendingQueryParams = {
    'lgbtq': false,
    'crowd' : 5,
    'day' : today,
    'time' : now,
    'zip_code' : zipcode,
    'rating' : "none",
    'price_level' : "none",
    'category' : "none"
  };

  this.getData(queryParams);
  this.getTopData(topQueryParams);
  this.getTrendingData(trendingQueryParams);
}

  render(){
      return (
        <div id = "delv" restaurants = {[{'Id':'test'}]}>
        <div className='max-width'>
            <span>
            <Dropdowns dropdownList={deliveryFilters} />
            <button type="submit" onClick = {this.handleSearch.bind(this)} id="search-btn">Search</button>
            </span>
        </div>
        <DeliveryCollections list = {this.state.trendList}/>
        <TopBrands list = {this.state.toprestaurantsList} />
        <ExploreSection
        restaurants={this.state.restaurantsList}
        collectionName="Bars/Pubs in Manhattan"
      />
      </div>
      )
    } 
 }

export default Delivery;

