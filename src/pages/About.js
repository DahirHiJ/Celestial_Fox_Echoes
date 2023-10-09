import React from 'react';
import Box from '../functions/Box'
import '../Themes/AboutStyle.css';

export default function About() {
  return (
    <div className="wrapper">
      <h2>About Celestial Fox Echoes</h2>
      <h2>Click on the boxes for information!</h2>
      <div className="Boxes">
      <Box
          imgSrc="/resources/images/Img1.png"
          title="Description"
          role="Who we are?"
          info="We are a group of university students who want to share the beauty of the universe with audio."
        />
        <Box
          imgSrc="/resources/images/Img2.png"
          title="Space Apps"
          role="Why?"
          info="We created this project to participate in Space Apps 2023 to improve our programming abilities."
        />
        <Box
          imgSrc="/resources/images/Img3.jpg"
          title="Credits"
          role="How?"
          info="We use sonification technologies available in the web as well as NASA's videos."
        />
      </div>
    </div>
  );
}
