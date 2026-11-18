
import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import {
  Search,
  Plus,
  Pencil,
  ChevronLeft,
  ChevronRight,
  X,
  Save,
  Users,
} from 'lucide-react'

import { useAuth } from '../../contexts/AuthContext'
import Sidebar from '../../components/Sidebar/Sidebar'
import api from '../../services/api'
import tratarErro from '../../services/tratarErro'

import './Clientes.css'

const LIMITE_POR_PAGINA = 10

const FORMULARIO_INICIAL = {
  nome: '',
  cpf: '',
  telefone: '',
  email: '',
  endereco: '',
  senha: '',
}

function Clientes() {
  const { usuario } = useAuth()
  const perfil = usuario?.perfil
  const temAcesso = perfil === 'Administrador'

  const [sidebarAberto, setSidebarAberto] = useState(true)
  const [clientes, setClientes] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')

  const [busca, setBusca] = useState('')
  const [buscaAplicada, setBuscaAplicada] = useState('')
  const [pagina, setPagina] = useState(1)
  const [recarga, setRecarga] = useState(0)

  const [modalAberto, setModalAberto] = useState(false)
  const [clienteEditando, setClienteEditando] = useState(null)
  const [formulario, setFormulario] = useState(FORMULARIO_INICIAL)
  const [salvando, setSalvando] = useState(false)
  const [erroFormulario, setErroFormulario] = useState('')
  const [aviso, setAviso] = useState('')

  useEffect(() => {
    if (!temAcesso) return

    let ignorar = false

    setCarregando(true)
    setErro('')

    api
      .get('/clientes/', {
        params: {
          skip: (pagina - 1) * LIMITE_POR_PAGINA,
          limit: LIMITE_POR_PAGINA,
          nome: buscaAplicada || undefined,
          sort_by: 'nome',
          order: 'asc',
        },
      })
      .then((res) => {
        if (!ignorar) setClientes(res.data || [])
      })
      .catch((err) => {
        if (!ignorar) {
          setClientes([])
          setErro(tratarErro(err).mensagem)
        }
      })
      .finally(() => {
        if (!ignorar) setCarregando(false)
      })

    return () => {
      ignorar = true
    }
  }, [temAcesso, pagina, buscaAplicada, recarga])

  if (!usuario) return <Navigate to="/login" replace />
  if (!temAcesso) return <Navigate to="/dashboard" replace />

  function atualizarCampo(e) {
    const { name, value } = e.target
    setFormulario((atual) => ({ ...atual, [name]: value }))
  }

  function abrirCadastro() {
    setClienteEditando(null)
    setFormulario(FORMULARIO_INICIAL)
    setErroFormulario('')
    setAviso('')
    setModalAberto(true)
  }

  function abrirEdicao(cliente) {
    setClienteEditando(cliente)
    setFormulario({
      telefone: cliente.telefone || '',
      endereco: cliente.endereco || '',
    })
    setErroFormulario('')
    setAviso('')
    setModalAberto(true)
  }

  function fecharModal() {
    if (salvando) return
    setModalAberto(false)
    setClienteEditando(null)
    setFormulario(FORMULARIO_INICIAL)
    setErroFormulario('')
  }

  function handleBuscar(e) {
    e.preventDefault()
    setPagina(1)
    setBuscaAplicada(busca.trim())
  }

  async function salvarCliente(e) {
    e.preventDefault()
    setSalvando(true)
    setErroFormulario('')

    try {
      if (clienteEditando) {
        await api.put(`/clientes/${clienteEditando.id}`, {
          telefone: formulario.telefone,
          endereco: formulario.endereco,
        })
        setAviso('Dados do cliente atualizados com sucesso.')
      } else {
        await api.post('/clientes/', formulario)
        setAviso('Cliente cadastrado com sucesso.')
      }

      setModalAberto(false)
      setClienteEditando(null)
      setFormulario(FORMULARIO_INICIAL)
      setRecarga((n) => n + 1)
    } catch (err) {
      setErroFormulario(tratarErro(err).mensagem)
    } finally {
      setSalvando(false)
    }
  }

  return (
    <div className="animais-page clientes-page">
      <Sidebar perfil={perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="animais-header">
          <div>
            <h1>Clientes</h1>
            <p>Gerencie os cadastros dos clientes do Petonline24h</p>
          </div>

          <button className="btn-novo" onClick={abrirCadastro}>
            <Plus size={18} />
            Novo cliente
          </button>
        </header>

        {aviso && (
          <p className="clientes-aviso clientes-aviso-sucesso">{aviso}</p>
        )}

        <div className="animais-toolbar">
          <form className="busca-form" onSubmit={handleBuscar}>
            <Search size={16} />
            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar por nome, CPF ou e-mail..."
            />
          </form>
        </div>

        {erro && <p className="animais-erro">{erro}</p>}

        <div className="clientes-resumo">
          <Users size={20} />
          <span>
            {carregando
              ? 'Carregando clientes...'
              : `${clientes.length} cliente(s) nesta página`}
          </span>
        </div>

        <div className="animais-tabela-wrapper">
          <table className="animais-tabela clientes-tabela">
            <thead>
              <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>Telefone</th>
                <th>E-mail</th>
                <th>Endereço</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>

            <tbody>
              {carregando && (
                <tr>
                  <td colSpan={6} className="tabela-status">
                    Carregando clientes...
                  </td>
                </tr>
              )}

              {!carregando && clientes.length === 0 && (
                <tr>
                  <td colSpan={6} className="tabela-status">
                    {buscaAplicada
                      ? 'Nenhum cliente encontrado.'
                      : 'Ainda não há clientes cadastrados.'}
                  </td>
                </tr>
              )}

              {!carregando &&
                clientes.map((cliente) => (
                  <tr key={cliente.id}>
                    <td className="col-nome">{cliente.nome}</td>
                    <td>{cliente.cpf}</td>
                    <td>{cliente.telefone}</td>
                    <td className="cliente-email">{cliente.email}</td>
                    <td className="cliente-endereco">{cliente.endereco}</td>
                    <td className="col-acoes">
                      <button
                        type="button"
                        className="btn-icone"
                        title="Editar telefone e endereço"
                        aria-label={`Editar ${cliente.nome}`}
                        onClick={() => abrirEdicao(cliente)}
                      >
                        <Pencil size={16} />
                      </button>
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>

        <div className="animais-paginacao">
          <button
            type="button"
            onClick={() => setPagina((p) => Math.max(1, p - 1))}
            disabled={pagina === 1 || carregando}
          >
            <ChevronLeft size={16} />
            Anterior
          </button>

          <span>Página {pagina}</span>

          <button
            type="button"
            onClick={() => setPagina((p) => p + 1)}
            disabled={carregando || clientes.length < LIMITE_POR_PAGINA}
          >
            Próxima
            <ChevronRight size={16} />
          </button>
        </div>
      </main>

      {modalAberto && (
        <div className="clientes-modal-overlay" onMouseDown={fecharModal}>
          <section
            className="clientes-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="clientes-modal-titulo"
            onMouseDown={(e) => e.stopPropagation()}
          >
            <header className="clientes-modal-header">
              <div>
                <h2 id="clientes-modal-titulo">
                  {clienteEditando ? 'Editar cliente' : 'Novo cliente'}
                </h2>
                <p>
                  {clienteEditando
                    ? 'Altere somente telefone e endereço.'
                    : 'Preencha os dados para criar o cadastro e o acesso.'}
                </p>
              </div>

              <button
                type="button"
                className="clientes-modal-fechar"
                onClick={fecharModal}
                disabled={salvando}
                aria-label="Fechar"
              >
                <X size={20} />
              </button>
            </header>

            <form onSubmit={salvarCliente} className="clientes-form">
              {clienteEditando ? (
                <>
                  <label>
                    Telefone
                    <input
                      name="telefone"
                      value={formulario.telefone}
                      onChange={atualizarCampo}
                      required
                      minLength={10}
                      maxLength={20}
                    />
                  </label>

                  <label>
                    Endereço
                    <input
                      name="endereco"
                      value={formulario.endereco}
                      onChange={atualizarCampo}
                      required
                      maxLength={255}
                    />
                  </label>
                </>
              ) : (
                <>
                  <label>
                    Nome completo
                    <input
                      name="nome"
                      value={formulario.nome}
                      onChange={atualizarCampo}
                      required
                      minLength={3}
                      maxLength={100}
                    />
                  </label>

                  <label>
                    CPF
                    <input
                      name="cpf"
                      value={formulario.cpf}
                      onChange={atualizarCampo}
                      required
                      placeholder="000.000.000-00"
                      maxLength={14}
                    />
                  </label>

                  <label>
                    Telefone
                    <input
                      name="telefone"
                      value={formulario.telefone}
                      onChange={atualizarCampo}
                      required
                      placeholder="(00) 00000-0000"
                      maxLength={20}
                    />
                  </label>

                  <label>
                    E-mail
                    <input
                      type="email"
                      name="email"
                      value={formulario.email}
                      onChange={atualizarCampo}
                      required
                      maxLength={255}
                    />
                  </label>

                  <label>
                    Endereço
                    <input
                      name="endereco"
                      value={formulario.endereco}
                      onChange={atualizarCampo}
                      required
                      maxLength={255}
                    />
                  </label>

                  <label>
                    Senha inicial
                    <input
                      type="password"
                      name="senha"
                      value={formulario.senha}
                      onChange={atualizarCampo}
                      required
                      minLength={6}
                      autoComplete="new-password"
                    />
                  </label>
                </>
              )}

              {erroFormulario && (
                <p className="clientes-form-erro">{erroFormulario}</p>
              )}

              <footer className="clientes-form-acoes">
                <button
                  type="button"
                  className="clientes-btn-cancelar"
                  onClick={fecharModal}
                  disabled={salvando}
                >
                  Cancelar
                </button>

                <button
                  type="submit"
                  className="clientes-btn-salvar"
                  disabled={salvando}
                >
                  <Save size={17} />
                  {salvando ? 'Salvando...' : 'Salvar'}
                </button>
              </footer>
            </form>
          </section>
        </div>
      )}
    </div>
  )
}

export default Clientes
