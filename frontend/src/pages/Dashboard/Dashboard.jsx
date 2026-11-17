import './Dashboard.css'

import { useEffect, useState } from 'react'
import { RefreshCw } from 'lucide-react'

import api from '../../services/api'
import Sidebar from '../../components/Sidebar/Sidebar'

import { useAuth } from '../../contexts/AuthContext'

import AdminDashboard from './AdminDashboard'
import VeterinarioDashboard from './VeterinarioDashboard'
import ClienteDashboard from './ClienteDashboard'

const ENDPOINT_POR_PERFIL = {
  Administrador: '/dashboard/admin',
  Veterinário: '/dashboard/veterinario',
  Cliente: '/dashboard/cliente',
}

function Dashboard() {
  const { usuario } = useAuth()

  const [sidebarAberto, setSidebarAberto] = useState(true)

  const perfil = usuario?.perfil
  const endpoint = ENDPOINT_POR_PERFIL[perfil]

  // Incrementar força o dashboard a ser buscado de novo (botão "Atualizar").
  const [recarga, setRecarga] = useState(0)

  // Resultado da última busca, junto com a "chave" que o gerou.
  // Se a chave atual for diferente da guardada, ainda estamos carregando.
  const [resultado, setResultado] = useState({
    chave: null,
    dados: {},
    erro: '',
  })

  const chaveBusca = `${perfil}|${recarga}`

  useEffect(() => {
    if (!usuario || !endpoint) return

    // Se o perfil mudar antes da resposta chegar, ignora a resposta antiga.
    let ignorar = false

    api
      .get(endpoint)
      .then((resposta) => {
        if (ignorar) return
        setResultado({ chave: chaveBusca, dados: resposta.data, erro: '' })
      })
      .catch((error) => {
        if (ignorar) return
        console.error(error)
        setResultado({
          chave: chaveBusca,
          dados: {},
          erro: 'Erro ao carregar o Dashboard.',
        })
      })

    return () => {
      ignorar = true
    }
  }, [usuario, endpoint, chaveBusca])

  // Sem usuário fica no "carregando"; perfil sem endpoint mostra o painel vazio.
  const carregando = !usuario || (Boolean(endpoint) && resultado.chave !== chaveBusca)
  const dados = endpoint ? resultado.dados : {}
  const erro = carregando ? '' : endpoint ? resultado.erro : ''

  if (carregando) {
    return <div className="loading-dashboard">Carregando dashboard...</div>
  }

  return (
    <div className="dashboard">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`dashboard-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h1>Dashboard {usuario?.perfil}</h1>
            <p>Bem-vindo ao sistema Petonline24h</p>
          </div>

          <button className="btn-refresh" onClick={() => setRecarga((n) => n + 1)}>
            <RefreshCw size={16} />
            Atualizar
          </button>
        </header>

        {erro && <p className="dashboard-erro">{erro}</p>}

        {usuario?.perfil === 'Administrador' && <AdminDashboard dados={dados} />}
        {usuario?.perfil === 'Veterinário' && <VeterinarioDashboard dados={dados} />}
        {usuario?.perfil === 'Cliente' && <ClienteDashboard dados={dados} />}
      </main>
    </div>
  )
}

export default Dashboard
