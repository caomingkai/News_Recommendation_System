import 'materialize-css/dist/css/materialize.min.css';
import 'materialize-css/dist/js/materialize.min.js';

import React, { Component } from 'react';
import logo from './logo.png';
import './App.css'; // 1. 每个component都有自己的一个css样式

import NewsPanel from '../NewsPanel/NewsPanel';



class App extends Component {
  render() {
    return (
      <div >
        <img src={logo} className="logo" alt="logo" />
        <div className="container">
            <NewsPanel />

        </div>
      </div>
    );
  }
}

export default App;
