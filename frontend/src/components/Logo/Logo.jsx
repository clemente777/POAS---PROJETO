import "./Logo.css";

import logo from "../../assets/logo.png";


function Logo(){

    return(

        <img
            className="logo"
            src={logo}
            alt="Logo"
        />

    )

}


export default Logo;