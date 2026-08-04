import "./Cadastro.css";

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

import logo from "../../assets/logo.png";

import Input from "../../components/Input/Input";
import Button from "../../components/Button/Button";

function Cadastro(){

    const navigate = useNavigate();


    const [nome,setNome] = useState("");
    const [cpf,setCpf] = useState("");
    const [telefone,setTelefone] = useState("");
    const [email,setEmail] = useState("");
    const [endereco,setEndereco] = useState("");
    const [senha,setSenha] = useState("");

    const [erro,setErro] = useState("");
    const [sucesso,setSucesso] = useState("");

    const [carregando,setCarregando] = useState(false);



    async function cadastrar(e){

        e.preventDefault();


        setErro("");
        setSucesso("");
        setCarregando(true);


        try{


            await axios.post(

                "http://127.0.0.1:8000/cadastro/",

                {
                    nome,
                    cpf,
                    telefone,
                    email,
                    endereco,
                    senha
                }

            );


            setSucesso(
                "Cadastro realizado com sucesso!"
            );


            setTimeout(()=>{

                navigate("/login");

            },2000);



        }


        catch(error){


            console.error(
                "Erro cadastro:",
                error.response
            );



            if(error.response){


                const detalhe =
                error.response.data?.detail;



                // Erros de validação FastAPI
                if(Array.isArray(detalhe)){


                    setErro(

                        detalhe
                        .map(item => {

                            if(item.campo){

                                return `${item.campo}: ${item.mensagem}`;

                            }


                            return item.msg;

                        })

                        .join("\n")

                    );


                }



                // Erros das regras de negócio
                else if(detalhe){


                    setErro(
                        detalhe
                    );


                }



                else{


                    setErro(
                        `Erro ${error.response.status}: Não foi possível cadastrar.`
                    );


                }



            }


            else{


                setErro(
                    "Servidor indisponível."
                );


            }



        }


        finally{

            setCarregando(false);

        }


    }



return (

    <div className="cadastro">


        <div className="cadastro-info">


            <img 
                src={logo}
                className="logo-poas"
                alt="Logo POAS"
            />


            <h2>
                Cuidado completo para seu pet
            </h2>


            <p className="descricao-poas">

                Agende consultas, acompanhe
                históricos e cuide melhor
                do seu animal.

            </p>


        </div>




        <div className="cadastro-box">


            <h1>
                Criar Conta
            </h1>


            <p className="subtitulo">

                Cadastre-se no Petonline24

            </p>




            <form onSubmit={cadastrar}>


                {erro && (

                    <div className="mensagem erro">

                        <strong>
                            ❌ Erro:
                        </strong>

                        <span>
                            {erro}
                        </span>

                    </div>

                )}




                {sucesso && (

                    <div className="mensagem sucesso">

                        ✅ {sucesso}

                    </div>

                )}




                <Input
                    placeholder="Nome completo"
                    value={nome}
                    onChange={
                        e=>setNome(e.target.value)
                    }
                />



                <Input
                    placeholder="CPF"
                    value={cpf}
                    onChange={
                        e=>setCpf(e.target.value)
                    }
                />



                <Input
                    placeholder="Telefone"
                    value={telefone}
                    onChange={
                        e=>setTelefone(e.target.value)
                    }
                />



                <Input
                    placeholder="Email"
                    type="email"
                    value={email}
                    onChange={
                        e=>setEmail(e.target.value)
                    }
                />



                <Input
                    placeholder="Endereço"
                    value={endereco}
                    onChange={
                        e=>setEndereco(e.target.value)
                    }
                />



                <Input
                    placeholder="Senha"
                    type="password"
                    value={senha}
                    onChange={
                        e=>setSenha(e.target.value)
                    }
                />




                <Button disabled={carregando}>

                    {
                        carregando
                        ?
                        "Cadastrando..."
                        :
                        "Criar conta"
                    }

                </Button>


            </form>




            <button

                className="voltar"

                onClick={()=>navigate("/login")}

            >

                Já tenho conta

            </button>



        </div>


    </div>

    );
}
export default Cadastro;