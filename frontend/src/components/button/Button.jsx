import "./Button.css";


function Button({children}){


    return (

        <button 
            className="button"
            type="submit"
        >

            {children}

        </button>

    );


}


export default Button;