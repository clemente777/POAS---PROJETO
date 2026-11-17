import { useEffect, useMemo, useState } from 'react'
import { Navigate } from 'react-router-dom'
import {
  Plus,
  Search,
  Pencil,
  History,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from 'lucide-react'

import api from '../../services/api'
import tratarErro from '../../services/tratarErro'
import { useAuth } from '../../contexts/AuthContext'

import Sidebar from '../../components/Sidebar/Sidebar'
import AtendimentoFormModal from '../../components/AtendimentoFormModal/AtendimentoFormModal'
import AnimalHistoricoModal from '../../components/AnimalHistoricoModal/AnimalHistoricoModal'

// Layout base (sidebar, cabeçalho, tabela, paginação) é o mesmo de Animais;
// os selos de status e avisos vêm de Minhas Consultas.
import '../Animais/Animais.css'
import '../MinhasConsultas/MinhasConsultas.css'
import './Atendimentos.css'

const LIMITE_POR_PAGINA = 10

// A API devolve a data sem fuso ("2026-10-20T14:30:00"); o navegador
// interpreta como horário local, que é o mesmo que foi digitado.
function formatarDataHora(iso) {
  const data = new Date(iso)

  if (Number.isNaN(data.getTime())) return '—'

  return data.toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function Atendimentos() {
  const { usuario } = useAuth()

  const perfil = usuario?.perfil
  const temAcesso = perfil === 'Veterinário' || perfil === 'Administrador'

  const [sidebarAberto, setSidebarAberto] = useState(true)

  // Animais e tutores: a API de atendimentos só devolve o animal_id,
  // então buscamos os dois para mostrar nomes na tabela.
  const [animais, setAnimais] = useState([])
  const [clientes, setClientes] = useState([])
  const [carregandoAnimais, setCarregandoAnimais] = useState(true)
  const [erroAnimais, setErroAnimais] = useState('')

  const [busca, setBusca] = useState('')
  const [buscaAplicada, setBuscaAplicada] = useState('')
  const [somenteMeus, setSomenteMeus] = useState(false)
  const [ordem, setOrdem] = useState('desc')
  const [pagina, setPagina] = useState(1)

  // Incrementar força a lista a ser buscada de novo.
  const [recarga, setRecarga] = useState(0)

  // Resultado da última busca, junto com a "chave" dos filtros que o gerou.
  // Se a chave atual for diferente da guardada, ainda estamos carregando.
  const [resultado, setResultado] = useState({
    chave: null,
    atendimentos: [],
    erro: '',
  })

  const [aviso, setAviso] = useState('')

  const [modalNovo, setModalNovo] = useState(false)
  const [atendimentoParaEditar, setAtendimentoParaEditar] = useState(null)
  const [historicoAnimalId, setHistoricoAnimalId] = useState(null)

  useEffect(() => {
    if (!temAcesso) return

    api
      .get('/animais/', { params: { pagina: 1, limite: 100 } })
      .then((res) => setAnimais(res.data || []))
      .catch((err) => setErroAnimais(tratarErro(err).mensagem))
      .finally(() => setCarregandoAnimais(false))

    api
      .get('/clientes/', { params: { limit: 100 } })
      .then((res) => setClientes(res.data || []))
      .catch(() => setClientes([]))
  }, [temAcesso])

  const animaisPorId = useMemo(
    () => Object.fromEntries(animais.map((animal) => [animal.id, animal])),
    [animais]
  )

  const nomesClientes = useMemo(
    () => Object.fromEntries(clientes.map((cliente) => [cliente.id, cliente.nome])),
    [clientes]
  )

  const chaveBusca = `${pagina}|${buscaAplicada}|${somenteMeus}|${ordem}|${recarga}`

  useEffect(() => {
    if (!temAcesso) return

    // Se os filtros mudarem antes da resposta chegar, ignora a resposta antiga.
    let ignorar = false

    api
      .get('/atendimentos/', {
        params: {
          skip: (pagina - 1) * LIMITE_POR_PAGINA,
          limit: LIMITE_POR_PAGINA,
          diagnostico: buscaAplicada || undefined,
          usuario_id: somenteMeus ? usuario.id : undefined,
          sort_by: 'data_atendimento',
          order: ordem,
        },
      })
      .then((res) => {
        if (ignorar) return
        setResultado({
          chave: chaveBusca,
          atendimentos: res.data || [],
          erro: '',
        })
      })
      .catch((err) => {
        if (ignorar) return
        setResultado({
          chave: chaveBusca,
          atendimentos: [],
          erro: tratarErro(err).mensagem,
        })
      })

    return () => {
      ignorar = true
    }
  }, [chaveBusca, pagina, buscaAplicada, somenteMeus, ordem, temAcesso, usuario])

  if (!usuario) return <Navigate to="/login" replace />
  if (!temAcesso) return <Navigate to="/dashboard" replace />

  const carregando = resultado.chave !== chaveBusca
  const atendimentos = resultado.atendimentos
  const erro = carregando ? '' : resultado.erro

  function recarregar() {
    setRecarga((n) => n + 1)
  }

  function nomeAnimal(atendimento) {
    return (
      animaisPorId[atendimento.animal_id]?.nome || `Animal #${atendimento.animal_id}`
    )
  }

  function nomeTutor(atendimento) {
    const animal = animaisPorId[atendimento.animal_id]

    return (animal && nomesClientes[animal.cliente_id]) || '—'
  }

  function rotuloVeterinario(atendimento) {
    return atendimento.usuario_id === usuario.id ? 'Você' : 'Outro veterinário'
  }

  function handleBuscar(e) {
    e.preventDefault()
    setPagina(1)
    setBuscaAplicada(busca.trim())
  }

  function alternarMeus(e) {
    setSomenteMeus(e.target.checked)
    setPagina(1)
  }

  function alternarOrdem() {
    setOrdem((atual) => (atual === 'asc' ? 'desc' : 'asc'))
    setPagina(1)
  }

  function salvouAtendimento() {
    const editando = Boolean(atendimentoParaEditar)

    setModalNovo(false)
    setAtendimentoParaEditar(null)
    setAviso(
      editando ? 'Atendimento atualizado.' : 'Atendimento registrado com sucesso!'
    )
    recarregar()
  }

  const temFiltro = Boolean(buscaAplicada || somenteMeus)
  const semAnimais = !carregandoAnimais && !erroAnimais && animais.length === 0

  return (
    <div className="animais-page consultas-page">
      <Sidebar perfil={perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="animais-header">
          <div>
            <h1>Atendimentos</h1>
            <p>Registre diagnósticos e acompanhe o histórico clínico dos animais</p>
          </div>

          <button
            className="btn-novo"
            onClick={() => {
              setAviso('')
              setModalNovo(true)
            }}
            disabled={carregandoAnimais || animais.length === 0}
            title={semAnimais ? 'Não há animais cadastrados' : erroAnimais || ''}
          >
            <Plus size={18} /> Registrar atendimento
          </button>
        </header>

        {aviso && <p className="consultas-aviso consultas-aviso-sucesso">{aviso}</p>}

        <div className="animais-toolbar">
          <form className="busca-form" onSubmit={handleBuscar}>
            <Search size={16} />
            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar pelo diagnóstico..."
            />
          </form>

          <label className="filtro-meus">
            <input type="checkbox" checked={somenteMeus} onChange={alternarMeus} />
            Somente os meus
          </label>

          <button className="btn-ordem" onClick={alternarOrdem} type="button">
            <ArrowUpDown size={16} />
            Data ({ordem === 'desc' ? 'mais recentes' : 'mais antigas'})
          </button>
        </div>

        {erro && <p className="animais-erro">{erro}</p>}
        {erroAnimais && <p className="animais-erro">{erroAnimais}</p>}

        <div className="animais-tabela-wrapper">
          <table className="animais-tabela">
            <thead>
              <tr>
                <th>Data e horário</th>
                <th>Animal</th>
                <th>Tutor</th>
                <th>Diagnóstico</th>
                <th>Observações</th>
                <th>Veterinário</th>
                <th>Status</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>

            <tbody>
              {carregando && (
                <tr>
                  <td colSpan={8} className="tabela-status">
                    Carregando...
                  </td>
                </tr>
              )}

              {!carregando && atendimentos.length === 0 && (
                <tr>
                  <td colSpan={8} className="tabela-status">
                    {temFiltro
                      ? 'Nenhum atendimento encontrado com esses filtros.'
                      : 'Ainda não há atendimentos registrados.'}
                  </td>
                </tr>
              )}

              {!carregando &&
                atendimentos.map((atendimento) => (
                  <tr key={atendimento.id}>
                    <td className="col-data">
                      {formatarDataHora(atendimento.data_atendimento)}
                    </td>
                    <td className="col-nome">{nomeAnimal(atendimento)}</td>
                    <td>{nomeTutor(atendimento)}</td>
                    <td className="col-descricao">{atendimento.diagnostico}</td>
                    <td className="col-descricao">{atendimento.observacoes || '—'}</td>
                    <td>{rotuloVeterinario(atendimento)}</td>
                    <td>
                      <span
                        className={`status-badge status-${atendimento.status.toLowerCase()}`}
                      >
                        {atendimento.status}
                      </span>
                    </td>
                    <td className="col-acoes">
                      <button
                        className="btn-icone"
                        title="Histórico do animal"
                        aria-label="Histórico do animal"
                        onClick={() => setHistoricoAnimalId(atendimento.animal_id)}
                      >
                        <History size={16} />
                      </button>

                      {atendimento.status !== 'Cancelado' && (
                        <button
                          className="btn-icone"
                          title="Editar diagnóstico e observações"
                          aria-label="Editar atendimento"
                          onClick={() => {
                            setAviso('')
                            setAtendimentoParaEditar(atendimento)
                          }}
                        >
                          <Pencil size={16} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>

        <div className="animais-paginacao">
          <button
            onClick={() => setPagina((p) => Math.max(1, p - 1))}
            disabled={pagina === 1 || carregando}
          >
            <ChevronLeft size={16} /> Anterior
          </button>

          <span>Página {pagina}</span>

          <button
            onClick={() => setPagina((p) => p + 1)}
            disabled={carregando || atendimentos.length < LIMITE_POR_PAGINA}
          >
            Próxima <ChevronRight size={16} />
          </button>
        </div>
      </main>

      {(modalNovo || atendimentoParaEditar) && (
        <AtendimentoFormModal
          animais={animais}
          atendimento={atendimentoParaEditar}
          usuarioId={usuario.id}
          onClose={() => {
            setModalNovo(false)
            setAtendimentoParaEditar(null)
          }}
          onSalvo={salvouAtendimento}
        />
      )}

      {historicoAnimalId !== null && (
        <AnimalHistoricoModal
          animalId={historicoAnimalId}
          onClose={() => setHistoricoAnimalId(null)}
        />
      )}
    </div>
  )
}

export default Atendimentos
