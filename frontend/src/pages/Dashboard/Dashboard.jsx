import "./Dashboard.css";

import { useEffect, useState } from "react";

import api from "../../services/api";
import Sidebar from "../../components/Sidebar/Sidebar";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";

import { useAuth } from "../../contexts/AuthContext";

import ChartCard 
from "../../components/ChartCard/ChartCard";
import UsuariosChart 
from "../../components/Charts/UsuariosChart";
import EstoqueChart 
from "../../components/Charts/EstoqueChart";
import AgendamentosChart 
from "../../components/Charts/AgendamentosChart";
import AnimaisEspecieChart from "../../components/Charts/AnimaisEspecieChart";
import ConsultasVeterinarioChart 
from "../../components/Charts/ConsultasVeterinarioChart";
import VacinasVeterinarioChart 
from "../../components/Charts/VacinasVeterinarioChart";


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


                const resposta = await api.get(
                    "/dashboard/admin"
                );

                setDados(resposta.data);


            }


            else if(usuario?.perfil === "Veterinário"){


                const resposta = await api.get(
                    "/dashboard/veterinario"
                );


                console.log(
                    "Dashboard Veterinário:",
                    resposta.data
                );


                setDados(resposta.data);


            }


            else if(usuario?.perfil === "Cliente"){


                setDados({});


            }


        }


        catch(error){

            console.error(error);

            setErro(
                "Erro ao carregar o Dashboard."
            );

        }


        finally{

            setCarregando(false);

        }

    }

    if(carregando){
        return (

            <div className="loading-dashboard">

                ⏳ Carregando Dashboard...

            </div>

    );

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

                    <div className="dashboard-title">

                        <h1>
                            Dashboard {usuario?.perfil}
                        </h1>

                        <p>
                            Bem-vindo ao sistema Petonline24h
                        </p>

                    </div>


                    {

                    usuario?.perfil !== "Cliente" && (

                    <button
                        className="btn-refresh"
                        onClick={() => {

                            setCarregando(true);

                            carregarDashboard();

                        }}
                    >

                        🔄 Atualizar

                    </button>

                    )
                    }


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
                        titulo="Administradores"
                        valor={dados.administradores}
                        icone="👑"
                    />

                    <DashboardCard
                        titulo="Veterinários"
                        valor={dados.veterinarios}
                        icone="🩺"
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

                <DashboardSection  titulo="📊 análise">


                    <div className="chart-container">


                        <ChartCard titulo="Usuários por perfil">

                            <UsuariosChart dados={dados}/>

                        </ChartCard>


                        <ChartCard titulo="Situação do Estoque">

                            <EstoqueChart dados={dados}/>

                        </ChartCard>


                        <ChartCard titulo="Agendamentos da semana">

                            <AgendamentosChart dados={dados}/>

                        </ChartCard>

                        <ChartCard titulo="Animais por espécie">

                            <AnimaisEspecieChart dados={dados}/>

                        </ChartCard>

                    </div>


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
                        valor={dados.consultas_hoje}
                        icone="📅"
                    />


                    <DashboardCard
                        titulo="Próximas consultas"
                        valor={dados.proximas_consultas}
                        icone="🕒"
                    />


                    <DashboardCard
                        titulo="Atendimentos realizados"
                        valor={dados.atendimentos_realizados}
                        icone="📋"
                    />


                    <DashboardCard
                        titulo="Animais atendidos"
                        valor={dados.animais_atendidos}
                        icone="🐾"
                    />


                    <DashboardCard
                        titulo="Vacinas aplicadas"
                        valor={dados.vacinas_aplicadas}
                        icone="💉"
                    />


                    <DashboardCard
                        titulo="Próximas doses"
                        valor={dados.proximas_doses}
                        icone="💊"
                    />

                 </DashboardSection>    

                 <DashboardSection  titulo="📊 análise">


                    <div className="chart-container">

                            <ChartCard titulo="Consultas da semana">

                                <ConsultasVeterinarioChart 
                                    dados={dados}
                                />

                            </ChartCard>
                            
                            <ChartCard titulo="Controle de vacinas">

                                <VacinasVeterinarioChart
                                    dados={dados}
                                />

                            </ChartCard>


                            <ChartCard titulo="Agendamentos da semana">

                                <AgendamentosChart dados={dados}/>

                            </ChartCard>

                            <ChartCard titulo="Animais por espécie">

                                <AnimaisEspecieChart dados={dados}/>

                            </ChartCard>

                    </div>


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