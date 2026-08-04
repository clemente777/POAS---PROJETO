import "./Dashboard.css";

import { useEffect, useState } from "react";

import api from "../../services/api";
import Sidebar from "../../components/Sidebar/Sidebar";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";

import { useAuth } from "../../contexts/AuthContext";

function Dashboard() {

    const { usuario } = useAuth();

    const [sidebarAberto, setSidebarAberto] = useState(true);

    const [dados, setDados] = useState({});

    const [carregando, setCarregando] = useState(true);

    const [erro, setErro] = useState("");
    

    useEffect(() => {

        if(usuario){

            carregarDashboard();

        }

    }, [usuario]);


async function carregarDashboard() {

    try {


        if(usuario?.perfil === "Administrador"){


            const resposta = await api.get("/dashboard/");

            setDados(resposta.data);


        } 
        else {


            setDados({});


        }


    }

    catch(error){

        console.error(error);

        setErro("Erro ao carregar o Dashboard.");

    }

    finally{

        setCarregando(false);

    }

}

    
    return (

        <div className="dashboard">

            <Sidebar 
                perfil={usuario?.perfil}
                setSidebarAberto={setSidebarAberto}
            />

            <main 
                className={`dashboard-content ${
                    sidebarAberto ? "aberto" : "fechado"
                }`}
            >

                <header className="dashboard-header">

                    <h1>
                        Dashboard {usuario?.perfil}
                    </h1>

                    <p>

                        Bem-vindo ao sistema Petonline24h

                    </p>

                </header>

                {
                usuario?.perfil === "Administrador" && (
                <>
                <DashboardSection titulo="📊 Estatísticas Gerais">

                    <DashboardCard
                        titulo="Usuários"
                        valor={dados.usuarios}
                        icone="👤"
                    />

                    <DashboardCard
                        titulo="Clientes"
                        valor={dados.clientes}
                        icone="👥"
                    />

                    <DashboardCard
                        titulo="Animais"
                        valor={dados.animais}
                        icone="🐾"
                    />

                    <DashboardCard
                        titulo="Agendamentos"
                        valor={dados.agendamentos}
                        icone="📅"
                    />

                    <DashboardCard
                        titulo="Atendimentos"
                        valor={dados.atendimentos}
                        icone="🩺"
                    />

                    <DashboardCard
                        titulo="Produtos"
                        valor={dados.produtos}
                        icone="🛒"

                    
                    />

                </DashboardSection>



                <DashboardSection titulo="📦 Estoque">

                    <DashboardCard
                        titulo="Valor Total"
                        valor={`R$ ${dados.valor_total_estoque}`}
                        icone="💰"
                    />

                    <DashboardCard
                        titulo="Estoque Baixo"
                        valor={dados.estoque_baixo}
                        icone="⚠️"
                    />

                    <DashboardCard
                        titulo="Sem Estoque"
                        valor={dados.produtos_sem_estoque}
                        icone="❌"
                    />

                </DashboardSection>



                <DashboardSection titulo="📅 Agenda">

                    <DashboardCard
                        titulo="Hoje"
                        valor={dados.agendamentos_hoje}
                        icone="📅"
                    />

                    <DashboardCard
                        titulo="Futuros"
                        valor={dados.agendamentos_futuros}
                        icone="🗓️"
                    />

                </DashboardSection>

                <DashboardSection titulo="🐾 Animais">

                    <DashboardCard
                        titulo="Animal mais velho"
                        valor={dados.animal_mais_velho?.nome || "-"}
                        icone="🐶"
                    />

                    <DashboardCard
                        titulo="Idade"
                        valor={dados.animal_mais_velho?.idade || "-"}
                        icone="🎂"
                    />

                    <DashboardCard
                        titulo="Média de idade"
                        valor={dados.media_idade_animais}
                        icone="📈"
                    />

                </DashboardSection>

                <DashboardSection titulo="👥 Clientes">

                    <DashboardCard
                        titulo="Cliente com mais animais"
                        valor={dados.cliente_com_mais_animais?.nome || "-"}
                        icone="👤"
                    />

                    <DashboardCard
                        titulo="Quantidade"
                        valor={dados.cliente_com_mais_animais?.quantidade || 0}
                        icone="🐾"
                    />

                </DashboardSection>

                </>

                )
                }
                {
                usuario?.perfil === "Veterinário" && (
                <>
                <DashboardSection titulo="🩺 Área do Veterinário">

                    <DashboardCard
                        titulo="Consultas hoje"
                        valor="0"
                        icone="📅"
                    />

                    <DashboardCard
                        titulo="Próximos atendimentos"
                        valor="0"
                        icone="🕒"
                    />

                    <DashboardCard
                        titulo="Animais atendidos"
                        valor="0"
                        icone="🐾"
                    />

                    <DashboardCard
                        titulo="Históricos"
                        valor="0"
                        icone="📋"
                    />

            </DashboardSection>
                </>
                )
                }
                {
                usuario?.perfil === "Cliente" && (
                    <>
                    <DashboardSection titulo="🐾 Minha Área">

                        <DashboardCard
                            titulo="Meus Animais"
                            valor="0"
                            icone="🐶"
                        />

                        <DashboardCard
                            titulo="Minhas Consultas"
                            valor="0"
                            icone="📅"
                        />

                        <DashboardCard
                            titulo="Minhas Compras"
                            valor="0"
                            icone="🛒"
                        />
                 </DashboardSection> 
                 
                </>       
                )
                }
                   
            </main>

        </div>

    );

}

export default Dashboard;