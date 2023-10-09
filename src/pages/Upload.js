import React, {ChangeEvent, useState} from 'react';
import '../Themes/UploadStyle.css'

export default function Upload(){
    function ToProcessing(){
        window.location.href = "/Processing";
    }
    return (
        <div className="wrapperUp">
            <header>Instrucctions</header>
            <div>
                <h1>Put the file in the path:</h1>
                <h2>celestial-fox-echoes/public/input</h2>
                <button onClick={ToProcessing}>Ready</button>
            </div>
        </div>
  );
}
