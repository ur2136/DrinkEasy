import React from 'react';
import './header.css';
import logo from './logo.png';
import Geosuggest from 'react-geosuggest';

const Header = () => {
    return (
        <div className="max-width header">
            <img src={logo} alt="DrinkEasy-logo" className="header-logo" />
            <div className="header-right">
                <div className='header-location-search-container'> 
                    <div className='location-wrapper'>
                        <div className="location-icon-name">
                            <i className="fi fi-rr-marker absolute-center location-icon"></i>
                            <div>Manhattan</div>
                        </div>
                        <i className="fi fi-rr-caret-down absolute-center"></i>
                    </div>
                    <div className="location-search-separator"></div>
                    <div className="header-search-bar">
                        <i className="fi fi-rr-search absolute-center search-icon"></i>
                        <input type = "text" placeholder='Search for particular zipcode' id = "loc" name = "loc" className='search-input'/>
    
                        
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Header;
