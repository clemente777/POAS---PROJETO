import { useEffect, useMemo, useState } from 'react'
import {
  Plus,
  Search,
  Pencil,
  Trash2,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from 'lucide-react'

import api from '../../services/api'
import tratarErro from '../../services/tratarErro'
import { useAuth } from '../../contexts/AuthContext'

import Sidebar from '../../components/Sidebar/Sidebar'
import VacinaFormModal from '../../components/VacinaFormModal/VacinaFormModal'
import AplicacaoVacinaFormModal from '../../components/AplicacaoVacinaFormModal/AplicacaoVacinaFormModal'
import ConfirmDialog from '../../components/ConfirmDialog/ConfirmDialog'
import DoseBadge from '../../components/DoseBadge/DoseBadge'
import { DIAS_AVISO, idsDosesVigentes, situacaoDaDose } from '../../utils/vacinas'

// Layout base (sidebar, cabeçalho, tabela, paginação) é o mesmo de Animais.
import '../Animais/Animais.css'
import './Vacinas.css'

const LIMITE_POR_PAGINA = 10

const SITUACOES = [
  { valor: 'atrasada', rotulo: 'Atrasadas' },
  { valor: 'vence-em-breve', rotulo: `Vencem em ${DIAS_AVISO} dias` },
  { valor: 'em-dia', rotulo: 'Em dia' },
  { valor: 'sem-reforco', rotulo: 'Sem reforço' },
  { valor: 'reaplicada', rotulo: 'Já reaplicadas' },
]

function formatarDataHora(iso) {
  const data = new Date(iso)

  if (!iso || Number.isNaN(data.getTime())) return '—'

  return data.toLocaleString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

// Busca sem diferenciar maiúsculas/minúsculas nem acentos.
function normalizar(texto) {
  return String(texto ?? '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
}

function Vacinas() {
  const { usuario } = useAuth()

  const perfil = usuario?.perfil
  const ehAdmin = perfil === 'Administrador'
  const ehVeterinario = perfil === 'Veterinário'
  const temAcesso = ehAdmin || ehVeterinario

  const [sidebarAberto, setSidebarAberto] = useState(true)
  const [aba, setAba] = useState('aplicacoes')

  // Incrementar força tudo a ser buscado de novo (após cadastrar/editar/excluir).
  const [recarga, setRecarga] = useState(0)
  const chaveBusca = String(recarga)

  // Resultado da última busca, junto com a "chave" que o gerou.
  // Se a chave atual for diferente da guardada, ainda estamos carregando.
  const [dados, setDados] = useState({
    chave: null,
    vacinas: [],
    aplicacoes: [],
    animais: [],
    erro: '',
  })

  const [buscaAplicacoes, setBuscaAplicacoes] = useState('')
  const [situacao, setSituacao] = useState('')
  const [ordem, setOrdem] = useState('desc')
  const [pagina, setPagina] = useState(1)

  const [buscaCatalogo, setBuscaCatalogo] = useState('')

  const [modalVacina, setModalVacina] = useState(null) // { vacina: obj | null }
  const [modalAplicacao, setModalAplicacao] = useState(null) // { aplicacao: obj | null }
  const [aviso, setAviso] = useState('')

  const [alvoExclusao, setAlvoExclusao] = useState(null) // { tipo, item }
  const [excluindo, setExcluindo] = useState(false)
  const [erroExclusao, setErroExclusao] = useState('')

  useEffect(() => {
    if (!temAcesso) return

    // Se a página recarregar antes da resposta chegar, ignora a resposta antiga.
    let ignorar = false

    Promise.all([
      api.get('/vacinas/'),
      api.get('/aplicacoes-vacina/'),
      api.get('/animais/', { params: { pagina: 1, limite: 500 } }),
    ])
      .then(([resVacinas, resAplicacoes, resAnimais]) => {
        if (ignorar) return

        setDados({
          chave: chaveBusca,
          vacinas: resVacinas.data || [],
          aplicacoes: resAplicacoes.data || [],
          animais: resAnimais.data || [],
          erro: '',
        })
      })
      .catch((err) => {
        if (ignorar) return

        setDados({
          chave: chaveBusca,
          vacinas: [],
          aplicacoes: [],
          animais: [],
          erro: tratarErro(err).mensagem,
        })
      })

    return () => {
      ignorar = true
    }
  }, [chaveBusca, temAcesso])

  const carregando = temAcesso && dados.chave !== chaveBusca
  const { vacinas, aplicacoes, animais } = dados
  const erro = carregando ? '' : dados.erro

  function recarregar() {
    setRecarga((n) => n + 1)
  }

  // A API de aplicações só devolve ids; os nomes vêm das outras listas.
  const nomesAnimais = useMemo(
    () => Object.fromEntries(animais.map((animal) => [animal.id, animal.nome])),
    [animais]
  )

  const nomesVacinas = useMemo(
    () => Object.fromEntries(vacinas.map((vacina) => [vacina.id, vacina.nome])),
    [vacinas]
  )

  // Aplicações enriquecidas com a situação da dose, já ordenadas e filtradas.
  const aplicacoesFiltradas = useMemo(() => {
    const vigentes = idsDosesVigentes(aplicacoes)

    const termo = normalizar(buscaAplicacoes.trim())

    return aplicacoes
      .map((aplicacao) => {
        return {
          ...aplicacao,
          animalNome:
            nomesAnimais[aplicacao.animal_id] || `Animal #${aplicacao.animal_id}`,
          vacinaNome:
            nomesVacinas[aplicacao.vacina_id] || `Vacina #${aplicacao.vacina_id}`,
          situacao: situacaoDaDose(aplicacao, vigentes.has(aplicacao.id)),
        }
      })
      .filter((aplicacao) => {
        if (situacao && aplicacao.situacao.valor !== situacao) return false

        if (!termo) return true

        return [aplicacao.animalNome, aplicacao.vacinaNome, aplicacao.lote].some(
          (campo) => normalizar(campo).includes(termo)
        )
      })
      .sort((a, b) => {
        const diferenca =
          new Date(a.data_aplicacao) - new Date(b.data_aplicacao) || a.id - b.id

        return ordem === 'asc' ? diferenca : -diferenca
      })
  }, [aplicacoes, nomesAnimais, nomesVacinas, buscaAplicacoes, situacao, ordem])

  const totalPaginas = Math.max(
    1,
    Math.ceil(aplicacoesFiltradas.length / LIMITE_POR_PAGINA)
  )
  const paginaAtual = Math.min(pagina, totalPaginas)

  const aplicacoesDaPagina = aplicacoesFiltradas.slice(
    (paginaAtual - 1) * LIMITE_POR_PAGINA,
    paginaAtual * LIMITE_POR_PAGINA
  )

  const vacinasFiltradas = useMemo(() => {
    const termo = normalizar(buscaCatalogo.trim())

    if (!termo) return vacinas

    return vacinas.filter((vacina) =>
      [vacina.nome, vacina.fabricante].some((campo) =>
        normalizar(campo).includes(termo)
      )
    )
  }, [vacinas, buscaCatalogo])

  function trocarAba(novaAba) {
    setAba(novaAba)
    setAviso('')
  }

  function alternarOrdem() {
    setOrdem((atual) => (atual === 'asc' ? 'desc' : 'asc'))
    setPagina(1)
  }

  function salvouVacina(editou) {
    setModalVacina(null)
    setAviso(editou ? 'Vacina atualizada.' : 'Vacina cadastrada com sucesso!')
    recarregar()
  }

  function salvouAplicacao(editou) {
    setModalAplicacao(null)
    setAviso(editou ? 'Aplicação atualizada.' : 'Vacina registrada com sucesso!')
    recarregar()
  }

  function pedirExclusao(tipo, item) {
    setAlvoExclusao({ tipo, item })
    setErroExclusao('')
  }

  async function confirmarExclusao() {
    setExcluindo(true)
    setErroExclusao('')

    const { tipo, item } = alvoExclusao

    try {
      if (tipo === 'vacina') {
        await api.delete(`/vacinas/${item.id}`)
      } else {
        await api.delete(`/aplicacoes-vacina/${item.id}`)
      }

      setAlvoExclusao(null)
      setAviso(tipo === 'vacina' ? 'Vacina excluída.' : 'Aplicação excluída.')
      recarregar()
    } catch (err) {
      // Ex.: a API recusa excluir vacina que já tem aplicações registradas.
      setErroExclusao(tratarErro(err).mensagem)
    } finally {
      setExcluindo(false)
    }
  }

  const semVacinas = !carregando && !erro && vacinas.length === 0
  const semAnimais = !carregando && !erro && animais.length === 0

  const temFiltroAplicacoes = Boolean(buscaAplicacoes.trim() || situacao)

  const subtitulo = ehVeterinario
    ? 'Registre as vacinas aplicadas e acompanhe os reforços'
    : 'Gerencie o catálogo e acompanhe as aplicações'

  if (!temAcesso) {
    return (
      <div className="animais-page vacinas-page">
        <Sidebar perfil={perfil} setSidebarAberto={setSidebarAberto} />

        <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
          <header className="animais-header">
            <div>
              <h1>Vacinas</h1>
              <p>Você não tem permissão para acessar esta página.</p>
            </div>
          </header>
        </main>
      </div>
    )
  }

  return (
    <div className="animais-page vacinas-page">
      <Sidebar perfil={perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="animais-header">
          <div>
            <h1>Vacinas</h1>
            <p>{subtitulo}</p>
          </div>

          {aba === 'aplicacoes' && ehVeterinario && (
            <button
              className="btn-novo"
              onClick={() => {
                setAviso('')
                setModalAplicacao({ aplicacao: null })
              }}
              disabled={carregando || semVacinas || semAnimais}
              title={
                semVacinas
                  ? 'Nenhuma vacina cadastrada no catálogo'
                  : semAnimais
                    ? 'Nenhum animal cadastrado'
                    : ''
              }
            >
              <Plus size={18} /> Aplicar vacina
            </button>
          )}

          {aba === 'catalogo' && ehAdmin && (
            <button
              className="btn-novo"
              onClick={() => {
                setAviso('')
                setModalVacina({ vacina: null })
              }}
            >
              <Plus size={18} /> Nova vacina
            </button>
          )}
        </header>

        <div className="vacinas-abas" role="tablist">
          <button
            role="tab"
            aria-selected={aba === 'aplicacoes'}
            className={aba === 'aplicacoes' ? 'is-active' : ''}
            onClick={() => trocarAba('aplicacoes')}
          >
            Aplicações
            {!carregando && !erro && <span>{aplicacoes.length}</span>}
          </button>

          <button
            role="tab"
            aria-selected={aba === 'catalogo'}
            className={aba === 'catalogo' ? 'is-active' : ''}
            onClick={() => trocarAba('catalogo')}
          >
            Catálogo de vacinas
            {!carregando && !erro && <span>{vacinas.length}</span>}
          </button>
        </div>

        {aviso && <p className="vacinas-aviso vacinas-aviso-sucesso">{aviso}</p>}

        {ehVeterinario && aba === 'aplicacoes' && semVacinas && (
          <p className="vacinas-aviso vacinas-aviso-info">
            Ainda não há vacinas no catálogo. Peça a um administrador para cadastrá-las
            antes de registrar aplicações.
          </p>
        )}

        {erro && <p className="animais-erro">{erro}</p>}

        {aba === 'aplicacoes' && (
          <>
            <div className="animais-toolbar">
              <form className="busca-form" onSubmit={(e) => e.preventDefault()}>
                <Search size={16} />
                <input
                  value={buscaAplicacoes}
                  onChange={(e) => {
                    setBuscaAplicacoes(e.target.value)
                    setPagina(1)
                  }}
                  placeholder="Buscar por animal, vacina ou lote..."
                />
              </form>

              <select
                className="filtro-situacao"
                value={situacao}
                onChange={(e) => {
                  setSituacao(e.target.value)
                  setPagina(1)
                }}
                aria-label="Filtrar por situação da próxima dose"
              >
                <option value="">Todas as situações</option>
                {SITUACOES.map((opcao) => (
                  <option key={opcao.valor} value={opcao.valor}>
                    {opcao.rotulo}
                  </option>
                ))}
              </select>

              <button className="btn-ordem" onClick={alternarOrdem} type="button">
                <ArrowUpDown size={16} />
                Data ({ordem === 'desc' ? 'mais recentes' : 'mais antigas'})
              </button>
            </div>

            <div className="animais-tabela-wrapper">
              <table className="animais-tabela">
                <thead>
                  <tr>
                    <th>Aplicada em</th>
                    <th>Animal</th>
                    <th>Vacina</th>
                    <th>Próxima dose</th>
                    <th>Lote</th>
                    <th>Aplicada por</th>
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

                  {!carregando && aplicacoesFiltradas.length === 0 && (
                    <tr>
                      <td colSpan={7} className="tabela-status">
                        {temFiltroAplicacoes
                          ? 'Nenhuma aplicação encontrada com esses filtros.'
                          : 'Nenhuma vacina aplicada ainda.'}
                      </td>
                    </tr>
                  )}

                  {!carregando &&
                    aplicacoesDaPagina.map((aplicacao) => (
                      <tr key={aplicacao.id}>
                        <td className="col-data">
                          {formatarDataHora(aplicacao.data_aplicacao)}
                        </td>

                        <td className="col-nome">{aplicacao.animalNome}</td>

                        <td>
                          <span className="vacina-nome">{aplicacao.vacinaNome}</span>
                          {aplicacao.observacoes && (
                            <span className="vacina-obs" title={aplicacao.observacoes}>
                              {aplicacao.observacoes}
                            </span>
                          )}
                        </td>

                        <td>
                          <DoseBadge
                            situacao={aplicacao.situacao}
                            proximaDose={aplicacao.proxima_dose}
                          />
                        </td>

                        <td>{aplicacao.lote || '—'}</td>

                        <td>
                          {aplicacao.veterinario_id === usuario?.id
                            ? 'Você'
                            : `Veterinário #${aplicacao.veterinario_id}`}
                        </td>

                        <td className="col-acoes">
                          <button
                            className="btn-icone"
                            title="Editar aplicação"
                            aria-label="Editar aplicação"
                            onClick={() => {
                              setAviso('')
                              setModalAplicacao({ aplicacao })
                            }}
                          >
                            <Pencil size={16} />
                          </button>

                          {ehAdmin && (
                            <button
                              className="btn-icone btn-icone-perigo"
                              title="Excluir aplicação"
                              aria-label="Excluir aplicação"
                              onClick={() => pedirExclusao('aplicacao', aplicacao)}
                            >
                              <Trash2 size={16} />
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
                onClick={() => setPagina(Math.max(1, paginaAtual - 1))}
                disabled={paginaAtual === 1 || carregando}
              >
                <ChevronLeft size={16} /> Anterior
              </button>

              <span>
                Página {paginaAtual} de {totalPaginas}
              </span>

              <button
                onClick={() => setPagina(paginaAtual + 1)}
                disabled={carregando || paginaAtual >= totalPaginas}
              >
                Próxima <ChevronRight size={16} />
              </button>
            </div>
          </>
        )}

        {aba === 'catalogo' && (
          <>
            <div className="animais-toolbar">
              <form className="busca-form" onSubmit={(e) => e.preventDefault()}>
                <Search size={16} />
                <input
                  value={buscaCatalogo}
                  onChange={(e) => setBuscaCatalogo(e.target.value)}
                  placeholder="Buscar por nome ou fabricante..."
                />
              </form>
            </div>

            <div className="animais-tabela-wrapper">
              <table className="animais-tabela">
                <thead>
                  <tr>
                    <th>Vacina</th>
                    <th>Fabricante</th>
                    <th>Doses</th>
                    <th>Intervalo</th>
                    <th>Descrição</th>
                    {ehAdmin && <th className="col-acoes">Ações</th>}
                  </tr>
                </thead>

                <tbody>
                  {carregando && (
                    <tr>
                      <td colSpan={ehAdmin ? 6 : 5} className="tabela-status">
                        Carregando...
                      </td>
                    </tr>
                  )}

                  {!carregando && vacinasFiltradas.length === 0 && (
                    <tr>
                      <td colSpan={ehAdmin ? 6 : 5} className="tabela-status">
                        {buscaCatalogo.trim()
                          ? 'Nenhuma vacina encontrada com essa busca.'
                          : 'Nenhuma vacina cadastrada ainda.'}
                      </td>
                    </tr>
                  )}

                  {!carregando &&
                    vacinasFiltradas.map((vacina) => (
                      <tr key={vacina.id}>
                        <td className="col-nome">{vacina.nome}</td>
                        <td>{vacina.fabricante}</td>
                        <td>{vacina.quantidade_doses}</td>
                        <td>
                          {vacina.intervalo_dias}{' '}
                          {vacina.intervalo_dias === 1 ? 'dia' : 'dias'}
                        </td>
                        <td className="col-descricao">{vacina.descricao || '—'}</td>

                        {ehAdmin && (
                          <td className="col-acoes">
                            <button
                              className="btn-icone"
                              title="Editar vacina"
                              aria-label="Editar vacina"
                              onClick={() => {
                                setAviso('')
                                setModalVacina({ vacina })
                              }}
                            >
                              <Pencil size={16} />
                            </button>

                            <button
                              className="btn-icone btn-icone-perigo"
                              title="Excluir vacina"
                              aria-label="Excluir vacina"
                              onClick={() => pedirExclusao('vacina', vacina)}
                            >
                              <Trash2 size={16} />
                            </button>
                          </td>
                        )}
                      </tr>
                    ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>

      {modalVacina && (
        <VacinaFormModal
          vacina={modalVacina.vacina}
          onClose={() => setModalVacina(null)}
          onSalvo={salvouVacina}
        />
      )}

      {modalAplicacao && (
        <AplicacaoVacinaFormModal
          aplicacao={modalAplicacao.aplicacao}
          animais={animais}
          vacinas={vacinas}
          onClose={() => setModalAplicacao(null)}
          onSalvo={salvouAplicacao}
        />
      )}

      {alvoExclusao && (
        <ConfirmDialog
          titulo={
            alvoExclusao.tipo === 'vacina' ? 'Excluir vacina' : 'Excluir aplicação'
          }
          mensagem={
            alvoExclusao.tipo === 'vacina'
              ? `Tem certeza que deseja excluir a vacina "${alvoExclusao.item.nome}"?`
              : `Tem certeza que deseja excluir a aplicação de "${
                  alvoExclusao.item.vacinaNome
                }" em "${alvoExclusao.item.animalNome}"?`
          }
          confirmando={excluindo}
          erro={erroExclusao}
          textoConfirmar="Excluir"
          textoConfirmando="Excluindo..."
          onConfirmar={confirmarExclusao}
          onCancelar={() => setAlvoExclusao(null)}
        />
      )}
    </div>
  )
}

export default Vacinas
