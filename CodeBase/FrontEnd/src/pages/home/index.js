import React, { useState } from 'react';
import Header from '../../components/common/header';
import TabOptions from '../../components/common/tabOptions';
import Footer from '../../components/common/footer';
import Delivery from '../../components/delivery';
import DiningOut from '../../components/diningOut';
import Nightlife from '../../components/nightlife';


const HomePage = () => {
    const [activeTab, setActiveTab] = useState("Delivery");
    return (
        <div>
           <Header />
           <TabOptions activeTab={activeTab} setActiveTab={setActiveTab} />
           {getCorrectScreen(activeTab)}
           <Footer />
        </div>
    );
};

const getCorrectScreen = (tab) => {
    switch(tab){
        case "Explore":
            return <Delivery />
        case "Choose your vibe":
            return <DiningOut />
        case "Extra tab":
            return <Nightlife />
        default:
            return <Delivery />
    }
};

export default HomePage;
