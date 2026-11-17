import { useEffect, useMemo, useState } from 'react'
import { Navigate } from 'react-router-dom'
import {
  Plus,
  Search,
  Check,
  CalendarClock,
  CalendarX,
  Stethoscope,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from 'lucide-react'

import api from '../../services/api'
import tratarErro from '../../services/tratarErro'
import { useAuth } from '../../contexts/AuthContext'

import Sidebar from '../../components/Sidebar/Sidebar'
import ConsultaFormModal from '../../components/ConsultaFormModal/ConsultaFormModal'
import AtendimentoFormModal from '../../components/AtendimentoFormModal/AtendimentoFormModal'
import ConfirmDialog from '../../components/ConfirmDialog/ConfirmDialog'

// Layout base (sidebar, cabeçalho, tabela, paginação) é o mesmo de Animais;
// os selos de status e avisos vêm de Minhas Consultas.
import '../Animais/Animais.css'
import '../MinhasConsultas/MinhasConsultas.css'
import './Agendamentos.css'

const LIMITE_POR_PAGINA = 10

// Mesmos valores aceitos pela API (STATUS_VALIDOS no service de agendamentos).
const STATUS_OPCOES = ['Pendente', 'Confirmado', 'Finalizado', 'Cancelado']

// Só dá pra mexer no que ainda não foi finalizado/cancelado.
const STATUS_ABERTOS = ['Pendente', 'Confirmado']

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

function Agendamentos() {
  const { usuario } = useAuth()

  const perfil = usuario?.perfil
  const ehVeterinario = perfil === 'Veterinário'
  const temAcesso = ehVeterinario || perfil === 'Administrador'

  const [sidebarAberto, setSidebarAberto] = useState(true)

  // Animais e tutores: a API de agendamentos só devolve o animal_id,
  // então buscamos os dois para mostrar nomes na tabela.
  const [animais, setAnimais] = useState([])
  const [clientes, setClientes] = useState([])
  const [carregandoAnimais, setCarregandoAnimais] = useState(true)
  const [erroAnimais, setErroAnimais] = useState('')

  const [busca, setBusca] = useState('')
  const [buscaAplicada, setBuscaAplicada] = useState('')
  const [status, setStatus] = useState('')
  const [ordem, setOrdem] = useState('desc')
  const [pagina, setPagina] = useState(1)

  // Incrementar força a lista a ser buscada de novo.
  const [recarga, setRecarga] = useState(0)

  // Resultado da última busca, junto com a "chave" dos filtros que o gerou.
  // Se a chave atual for diferente da guardada, ainda estamos carregando.
  const [resultado, setResultado] = useState({
    chave: null,
    consultas: [],
    erro: '',
  })

  const [aviso, setAviso] = useState({ tipo: '', texto: '' })
  const [ocupadoId, setOcupadoId] = useState(null)

  const [modalNovo, setModalNovo] = useState(false)
  const [consultaParaReagendar, setConsultaParaReagendar] = useState(null)
  const [consultaParaAtender, setConsultaParaAtender] = useState(null)

  const [consultaParaCancelar, setConsultaParaCancelar] = useState(null)
  const [cancelando, setCancelando] = useState(false)
  const [erroCancelamento, setErroCancelamento] = useState('')

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

  const chaveBusca = `${pagina}|${status}|${buscaAplicada}|${ordem}|${recarga}`

  useEffect(() => {
    if (!temAcesso) return

    // Se os filtros mudarem antes da resposta chegar, ignora a resposta antiga.
    let ignorar = false

    api
      .get('/agendamentos/', {
        params: {
          skip: (pagina - 1) * LIMITE_POR_PAGINA,
          limit: LIMITE_POR_PAGINA,
          status: status || undefined,
          descricao: buscaAplicada || undefined,
          sort_by: 'data_agendamento',
          order: ordem,
        },
      })
      .then((res) => {
        if (ignorar) return
        setResultado({
          chave: chaveBusca,
          consultas: res.data || [],
          erro: '',
        })
      })
      .catch((err) => {
        if (ignorar) return
        setResultado({
          chave: chaveBusca,
          consultas: [],
          erro: tratarErro(err).mensagem,
        })
      })

    return () => {
      ignorar = true
    }
  }, [chaveBusca, pagina, status, buscaAplicada, ordem, temAcesso])

  if (!usuario) return <Navigate to="/login" replace />
  if (!temAcesso) return <Navigate to="/dashboard" replace />

  const carregando = resultado.chave !== chaveBusca
  const consultas = resultado.consultas
  const erro = carregando ? '' : resultado.erro

  function recarregar() {
    setRecarga((n) => n + 1)
  }

  function mostrarAviso(tipo, texto) {
    setAviso({ tipo, texto })
  }

  function nomeAnimal(consulta) {
    return animaisPorId[consulta.animal_id]?.nome || `Animal #${consulta.animal_id}`
  }

  function nomeTutor(consulta) {
    const animal = animaisPorId[consulta.animal_id]

    return (animal && nomesClientes[animal.cliente_id]) || '—'
  }

  function rotuloVeterinario(consulta) {
    if (!consulta.veterinario_id) return 'Sem veterinário'
    if (consulta.veterinario_id === usuario.id) return 'Você'

    return 'Outro veterinário'
  }

  function handleBuscar(e) {
    e.preventDefault()
    setPagina(1)
    setBuscaAplicada(busca.trim())
  }

  function handleStatus(e) {
    setStatus(e.target.value)
    setPagina(1)
  }

  function alternarOrdem() {
    setOrdem((atual) => (atual === 'asc' ? 'desc' : 'asc'))
    setPagina(1)
  }

  function salvouAgendamento() {
    const reagendando = Boolean(consultaParaReagendar)

    setModalNovo(false)
    setConsultaParaReagendar(null)
    mostrarAviso(
      'sucesso',
      reagendando ? 'Consulta reagendada.' : 'Consulta agendada com sucesso!'
    )
    recarregar()
  }

  // Confirma a consulta e, se quem confirma é veterinário, já assume
  // o atendimento (a API só aceita que ele indique a si mesmo).
  async function confirmarConsulta(consulta) {
    setOcupadoId(consulta.id)
    setAviso({ tipo: '', texto: '' })

    try {
      await api.put(`/agendamentos/${consulta.id}`, {
        status: 'Confirmado',
        ...(ehVeterinario ? { veterinario_id: usuario.id } : {}),
      })

      mostrarAviso('sucesso', 'Consulta confirmada.')
      recarregar()
    } catch (err) {
      mostrarAviso('erro', tratarErro(err).mensagem)
    } finally {
      setOcupadoId(null)
    }
  }

  // O atendimento já foi gravado; falta marcar o agendamento como finalizado.
  async function salvouAtendimento() {
    const consulta = consultaParaAtender

    setConsultaParaAtender(null)
    setOcupadoId(consulta.id)

    try {
      await api.put(`/agendamentos/${consulta.id}`, {
        status: 'Finalizado',
        ...(ehVeterinario ? { veterinario_id: usuario.id } : {}),
      })

      mostrarAviso('sucesso', 'Atendimento registrado e consulta finalizada.')
    } catch (err) {
      mostrarAviso(
        'erro',
        `Atendimento registrado, mas não foi possível finalizar a consulta: ${
          tratarErro(err).mensagem
        }`
      )
    } finally {
      setOcupadoId(null)
      recarregar()
    }
  }

  function pedirCancelamento(consulta) {
    setConsultaParaCancelar(consulta)
    setErroCancelamento('')
  }

  async function confirmarCancelamento() {
    setCancelando(true)
    setErroCancelamento('')

    try {
      await api.post(`/agendamentos/${consultaParaCancelar.id}/cancelar`)

      setConsultaParaCancelar(null)
      mostrarAviso('sucesso', 'Consulta cancelada.')
      recarregar()
    } catch (err) {
      setErroCancelamento(tratarErro(err).mensagem)
    } finally {
      setCancelando(false)
    }
  }

  const temFiltro = Boolean(status || buscaAplicada)
  const semAnimais = !carregandoAnimais && !erroAnimais && animais.length === 0

  return (
    <div className="animais-page consultas-page">
      <Sidebar perfil={perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="animais-header">
          <div>
            <h1>Agendamentos</h1>
            <p>Confirme, reagende e conduza as consultas da clínica</p>
          </div>

          <button
            className="btn-novo"
            onClick={() => {
              setAviso({ tipo: '', texto: '' })
              setModalNovo(true)
            }}
            disabled={carregandoAnimais || animais.length === 0}
            title={semAnimais ? 'Não há animais cadastrados' : erroAnimais || ''}
          >
            <Plus size={18} /> Agendar consulta
          </button>
        </header>

        {aviso.texto && (
          <p
            className={`consultas-aviso ${
              aviso.tipo === 'erro' ? 'agenda-aviso-erro' : 'consultas-aviso-sucesso'
            }`}
            role={aviso.tipo === 'erro' ? 'alert' : 'status'}
          >
            {aviso.texto}
          </p>
        )}

        <div className="animais-toolbar">
          <form className="busca-form" onSubmit={handleBuscar}>
            <Search size={16} />
            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar pelo motivo..."
            />
          </form>

          <select
            className="filtro-status"
            value={status}
            onChange={handleStatus}
            aria-label="Filtrar por status"
          >
            <option value="">Todos os status</option>
            {STATUS_OPCOES.map((opcao) => (
              <option key={opcao} value={opcao}>
                {opcao}
              </option>
            ))}
          </select>

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
                <th>Motivo</th>
                <th>Veterinário</th>
                <th>Status</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>

            <tbody>
              {carregando && (
                <tr>
                  <td colSpan={7} className="tabela-status">
                    Carregando...
                  </td>
                </tr>
              )}

              {!carregando && consultas.length === 0 && (
                <tr>
                  <td colSpan={7} className="tabela-status">
                    {temFiltro
                      ? 'Nenhum agendamento encontrado com esses filtros.'
                      : 'Ainda não há agendamentos.'}
                  </td>
                </tr>
              )}

              {!carregando &&
                consultas.map((consulta) => {
                  const aberta = STATUS_ABERTOS.includes(consulta.status)
                  const ocupada = ocupadoId === consulta.id

                  return (
                    <tr key={consulta.id}>
                      <td className="col-data">
                        {formatarDataHora(consulta.data_agendamento)}
                      </td>
                      <td className="col-nome">{nomeAnimal(consulta)}</td>
                      <td>{nomeTutor(consulta)}</td>
                      <td className="col-descricao">{consulta.descricao}</td>
                      <td>{rotuloVeterinario(consulta)}</td>
                      <td>
                        <span
                          className={`status-badge status-${consulta.status.toLowerCase()}`}
                        >
                          {consulta.status}
                        </span>
                      </td>
                      <td className="col-acoes">
                        {consulta.status === 'Pendente' && (
                          <button
                            className="btn-icone btn-icone-sucesso"
                            title="Confirmar consulta"
                            aria-label="Confirmar consulta"
                            disabled={ocupada}
                            onClick={() => confirmarConsulta(consulta)}
                          >
                            <Check size={16} />
                          </button>
                        )}

                        {aberta && (
                          <button
                            className="btn-icone btn-icone-sucesso"
                            title="Registrar atendimento"
                            aria-label="Registrar atendimento"
                            disabled={ocupada}
                            onClick={() => setConsultaParaAtender(consulta)}
                          >
                            <Stethoscope size={16} />
                          </button>
                        )}

                        {aberta && (
                          <button
                            className="btn-icone"
                            title="Reagendar consulta"
                            aria-label="Reagendar consulta"
                            disabled={ocupada}
                            onClick={() => {
                              setAviso({ tipo: '', texto: '' })
                              setConsultaParaReagendar(consulta)
                            }}
                          >
                            <CalendarClock size={16} />
                          </button>
                        )}

                        {aberta && (
                          <button
                            className="btn-icone btn-icone-perigo"
                            title="Cancelar consulta"
                            aria-label="Cancelar consulta"
                            disabled={ocupada}
                            onClick={() => pedirCancelamento(consulta)}
                          >
                            <CalendarX size={16} />
                          </button>
                        )}
                      </td>
                    </tr>
                  )
                })}
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
            disabled={carregando || consultas.length < LIMITE_POR_PAGINA}
          >
            Próxima <ChevronRight size={16} />
          </button>
        </div>
      </main>

      {(modalNovo || consultaParaReagendar) && (
        <ConsultaFormModal
          animais={animais}
          consulta={consultaParaReagendar}
          onClose={() => {
            setModalNovo(false)
            setConsultaParaReagendar(null)
          }}
          onSalvo={salvouAgendamento}
        />
      )}

      {consultaParaAtender && (
        <AtendimentoFormModal
          animais={animais}
          animalIdInicial={consultaParaAtender.animal_id}
          usuarioId={usuario.id}
          onClose={() => setConsultaParaAtender(null)}
          onSalvo={salvouAtendimento}
        />
      )}

      {consultaParaCancelar && (
        <ConfirmDialog
          titulo="Cancelar consulta"
          mensagem={`Tem certeza que deseja cancelar a consulta de "${nomeAnimal(
            consultaParaCancelar
          )}" marcada para ${formatarDataHora(consultaParaCancelar.data_agendamento)}?`}
          confirmando={cancelando}
          erro={erroCancelamento}
          textoConfirmar="Cancelar consulta"
          textoConfirmando="Cancelando..."
          textoCancelar="Voltar"
          onConfirmar={confirmarCancelamento}
          onCancelar={() => setConsultaParaCancelar(null)}
        />
      )}
    </div>
  )
}

export default Agendamentos
