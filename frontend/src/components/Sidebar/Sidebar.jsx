import "./Sidebar.css";

import { useState } from "react";

import { menusPorPerfil } from "../../permissions/permissoes";

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";

import {
  Menu,
  LayoutDashboard,
  PawPrint,
  Dog,
  Users,
  CalendarCheck,
  Stethoscope,
  ShoppingCart,
  ShoppingBag,
  Settings,
  LogOut,
} from "lucide-react";

const ITENS_MENU = [
  { chave: "dashboard", label: "Dashboard", Icone: LayoutDashboard, rota: "/dashboard" },
  { chave: "animais", label: "Animais", Icone: PawPrint, rota: "/animais" },
  { chave: "meus_animais", label: "Meus Animais", Icone: Dog, rota: "/meus-animais" },
  { chave: "clientes", label: "Clientes", Icone: Users, rota: null },
  { chave: "agendamentos", label: "Agendamentos", Icone: CalendarCheck, rota: null },
  { chave: "minhas_consultas", label: "Minhas Consultas", Icone: CalendarCheck, rota: "/minhas-consultas" },
  { chave: "atendimentos", label: "Atendimentos", Icone: Stethoscope, rota: null },
  { chave: "produtos", label: "Produtos", Icone: ShoppingCart, rota: null },
  { chave: "compras", label: "Minhas Compras", Icone: ShoppingBag, rota: "/compras" },
];

function Sidebar({ perfil, setSidebarAberto }) {
  const navigate = useNavigate();
  const location = useLocation();

  const { logout } = useAuth();

  const [aberto, setAberto] = useState(true);

  function sair() {
    logout();
    navigate("/login");
  }

  function alternarSidebar() {
    setAberto(!aberto);
    setSidebarAberto(!aberto);
  }

  const permissoes = menusPorPerfil[perfil] || [];

  return (
    <aside className={`sidebar ${aberto ? "aberto" : "fechado"}`}>
      <button className="toggle" onClick={alternarSidebar} aria-label="Alternar menu">
        <Menu size={22} />
      </button>

      <div className="brand">
        <PawPrint size={22} />
        {aberto && <span>Petonline</span>}
      </div>

      <nav>
        {ITENS_MENU.filter((item) => permissoes.includes(item.chave)).map(
          ({ chave, label, Icone, rota }) => {
            const ativo = rota && location.pathname === rota;

            if (rota) {
              return (
                <Link key={chave} to={rota} className={ativo ? "is-active" : ""}>
                  <Icone size={20} />
                  {aberto && <span>{label}</span>}
                </Link>
              );
            }

            // Ainda sem página própria: mantém visível, sem navegar.
            return (
              <a key={chave} className="em-breve" title="Em breve">
                <Icone size={20} />
                {aberto && <span>{label}</span>}
              </a>
            );
          }
        )}

        <a>
          <Settings size={20} />
          {aberto && <span>Perfil</span>}
        </a>
      </nav>

      <button className="logout" onClick={sair}>
        <LogOut size={18} />
        {aberto && <span>Sair</span>}
      </button>
    </aside>
  );
}

export default Sidebar;
