import "./Login.css";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import logo from "../../assets/logo.png";
import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";

import { useAuth } from "../../contexts/AuthContext";


function Login() {

    const navigate = useNavigate();
    
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [mensagemErro, setMensagemErro] = useState("");

    async function entrar(e) {

        e.preventDefault();

        try {

            const dados = new URLSearchParams();

            dados.append("username", email);
            dados.append("password", senha);

            const resposta = await axios.post(

                "http://127.0.0.1:8000/login/",

                dados,

                {

                    headers: {

                        "Content-Type":
                        "application/x-www-form-urlencoded"

                    }

                }

            );

            localStorage.setItem(
                "token",
                resposta.data.access_token
            );


            login(
                resposta.data.usuario
            );

            setMensagemErro("");

            navigate("/dashboard");

        }

        catch (erro) {

            console.error(
                "Erro login:",
                erro.response
            );


            if (erro.response) {


                const detalhe = erro.response.data?.detail;


                if (Array.isArray(detalhe)) {

                    setMensagemErro(
                        detalhe
                        .map(item => item.msg)
                        .join(", ")
                    );

                }


                else if (detalhe) {

                    setMensagemErro(detalhe);

                }


                else {

                    setMensagemErro(
                        `Erro ${erro.response.status}`
                    );

                }


            } 
            
            else {

                setMensagemErro(
                    "Servidor indisponível."
                );

            }

        }
}
    return (

        <div className="login">

            <div className="left">

                <img
                    src={logo}
                    alt="Logo"
                />

            </div>

            <div className="right">

                <div className="box">

                    <h1>Bem-Vindo!</h1>

                    <form onSubmit={entrar}>
                        
                        {mensagemErro && (
                            <p className="erro-login">
                                {mensagemErro}
                            </p>
                        )}

                        <Input
                            type="email"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                        />

                        <Input
                            type="password"
                            placeholder="Senha"
                            value={senha}
                            onChange={(e) => setSenha(e.target.value)}
                        />

                        <Button>

                            Entrar

                        </Button>

                    
                    </form>

                    <div className="links">

                        <a href="/cadastro">
                            Criar conta
                        </a>

                        <a href="#">Esqueci minha senha</a>

                    </div>

                </div>

            </div>

        </div>

    );

}

export default Login;