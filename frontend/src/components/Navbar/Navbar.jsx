import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Navbar.css";
import Logo from "../Logo/Logo";

function Navbar() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header className={`navbar ${scrolled ? "is-scrolled" : ""}`}>
      <Link to="/" className="navbar-brand">
        <Logo />
      </Link>

      <nav>
        <Link to="/" className="nav-link">
          Início
        </Link>

        <a href="#servicos" className="nav-link">
          Serviços
        </a>

        <a href="#cobertura" className="nav-link">
          Cobertura
        </a>

        <a href="#sobre" className="nav-link">
          Sobre
        </a>

        <a href="#contato" className="nav-link">
          Contato
        </a>

        <Link to="/login" className="btn-login">
          Entrar
        </Link>
      </nav>
    </header>
  );
}

export default Navbar;
