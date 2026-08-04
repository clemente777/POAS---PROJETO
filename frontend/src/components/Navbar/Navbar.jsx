import "./Navbar.css";
import { Link } from "react-router-dom";


function Navbar() {

    return (

        <header className="navbar">


            <div className="logo">
                🐾 POAS
            </div>



            <nav>


                <Link 
                    to="/"
                    className="nav-link"
                >
                    Início
                </Link>



                <a 
                    href="#servicos"
                    className="nav-link"
                >
                    Serviços
                </a>



                <a 
                    href="#sobre"
                    className="nav-link"
                >
                    Sobre
                </a>



                <a 
                    href="#contato"
                    className="nav-link"
                >
                    Contato
                </a>




                <Link
                    to="/login"
                    className="btn-login"
                >
                    Entrar
                </Link>


            </nav>


        </header>

    );

}


export default Navbar;