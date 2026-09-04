import "./Sidebar.css";

import { useState } from "react";

import { menusPorPerfil } from "../../permissions/permissoes";

import { useNavigate } from "react-router-dom";
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
  { chave: "dashboard", label: "Dashboard", Icone: LayoutDashboard },
  { chave: "animais", label: "Animais", Icone: PawPrint },
  { chave: "meus_animais", label: "Meus Animais", Icone: Dog },
  { chave: "clientes", label: "Clientes", Icone: Users },
  { chave: "agendamentos", label: "Agendamentos", Icone: CalendarCheck },
  { chave: "minhas_consultas", label: "Minhas Consultas", Icone: CalendarCheck },
  { chave: "atendimentos", label: "Atendimentos", Icone: Stethoscope },
  { chave: "produtos", label: "Produtos", Icone: ShoppingCart },
  { chave: "compras", label: "Minhas Compras", Icone: ShoppingBag },
];

function Sidebar({ perfil, setSidebarAberto }) {
  const navigate = useNavigate();

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
          ({ chave, label, Icone }) => (
            <a key={chave} className={chave === "dashboard" ? "is-active" : ""}>
              <Icone size={20} />
              {aberto && <span>{label}</span>}
            </a>
          )
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
