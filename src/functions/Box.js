import React, { useState } from 'react';

function Box({ imgSrc, title, role, info }) {
  const [showInfo, setShowInfo] = useState(false);

  const toggleInfo = () => {
    setShowInfo(!showInfo);
  };

  return (
    <button className="box" onClick={toggleInfo}>
      <div className="box_img">
        <img src={imgSrc} alt={title} />
      </div>
      <h3>{title}</h3>
      <p className="role">{role}</p>
      {showInfo && <div className="box-info">{info}</div>}
    </button>
  );
}

export default Box;