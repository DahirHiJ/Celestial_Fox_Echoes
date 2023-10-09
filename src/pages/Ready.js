import '../Themes/ReadyStyle.css'
export default function Ready(){
    function ToHome() {
        window.location.href = "/";
    }
    return(
        <>
        <body className="body">
            <div className="thank">
                <h1>Your video is ready</h1>
                <h1>Thank you for using Celestial Fox Echoes!</h1>
                <button className="button" onClick={ToHome}>Return to main page</button>
            </div>
        </body>
        </>
    );
}