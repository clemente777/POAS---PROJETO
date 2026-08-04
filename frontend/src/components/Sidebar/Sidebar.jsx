import "./Sidebar.css";

import { useState } from "react";

import { menusPorPerfil } from "../../permissions/permissoes";

import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";


function Sidebar({ perfil, setSidebarAberto }) {

    const navigate = useNavigate();

    const { logout } = useAuth();

    const [aberto, setAberto] = useState(true);


    function sair(){

        logout();

        navigate("/login");

    }
    function alternarSidebar(){

        setAberto(!aberto);

        setSidebarAberto(!aberto);

    }



    const permissoes = menusPorPerfil[perfil] || [];



    return (

        <aside 
            className={`sidebar ${aberto ? "aberto" : "fechado"}`}
        >


            <button
                className="toggle"
                onClick={alternarSidebar}
            >

                ☰

            </button>



            <div className="brand">

                {aberto ? "🐾 Petonline" : "🐾"}

            </div>



            <nav>


                {permissoes.includes("dashboard") && (

                    <a>
                        📊
                        {aberto && " Dashboard"}
                    </a>

                )}




                {permissoes.includes("animais") && (

                    <a>
                        🐾
                        {aberto && " Animais"}
                    </a>

                )}

                {permissoes.includes("meus_animais") && (

                    <a>
                        🐶
                        {aberto && " Meus Animais"}
                    </a>

                )}




                {permissoes.includes("clientes") && (

                    <a>
                        👥
                        {aberto && " Clientes"}
                    </a>

                )}




                {permissoes.includes("agendamentos") && (

                    <a>
                        📅
                        {aberto && " Agendamentos"}
                    </a>

                )}

                {permissoes.includes("minhas_consultas") && (

                    <a>
                        📅
                        {aberto && " Minhas Consultas"}
                    </a>

                )}


                {permissoes.includes("atendimentos") && (

                    <a>
                        🩺
                        {aberto && " Atendimentos"}
                    </a>

                )}




                {permissoes.includes("produtos") && (

                    <a>
                        🛒
                        {aberto && " Produtos"}
                    </a>

                )}

                {permissoes.includes("compras") && (

                    <a>
                        🛍️
                        {aberto && " Minhas Compras"}
                    </a>

                )}

                <a>
                    ⚙️
                    {aberto && " Perfil"}
                </a>



            </nav>



            <button 
                className="logout"
                onClick={sair}
            >

                🚪
                {aberto && " Sair"}

            </button>



        </aside>

    );

}


export default Sidebar;