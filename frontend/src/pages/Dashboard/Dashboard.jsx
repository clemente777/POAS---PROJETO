import "./Dashboard.css";

import { useEffect, useState } from "react";
import { RefreshCw } from "lucide-react";

import api from "../../services/api";
import Sidebar from "../../components/Sidebar/Sidebar";

import { useAuth } from "../../contexts/AuthContext";

import AdminDashboard from "./AdminDashboard";
import VeterinarioDashboard from "./VeterinarioDashboard";
import ClienteDashboard from "./ClienteDashboard";

const ENDPOINT_POR_PERFIL = {
  Administrador: "/dashboard/admin",
  "Veterinário": "/dashboard/veterinario",
  Cliente: "/dashboard/cliente",
};

function Dashboard() {
  const { usuario } = useAuth();

  const [sidebarAberto, setSidebarAberto] = useState(true);
  const [dados, setDados] = useState({});
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    if (usuario) {
      carregarDashboard();
    }
  }, [usuario]);

  async function carregarDashboard() {
    const endpoint = ENDPOINT_POR_PERFIL[usuario?.perfil];

    if (!endpoint) {
      setDados({});
      setCarregando(false);
      return;
    }

    try {
      const resposta = await api.get(endpoint);
      setDados(resposta.data);
      setErro("");
    } catch (error) {
      console.error(error);
      setErro("Erro ao carregar o Dashboard.");
    } finally {
      setCarregando(false);
    }
  }

  if (carregando) {
    return <div className="loading-dashboard">Carregando dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`dashboard-content ${sidebarAberto ? "aberto" : "fechado"}`}>
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h1>Dashboard {usuario?.perfil}</h1>
            <p>Bem-vindo ao sistema Petonline24h</p>
          </div>

          <button
            className="btn-refresh"
            onClick={() => {
              setCarregando(true);
              carregarDashboard();
            }}
          >
            <RefreshCw size={16} />
            Atualizar
          </button>
        </header>

        {erro && <p className="dashboard-erro">{erro}</p>}

        {usuario?.perfil === "Administrador" && <AdminDashboard dados={dados} />}
        {usuario?.perfil === "Veterinário" && <VeterinarioDashboard dados={dados} />}
        {usuario?.perfil === "Cliente" && <ClienteDashboard dados={dados} />}
      </main>
    </div>
  );
}

export default Dashboard;
