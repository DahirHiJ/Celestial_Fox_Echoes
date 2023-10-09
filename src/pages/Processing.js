import React, { useState, useEffect } from 'react';
import '../Themes/BarStyle.css'
export default function Processing() {
    const [progress, setProgress] = useState(0);
  
    useEffect(() => {
      const interval = setInterval(() => {
        if (progress < 100) {
          setProgress(progress + 1);
        } else {
            clearInterval(interval);
            window.location.href = "/Ready";
        }
      }, 100);
  
      return () => clearInterval(interval);
    }, [progress]);
  
    const h1 = {
        display: 'flex',
        justifyContent: 'center',
        color: '#FFFFFF',
        fontsize: '24px',
        fontweight: '600',
        textalign: 'center'
    }
    return (
        <div >
            <h1 style={h1}>Loading...</h1>
            <progress  className="progress-bar" value={progress} max={100} />
        </div>
    );
  }