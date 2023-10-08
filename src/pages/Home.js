import Logo from '../functions/logo.js'
import buttonStyle from '../Themes/button.js'
import webColor from '../Themes/themes.js'
import React, { useEffect } from 'react';

function Header(){
  const headerStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    padding: '20px',
    background: webColor.theme.backgroundColor,
    color: webColor.theme.color
  };

  const titleStyle = {
    textAlign: 'center',
  };

  const buttonContainerStyle = {
    display: 'flex',
    justifyContent: 'flex-end',
    alignItems: 'center'
  };

  function ToAbout(){
      window.location.href = "/About";
  }


  return (
    <header style={headerStyle}>
      <div>
        <Logo />
      </div>
      <div style={titleStyle}>
        <h2>Celestial Fox Echoes</h2>
        <h1>Listen to the Universe</h1>
      </div>
      <div style={buttonContainerStyle}>
      <button style={buttonStyle}>Upload</button>
      <button style={buttonStyle} onClick={ToAbout}>About</button>
      </div>
    </header>
  );
}

function Body(){
  const BodyStyle = {
    background: webColor.theme.backgroundColor,
    color: webColor.theme.color
  };
  const EvenlySpacedStyle ={
     display: 'flex', 
     justifyContent: 'space-between'
  };
  const LinkStyle = {
    color: 'white',
    fontSize: '2rem',
  };
  return(
    <div style = {BodyStyle}>
      <video width="100%" height="470" controls src='/resources/videos/TestVideoNASA.mp4'/>
      <a href="#videosSection" className="scroll-link-button" style={LinkStyle}>
        Explore other videos
      </a>
      <div id="videosSection" style={EvenlySpacedStyle}>
        <video width="30%" height="300" controls src='/resources/videos/TestVideoNASA2.mp4' />
        <video width="30%" height="300" controls src='/resources/videos/TestVideoNASA2.mp4' />
        <video width="30%" height="300" controls src='/resources/videos/TestVideoNASA2.mp4' />
      </div>
    </div>
  )
}





export default function Home() {
  useEffect(() => {
    const isRefreshed = performance.getEntriesByType("navigation")[0].type === "reload";
    if (isRefreshed) {
      window.location.href = "/";
    }
  }, []);
  return (
      <>
        {Header()}
        {Body()}
      </>
  );
}