import { useEffect, useMemo, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  Plus,
  Search,
  CalendarX,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from 'lucide-react'

import api from '../../services/api'
import tratarErro from '../../services/tratarErro'
import { useAuth } from '../../contexts/AuthContext'

import Sidebar from '../../components/Sidebar/Sidebar'
import ConsultaFormModal from '../../components/ConsultaFormModal/ConsultaFormModal'
import ConfirmDialog from '../../components/ConfirmDialog/ConfirmDialog'

import '../Animais/Animais.css'
import './MinhasConsultas.css'

const LIMITE_POR_PAGINA = 10

const STATUS_OPCOES = ['Pendente', 'Confirmado', 'Finalizado', 'Cancelado']

const STATUS_CANCELAVEIS = ['Pendente', 'Confirmado']

function formatarDataHora(iso) {
  if (!iso) return '—'

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

function MinhasConsultas() {
  const { usuario } = useAuth()

  const [sidebarAberto, setSidebarAberto] = useState(true)

  const [animais, setAnimais] = useState([])
  const [carregandoAnimais, setCarregandoAnimais] = useState(true)
  const [erroAnimais, setErroAnimais] = useState('')

  const [busca, setBusca] = useState('')
  const [buscaAplicada, setBuscaAplicada] = useState('')
  const [status, setStatus] = useState('')
  const [ordem, setOrdem] = useState('desc')
  const [pagina, setPagina] = useState(1)

  const [recarga, setRecarga] = useState(0)

  const [resultado, setResultado] = useState({
    chave: null,
    consultas: [],
    erro: '',
  })

  const [modalNovo, setModalNovo] = useState(false)
  const [aviso, setAviso] = useState('')

  const [consultaParaCancelar, setConsultaParaCancelar] = useState(null)
  const [cancelando, setCancelando] = useState(false)
  const [erroCancelamento, setErroCancelamento] = useState('')

  useEffect(() => {
    let ignorar = false

    async function carregarAnimais() {
      try {
        const resposta = await api.get('/animais/', {
          params: {
            pagina: 1,
            limite: 100,
          },
        })

        if (!ignorar) {
          setAnimais(Array.isArray(resposta.data) ? resposta.data : [])
          setErroAnimais('')
        }
      } catch (erro) {
        if (!ignorar) {
          setAnimais([])
          setErroAnimais(tratarErro(erro).mensagem)
        }
      } finally {
        if (!ignorar) {
          setCarregandoAnimais(false)
        }
      }
    }

    carregarAnimais()

    return () => {
      ignorar = true
    }
  }, [])

  const nomesAnimais = useMemo(
    () => Object.fromEntries(animais.map((animal) => [animal.id, animal.nome])),
    [animais]
  )

  const chaveBusca = `${pagina}|${status}|${buscaAplicada}|${ordem}|${recarga}`

  useEffect(() => {
    let ignorar = false

    async function carregarConsultas() {
      try {
        const resposta = await api.get('/agendamentos/', {
          params: {
            skip: (pagina - 1) * LIMITE_POR_PAGINA,
            limit: LIMITE_POR_PAGINA,
            status: status || undefined,
            descricao: buscaAplicada || undefined,
            sort_by: 'data_agendamento',
            order: ordem,
          },
        })

        if (ignorar) return

        setResultado({
          chave: chaveBusca,
          consultas: Array.isArray(resposta.data) ? resposta.data : [],
          erro: '',
        })
      } catch (erro) {
        if (ignorar) return

        setResultado({
          chave: chaveBusca,
          consultas: [],
          erro: tratarErro(erro).mensagem,
        })
      }
    }

    carregarConsultas()

    return () => {
      ignorar = true
    }
  }, [chaveBusca, pagina, status, buscaAplicada, ordem])

  const carregando = resultado.chave !== chaveBusca
  const consultas = resultado.consultas
  const erro = carregando ? '' : resultado.erro

  function recarregar() {
    setRecarga((atual) => atual + 1)
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

  function salvouConsulta() {
    setModalNovo(false)
    setAviso('Consulta agendada com sucesso!')
    recarregar()
  }

  function pedirCancelamento(consulta) {
    setConsultaParaCancelar(consulta)
    setErroCancelamento('')
  }

  async function confirmarCancelamento() {
    if (!consultaParaCancelar || cancelando) return

    setCancelando(true)
    setErroCancelamento('')

    try {
      await api.post(`/agendamentos/${consultaParaCancelar.id}/cancelar`)

      setConsultaParaCancelar(null)
      setAviso('Consulta cancelada com sucesso!')
      recarregar()
    } catch (erro) {
      setErroCancelamento(tratarErro(erro).mensagem)
    } finally {
      setCancelando(false)
    }
  }

  const [searchParams, setSearchParams] = useSearchParams()

  useEffect(() => {
    if (searchParams.get('agendar') !== '1' || carregandoAnimais) return

    if (animais.length > 0) {
      setModalNovo(true)
    }

    setSearchParams({}, { replace: true })
  }, [searchParams, carregandoAnimais, animais.length, setSearchParams])

  const temFiltro = Boolean(status || buscaAplicada)
  const semAnimais = !carregandoAnimais && !erroAnimais && animais.length === 0

  return (
    <div className="animais-page consultas-page">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="animais-header">
          <div>
            <h1>Minhas Consultas</h1>
            <p>Acompanhe e agende as consultas dos seus pets</p>
          </div>

          <button
            type="button"
            className="btn-novo"
            onClick={() => {
              setAviso('')
              setModalNovo(true)
            }}
            disabled={carregandoAnimais || animais.length === 0 || Boolean(erroAnimais)}
            title={
              semAnimais ? 'Cadastre um animal para poder agendar' : erroAnimais || ''
            }
          >
            <Plus size={18} />
            Agendar consulta
          </button>
        </header>

        {aviso && (
          <p className="consultas-aviso consultas-aviso-sucesso" role="status">
            {aviso}
          </p>
        )}

        {semAnimais && (
          <p className="consultas-aviso consultas-aviso-info">
            Para agendar uma consulta, primeiro cadastre um animal em{' '}
            <Link to="/meus-animais">Meus Animais</Link>.
          </p>
        )}

        <div className="animais-toolbar">
          <form className="busca-form" onSubmit={handleBuscar}>
            <Search size={16} />
            <input
              type="search"
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar pelo motivo..."
              aria-label="Buscar consulta pelo motivo"
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

        {erro && (
          <p className="animais-erro" role="alert">
            {erro}
          </p>
        )}

        {erroAnimais && (
          <p className="animais-erro" role="alert">
            Não foi possível carregar seus animais: {erroAnimais}
          </p>
        )}

        <div className="animais-tabela-wrapper">
          <table className="animais-tabela animais-tabela--cartoes">
            <thead>
              <tr>
                <th>Data e horário</th>
                <th>Animal</th>
                <th>Motivo</th>
                <th>Status</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>

            <tbody>
              {carregando && (
                <tr>
                  <td colSpan={5} className="tabela-status">
                    Carregando consultas...
                  </td>
                </tr>
              )}

              {!carregando && consultas.length === 0 && (
                <tr>
                  <td colSpan={5} className="tabela-status">
                    {erro
                      ? 'Não foi possível carregar as consultas.'
                      : temFiltro
                        ? 'Nenhuma consulta encontrada com esses filtros.'
                        : 'Você ainda não tem consultas agendadas.'}
                  </td>
                </tr>
              )}

              {!carregando &&
                consultas.map((consulta) => {
                  const statusConsulta = consulta.status || ''

                  return (
                    <tr key={consulta.id}>
                      <td className="col-data" data-label="Data e horário">
                        {formatarDataHora(consulta.data_agendamento)}
                      </td>

                      <td className="col-nome" data-label="Animal">
                        {nomesAnimais[consulta.animal_id] ||
                          `Animal #${consulta.animal_id}`}
                      </td>

                      <td className="col-descricao" data-label="Motivo">
                        {consulta.descricao || '—'}
                      </td>

                      <td data-label="Status">
                        <span
                          className={`status-badge status-${statusConsulta
                            .toLowerCase()
                            .replace(/\s+/g, '-')}`}
                        >
                          {statusConsulta || 'Indefinido'}
                        </span>
                      </td>

                      <td className="col-acoes">
                        {STATUS_CANCELAVEIS.includes(statusConsulta) && (
                          <button
                            type="button"
                            className="btn-icone btn-icone-perigo"
                            title="Cancelar consulta"
                            aria-label={`Cancelar consulta de ${
                              nomesAnimais[consulta.animal_id] || 'seu animal'
                            }`}
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
            type="button"
            onClick={() => setPagina((atual) => Math.max(1, atual - 1))}
            disabled={pagina === 1 || carregando}
          >
            <ChevronLeft size={16} />
            Anterior
          </button>

          <span>Página {pagina}</span>

          <button
            type="button"
            onClick={() => setPagina((atual) => atual + 1)}
            disabled={carregando || consultas.length < LIMITE_POR_PAGINA}
          >
            Próxima
            <ChevronRight size={16} />
          </button>
        </div>
      </main>

      {modalNovo && (
        <ConsultaFormModal
          animais={animais}
          onClose={() => setModalNovo(false)}
          onSalvo={salvouConsulta}
        />
      )}

      {consultaParaCancelar && (
        <ConfirmDialog
          titulo="Cancelar consulta"
          mensagem={`Tem certeza que deseja cancelar a consulta de "${
            nomesAnimais[consultaParaCancelar.animal_id] || 'seu animal'
          }" marcada para ${formatarDataHora(consultaParaCancelar.data_agendamento)}?`}
          confirmando={cancelando}
          erro={erroCancelamento}
          textoConfirmar="Cancelar consulta"
          textoConfirmando="Cancelando..."
          textoCancelar="Voltar"
          onConfirmar={confirmarCancelamento}
          onCancelar={() => {
            if (!cancelando) {
              setConsultaParaCancelar(null)
            }
          }}
        />
      )}
    </div>
  )
}

export default MinhasConsultas
