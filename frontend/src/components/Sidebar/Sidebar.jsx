import './Sidebar.css'

import { useEffect, useState } from 'react'

import { menusPorPerfil } from '../../permissions/permissoes'

import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../contexts/AuthContext'

import {
  Menu,
  LayoutDashboard,
  PawPrint,
  Dog,
  Users,
  CalendarCheck,
  Stethoscope,
  Syringe,
  ShoppingCart,
  ShoppingBag,
  UserRound,
  LogOut,
} from 'lucide-react'

// "curto" é o rótulo usado na barra inferior do celular (espaço pequeno).
const ITENS_MENU = [
  {
    chave: 'dashboard',
    label: 'Dashboard',
    curto: 'Início',
    Icone: LayoutDashboard,
    rota: '/dashboard',
  },
  {
    chave: 'animais',
    label: 'Animais',
    curto: 'Animais',
    Icone: PawPrint,
    rota: '/animais',
  },
  {
    chave: 'meus_animais',
    label: 'Meus Animais',
    curto: 'Pets',
    Icone: Dog,
    rota: '/meus-animais',
  },
  {
    chave: 'clientes',
    label: 'Clientes',
    curto: 'Clientes',
    Icone: Users,
    rota: '/clientes',
  },
  {
    chave: 'agendamentos',
    label: 'Agendamentos',
    curto: 'Agenda',
    Icone: CalendarCheck,
    rota: '/agendamentos',
  },
  {
    chave: 'minhas_consultas',
    label: 'Minhas Consultas',
    curto: 'Consultas',
    Icone: CalendarCheck,
    rota: '/minhas-consultas',
  },
  {
    chave: 'atendimentos',
    label: 'Atendimentos',
    curto: 'Atend.',
    Icone: Stethoscope,
    rota: '/atendimentos',
  },
  {
    chave: 'vacinas',
    label: 'Vacinas',
    curto: 'Vacinas',
    Icone: Syringe,
    rota: '/vacinas',
  },
  {
    chave: 'produtos',
    label: 'Produtos',
    curto: 'Loja',
    Icone: ShoppingCart,
    rota: '/produtos',
  },
  {
    chave: 'compras',
    label: 'Minhas Compras',
    curto: 'Compras',
    Icone: ShoppingBag,
    rota: '/compras',
  },
]

// Acompanha uma media query (ex.: tela de celular) e reage quando ela muda.
function useMediaQuery(consulta) {
  const [corresponde, setCorresponde] = useState(
    () => window.matchMedia(consulta).matches
  )

  useEffect(() => {
    const lista = window.matchMedia(consulta)
    const atualizar = () => setCorresponde(lista.matches)

    atualizar()
    lista.addEventListener('change', atualizar)
    return () => lista.removeEventListener('change', atualizar)
  }, [consulta])

  return corresponde
}

function Rotulo({ label, curto }) {
  return (
    <>
      <span className="rotulo-longo">{label}</span>
      <span className="rotulo-curto">{curto}</span>
    </>
  )
}

function Sidebar({ perfil, setSidebarAberto }) {
  const navigate = useNavigate()
  const location = useLocation()

  const { logout } = useAuth()

  const [aberto, setAberto] = useState(true)

  // No celular o menu vira uma barra inferior e sempre mostra os rótulos.
  const ehMobile = useMediaQuery('(max-width: 768px)')
  const mostrarRotulo = aberto || ehMobile

  function sair() {
    logout()
    navigate('/login')
  }

  function alternarSidebar() {
    setAberto(!aberto)
    setSidebarAberto(!aberto)
  }

  const permissoes = menusPorPerfil[perfil] || []

  return (
    <aside
      className={`sidebar ${aberto ? 'aberto' : 'fechado'}`}
      aria-label="Menu principal"
    >
      <button className="toggle" onClick={alternarSidebar} aria-label="Alternar menu">
        <Menu size={22} />
      </button>

      <div className="brand">
        <PawPrint size={22} />
        {aberto && <span>Petonline</span>}
      </div>

      <nav>
        {ITENS_MENU.filter((item) => permissoes.includes(item.chave)).map(
          ({ chave, label, curto, Icone, rota }) => {
            const ativo = rota && location.pathname === rota

            if (rota) {
              return (
                <Link
                  key={chave}
                  to={rota}
                  className={ativo ? 'is-active' : ''}
                  aria-current={ativo ? 'page' : undefined}
                >
                  <Icone size={20} />
                  {mostrarRotulo && <Rotulo label={label} curto={curto} />}
                </Link>
              )
            }

            // Ainda sem página própria: mantém visível, sem navegar.
            return (
              <a key={chave} className="em-breve" title="Em breve">
                <Icone size={20} />
                {mostrarRotulo && <Rotulo label={label} curto={curto} />}
              </a>
            )
          }
        )}

        <Link
          to="/perfil"
          className={`item-perfil ${
            location.pathname === '/perfil' ? 'is-active' : ''
          }`}
          aria-current={location.pathname === '/perfil' ? 'page' : undefined}
        >
          <UserRound size={20} />
          {mostrarRotulo && <Rotulo label="Perfil" curto="Perfil" />}
        </Link>
      </nav>

      <button className="logout" onClick={sair}>
        <LogOut size={18} />
        {mostrarRotulo && <span>Sair</span>}
      </button>
    </aside>
  )
}

export default Sidebar
