import "./Home.css";

import { Link } from "react-router-dom";

import vetImage from "../../assets/vet-home.jpg";

import Navbar from "../../components/Navbar/Navbar";


function Home() {

    return (

        <div className="home">


            <Navbar />



            <section className="hero">


                <div className="hero-text">


                    <h1>
                        Cuidando do seu pet
                        <br />
                        com tecnologia e carinho
                    </h1>



                    <p>
                        Um sistema completo para clínicas veterinárias.
                        Controle animais, consultas e atendimentos
                        em um único lugar.
                    </p>



                    <div className="hero-buttons">


                        <Link 
                            to="/login"
                            className="primary"
                        >
                            Acessar sistema
                        </Link>



                        <a 
                            href="#servicos"
                            className="secondary"
                        >
                            Conheça nossos serviços
                        </a>


                    </div>


                </div>





                <div className="hero-image">


                    <img
                        src={vetImage}
                        alt="Veterinário atendendo um animal"
                    />


                </div>


            </section>





            <section 
                className="services"
                id="servicos"
            >

                <h2>
                    Nossos serviços
                </h2>


                <div className="service-grid">


                    <div className="service-card">

                        <span>
                            🐶
                        </span>

                        <h3>
                            Gestão de Animais
                        </h3>

                        <p>
                            Cadastro completo dos pacientes.
                        </p>

                    </div>



                    <div className="service-card">

                        <span>
                            📅
                        </span>

                        <h3>
                            Agendamentos
                        </h3>

                        <p>
                            Controle consultas e horários.
                        </p>

                    </div>



                    <div className="service-card">

                        <span>
                            🩺
                        </span>

                        <h3>
                            Atendimentos
                        </h3>

                        <p>
                            Histórico médico organizado.
                        </p>

                    </div>


                </div>


            </section>






            <section 
                className="about"
                id="sobre"
            >

                <h2>
                    Tecnologia para cuidar melhor
                </h2>


                <p>
                    O POAS ajuda clínicas veterinárias
                    a organizarem sua rotina,
                    melhorarem o atendimento e
                    acompanharem cada paciente.
                </p>


            </section>






            <footer id="contato">

                🐾 POAS Clínica Veterinária

            </footer>



        </div>

    );

}


export default Home;