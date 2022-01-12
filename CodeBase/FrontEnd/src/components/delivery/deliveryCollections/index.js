import React from "react";
import "./deliveryCollections.css";
import DeliveryItem from "./deliveryItem";
import Carousel from "react-grid-carousel";
import Slider from "react-slick";
import PrevArrow from "../../common/carousel/prevArrow";
import NextArrow from "../../common/carousel/nextArrow";
import {restaurants_trending } from "../../../data/restaurants";


//Logic for creating our list
var trendingList = []
for (var i = 0; i < restaurants_trending.length; i ++){
  trendingList[i] = {
    id:i,
    title : restaurants_trending[i].Name,
    cover: 'https://bar-photos-2021.s3.amazonaws.com/ChIJBxJ-juJYwokRIhCTJPoQTKs.png'//restaurants_top_rated[i].id,
  }

}

//Zomato data
const deliveryItems = [
  {
    id: 1,
    title: "Suite",
    cover:
      "https://lh3.googleusercontent.com/proxy/oXy8eFQ_imVSzlQRwzH0p7qftbNARPIcBeYAIEdmnVeAE6fIm78c3n1hCAYIoAbYxt-yUIDA97XBBwCKXQG5XAB2umWFjvBbrhutSm8VD4THPrZF",
  },
  {
    id: 2,
    title: "Lion's Head Tavern",
    cover:
      "https://nyc.thedrinknation.com/images/bars/3lionsheadtavern.jpg",
  },
  {
    id: 3,
    title: "1020 Bar",
    cover:
      "https://s3-media0.fl.yelpcdn.com/bphoto/6PwCloJMw3m7yv-1vQdXRw/348s.jpg",
  },
  {
    id: 4,
    title: "Amity Hall",
    cover:
      "https://static.spotapps.co/spots/fa/b0a1a044b111e894d8c160d8abbdad/full",
  },
  {
    id: 5,
    title: "Industry",
    cover:
      "https://pyxis.nymag.com/v1/imgs/858/6e4/0b556bcbf56ccf1578f8e6d6fadea03015-industry-01.rsocial.w1200.jpg",
  },
  {
    id: 6,
    title: "Pieces",
    cover:
      "http://2.bp.blogspot.com/-8tUXobUgGtY/Tt9iiJIkLEI/AAAAAAAAO_E/I29cHKC81rk/s1600/screen-capture-4.jpg",
  },
  {
    id: 7,
    title: "Flaming Saddles",
    cover:
      "https://pyxis.nymag.com/v1/imgs/b93/ed2/0be10af57348ba6587a9b5dc49a6d0ed1c-flaming-saddles-01.rsocial.w1200.jpg",
  },
  {
    id: 8,
    title: "La Bain",
    cover:
      "https://media.guestofaguest.com/t_article_content/gofg-media/2021/03/1/54584/screen_shot_2021-03-17_at_11.41.22_am.png",
  },
  {
    id: 9,
    title: "Paradise",
    cover:
      "https://cdn.vox-cdn.com/thumbor/eJv5Oio8EkBV5CvE4dEAC7gYgyk=/0x0:5400x4047/1200x800/filters:focal(2268x1592:3132x2456)/cdn.vox-cdn.com/uploads/chorus_image/image/63048041/Mister_Paradise_Interior_Wide.0.jpg",
  },
  {
    id: 10,
    title: "Nobody Told Me",
    cover:
      "https://arc-anglerfish-arc2-prod-spectator.s3.amazonaws.com/public/7TCMHJHQQZCX3IG3APE6FTADNQ.jpg",
  },
  {
    id: 11,
    title: "Tap a Keg",
    cover:
      "https://friedneckbones.files.wordpress.com/2012/04/tapakeg-002.jpg",
  },
];

const settings = {
  infinite: false,
  slidesToShow: 4,
  slidesToScroll: 1,
  nextArrow: <NextArrow />,
  prevArrow: <PrevArrow />,
};

const DeliveryCollections = ({list}) => {
  return (
    <div className="delivery-collections">
      <div className="max-width">
        <div className="collection-title">Trending Places</div>
        <Slider {...settings}>
          {list.map((item) => { //changed deliverItem to trendingList
            return <DeliveryItem item={item} />;
          })}
        </Slider>
      </div>
    </div>
  );
};

export default DeliveryCollections;