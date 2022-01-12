import { render } from "@testing-library/react";
import React, {Component} from "react";
import Slider from "react-slick";
import { restaurants_top_rated } from "../../../data/restaurants";
import NextArrow from "../carousel/nextArrow";
import PrevArrow from "../carousel/prevArrow";
import "./collection.css";

const collectionList = [
  {
    id: 1,
    title: "Sports Bars",
    key: "sports",
    cover:
      "https://b.zmtcdn.com/data/collections/7e296d5b75ca7b0f88e451b49e41ba99_1618208591.jpg",
  },
  // {
  //   id: 2,
  //   title: "Newly Opened",
  //   key: "new",
  //   cover:
  //   "https://b.zmtcdn.com/data/collections/42e666d436d9a3b90431e6cc4a6b242d_1582106525.jpg",
    
  // },
  // {
  //   id: 3,
  //   title: "Veggie Friendly",
  //   key: "veg",
  //   cover:
  //   "https://www.feastingathome.com/wp-content/uploads/2020/01/Chimichurri-Cauliflower-Bowls-15.jpg",
    
  // },
  {
    id: 4,
    title: "Jazz Bars",
    key: "jazz",
    cover:
    "https://urbanmatter.com/chicago/wp-content/uploads/2020/01/81936566_3174193882596320_7204411677415047168_o.jpg",
    
  },
  {
    id: 5,
    title: "Night Clubs",
    key: "night",
    cover:
    "https://images.unsplash.com/photo-1570872626485-d8ffea69f463?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8bmlnaHQlMjBjbHVifGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=900&q=60",
  
  },
  {
    id: 6,
    title: "LGBTQ Friendly",
    key: "lgbtq",
    cover:
    "https://selectregistry.com/wp-content/uploads/2018/08/gay-friendly-bed-and-breakfast.jpg",
    
  }
];

const settings = {
  infinite: false,
  slidesToShow: 4,
  slidesToScroll: 1,
  nextArrow: <NextArrow />,
  prevArrow: <PrevArrow />,
};

class Collection extends Component {
  state = {
    queryParams: "",
    restaurantsList: [],
    category: "none"
  };

  handleCategory(cat){
    console.log(cat);
    document.getElementById("hack").value = cat;
    var categories = {
      'jazz': 0,
      'sports': 0,
      'lgbtq': 0,
    }
    var category;
    if (cat == "jazz")
      category = 1;
    else if(cat =="sports")
      category = 2;
    else if(cat =="lgbtq")
      category = 3;
    else if (cat == "night")
      category = 4;

    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); 
    var yyyy = today.getFullYear();
    var now = today.getHours();
    today = yyyy + '-' + mm + '-' + dd;
  
    const zipcode =  document.getElementById("loc").value == "" ? "10027" : document.getElementById("loc").value;
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
      'lgbtq': false,
      'crowd' : crowd,
      'day' : today,
      'time' : time,
      'zip_code' : zipcode,
      'rating' : rating,
      'price_level' : price_level,
      'category': category
    };
    this.setState({category:category})
    this.getData(queryParams)
  }


  getData(queryParams){
    console.log(queryParams);
    const url = `https://61m1zj5co5.execute-api.us-east-1.amazonaws.com/v1/getbar?lgbtq=${queryParams.lgbtq}&zip_code=${queryParams.zip_code}&rating=${queryParams.rating}&price_level=${queryParams.price_level}&day=${queryParams.day}&time=${queryParams.time}&crowd=${queryParams.crowd}&category=${queryParams.category}`;
    fetch(url,{
      method : 'POST'
    })
    .then(res => res.json())
    .then(
      (result) => {
        this.setState({
          restaurantsList: result
        });
      this.props.passToParent(this.state.restaurantsList);
      }
    )
  }

  componentDidMount()
  {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); 
    var yyyy = today.getFullYear();
    var now = today.getHours();
    today = yyyy + '-' + mm + '-' + dd;
  
    const zipcode =  document.getElementById("loc").value == "" ? "10027" : document.getElementById("loc").value;
    const crowd =  document.getElementById("crowd").value;
    const input_time = document.getElementById("time").value
    console.log(input_time);
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
      'lgbtq': false,
      'crowd' : crowd,
      'day' : today,
      'time' : time,
      'zip_code' : zipcode,
      'rating' : rating,
      'price_level' : price_level,
      'category': "none"
    };
    this.getData(queryParams)
  
  }
  render(){
    return (
      <div className="collection-wrapper">
        <div className="max-width collection">
          <div className="collection-title">Categories</div>
          <div className="collection-subtitle-row">
            <div className="collection-subtitle-text">
              Explore curated lists of top pubs and bars, based on categories in Manhattan
            </div>
            <div className="collection-location">
              <div>All Categories in Manhattan </div>
              <i className="fi fi-rr-caret-right absolute-center"></i>
            </div>
          </div>
          <Slider {...settings}>
            {collectionList.map((item) => (
              <div>
                <div onClick = {()=>this.handleCategory(item.key)} className="collection-cover">
                <input id = 'hack' value = 'none' hidden />
                <img
                    src={item.cover}
                    alt={item.title}
                    className="collection-image"
                  />
                  <div className="gradient-bg"></div>
                  <div className="collection-card-title">{item.title}</div>
                  <div className="collection-card-subtitle">
                    <div>{item.places}</div>
                  </div>
                </div>
              </div>
            ))}
          </Slider>
        </div>
      </div>
    );
  };
};

export default Collection;