
import './Dashboard.css'

import { Navigate } from 'react-router-dom'
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
  const [recarga, setRecarga] = useState(0)

  const perfil = usuario?.perfil
  const endpoint = ENDPOINT_POR_PERFIL[perfil]

  const [resultado, setResultado] = useState({
    chave: null,
    dados: {},
    erro: '',
  })

  const chaveBusca = `${perfil}|${recarga}`

  useEffect(() => {
    // Sem endpoint, não existe requisição a realizar.
    if (!endpoint) return

    let ignorar = false

    async function buscarDashboard() {
      try {
        const resposta = await api.get(endpoint)

        if (ignorar) return

        setResultado({
          chave: chaveBusca,
          dados: resposta.data,
          erro: '',
        })
      } catch (error) {
        if (ignorar) return

        console.error('Erro ao carregar dashboard:', error)

        setResultado({
          chave: chaveBusca,
          dados: {},
          erro: 'Erro ao carregar o Dashboard.',
        })
      }
    }

    buscarDashboard()

    return () => {
      ignorar = true
    }
  }, [endpoint, chaveBusca])

  const carregando =
    !usuario ||
    (Boolean(endpoint) && resultado.chave !== chaveBusca)

  const dados = endpoint ? resultado.dados : {}
  const erro = carregando ? '' : endpoint ? resultado.erro : ''

  const ehCliente = perfil === 'Cliente'

  const primeiroNome = (
    usuario?.nome || usuario?.name || ''
  ).trim().split(' ')[0]

    // Impede acesso ao dashboard sem usuário autenticado.
  if (!usuario || !localStorage.getItem('token')) {
    return <Navigate to="/login" replace />
  }

  if (carregando) {
    return (
      <div className="loading-dashboard">
        Carregando dashboard...
      </div>
    )
  }

  return (
    <div className="dashboard">
      <Sidebar
        perfil={perfil}
        setSidebarAberto={setSidebarAberto}
      />

      <main
        className={`dashboard-content ${
          sidebarAberto ? 'aberto' : 'fechado'
        }`}
      >
        <header className="dashboard-header">
          <div className="dashboard-title">
            {ehCliente ? (
              <>
                <h1>
                  Olá{primeiroNome ? `, ${primeiroNome}` : ''}!
                </h1>

                <p>
                  O que você precisa para o seu pet hoje?
                </p>
              </>
            ) : (
              <>
                <h1>Dashboard {perfil}</h1>

                <p>
                  Bem-vindo ao sistema Petonline24h
                </p>
              </>
            )}
          </div>

          <button
            className="btn-refresh"
            type="button"
            aria-label="Atualizar dashboard"
            onClick={() => setRecarga((atual) => atual + 1)}
          >
            <RefreshCw size={16} />
            <span className="btn-refresh-texto">
              Atualizar
            </span>
          </button>
        </header>

        {erro && (
          <p className="dashboard-erro">
            {erro}
          </p>
        )}

        {perfil === 'Administrador' && (
          <AdminDashboard dados={dados} />
        )}

        {perfil === 'Veterinário' && (
          <VeterinarioDashboard dados={dados} />
        )}

        {perfil === 'Cliente' && (
          <ClienteDashboard dados={dados} />
        )}
      </main>
    </div>
  )
}

export default Dashboard
