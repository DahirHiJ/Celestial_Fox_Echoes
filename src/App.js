import Logo from './functions/logo.js'
import Button from './functions/button.js'
import webColor from './themes.js'


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
        <Button text='Upload'/>
        <Button text='About' />
      </div>
    </header>
  );
}

function Body(){
  const BodyStyle = {
    background: webColor.theme.backgroundColor,
    color: webColor.theme.color
  };
  return(
    <div style = {BodyStyle}>
      <video width="100%" height="500" controls src='/resources/videos/TestVideoNASA.mp4' />
      <h1>saddad</h1>
    </div>
  )
}


export default function Main() {
  return (
      <>
      {Header()}
      {Body()}
      </>
  );
}