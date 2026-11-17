
import { useEffect, useState } from 'react'
import {
  Plus,
  Search,
  Pencil,
  Trash2,
  History,
  Syringe,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from 'lucide-react'

import api from '../../services/api'
import { useAuth } from '../../contexts/AuthContext'

import Sidebar from '../../components/Sidebar/Sidebar'
import AnimalFormModal from '../../components/AnimalFormModal/AnimalFormModal'
import AnimalHistoricoModal from '../../components/AnimalHistoricoModal/AnimalHistoricoModal'
import AnimalVacinasModal from '../../components/AnimalVacinasModal/AnimalVacinasModal'
import ConfirmDialog from '../../components/ConfirmDialog/ConfirmDialog'

import '../Animais/Animais.css'

const LIMITE_POR_PAGINA = 10

function MeusAnimais() {
  const { usuario } = useAuth()

  const [sidebarAberto, setSidebarAberto] = useState(true)

  // ==================================================
  // FILTROS E PAGINAÇÃO
  // ==================================================

  const [busca, setBusca] = useState('')
  const [buscaAplicada, setBuscaAplicada] = useState('')
  const [ordem, setOrdem] = useState('asc')
  const [pagina, setPagina] = useState(1)
  const [recarga, setRecarga] = useState(0)

  // ==================================================
  // MODAIS
  // ==================================================

  const [modalForm, setModalForm] = useState(null)
  const [modalHistoricoId, setModalHistoricoId] = useState(null)
  const [animalVacinas, setAnimalVacinas] = useState(null)
  const [animalParaExcluir, setAnimalParaExcluir] = useState(null)

  const [excluindo, setExcluindo] = useState(false)
  const [erroExclusao, setErroExclusao] = useState('')

  // ==================================================
  // CLIENTE DO USUÁRIO LOGADO
  // ==================================================

  const email = usuario?.email

  const [resultadoCliente, setResultadoCliente] = useState({
    email: null,
    cliente: null,
    erro: '',
  })

  useEffect(() => {
    if (!email) return

    let ignorar = false

    async function buscarCliente() {
      try {
        const resposta = await api.get('/clientes/', {
          params: {
            email,
            limit: 1,
          },
        })

        if (ignorar) return

        const clientes = Array.isArray(resposta.data)
          ? resposta.data
          : Array.isArray(resposta.data?.items)
            ? resposta.data.items
            : Array.isArray(resposta.data?.clientes)
              ? resposta.data.clientes
              : []

        const encontrado =
          clientes.find((cliente) => cliente.email === email) ||
          clientes[0] ||
          null

        setResultadoCliente({
          email,
          cliente: encontrado,
          erro: encontrado
            ? ''
            : 'Não encontramos seu cadastro de cliente.',
        })
      } catch (error) {
        if (ignorar) return

        console.error('Erro ao carregar cliente:', error)

        setResultadoCliente({
          email,
          cliente: null,
          erro: 'Não foi possível carregar seus dados.',
        })
      }
    }

    buscarCliente()

    return () => {
      ignorar = true
    }
  }, [email])

  const clienteAtual =
    Boolean(email) && resultadoCliente.email === email

  const carregandoCliente =
    Boolean(email) && !clienteAtual

  const meuCliente =
    clienteAtual ? resultadoCliente.cliente : null

  const erroCliente = !email
    ? 'Não foi possível identificar o usuário conectado.'
    : clienteAtual
      ? resultadoCliente.erro
      : ''

  // ==================================================
  // LISTAGEM DE ANIMAIS
  // ==================================================

  const [resultado, setResultado] = useState({
    chave: null,
    animais: [],
    erro: '',
  })

  const chaveBusca =
    `${pagina}|${buscaAplicada}|${ordem}|${recarga}`

  useEffect(() => {
    let ignorar = false

    const chaveAtual =
      `${pagina}|${buscaAplicada}|${ordem}|${recarga}`

    async function buscarAnimais() {
      try {
        const resposta = await api.get('/animais/', {
          params: {
            pagina,
            limite: LIMITE_POR_PAGINA,
            nome: buscaAplicada || undefined,
            ordem,
          },
        })

        if (ignorar) return

        const dados = Array.isArray(resposta.data)
          ? resposta.data
          : Array.isArray(resposta.data?.items)
            ? resposta.data.items
            : Array.isArray(resposta.data?.animais)
              ? resposta.data.animais
              : []

        setResultado({
          chave: chaveAtual,
          animais: dados,
          erro: '',
        })
      } catch (error) {
        if (ignorar) return

        console.error('Erro ao carregar animais:', error)

        setResultado({
          chave: chaveAtual,
          animais: [],
          erro:
            error?.response?.data?.detail ||
            'Não foi possível carregar seus animais.',
        })
      }
    }

    buscarAnimais()

    return () => {
      ignorar = true
    }
  }, [pagina, buscaAplicada, ordem, recarga])

  const carregando = resultado.chave !== chaveBusca

  const animais = resultado.animais

  const erro = carregando ? '' : resultado.erro

  // ==================================================
  // ATUALIZAR LISTAGEM
  // ==================================================

  function carregarAnimais() {
    setRecarga((atual) => atual + 1)
  }

  // ==================================================
  // BUSCA
  // ==================================================

  function handleBuscar(evento) {
    evento.preventDefault()

    setPagina(1)
    setBuscaAplicada(busca.trim())
  }

  // ==================================================
  // ORDENAÇÃO
  // ==================================================

  function alternarOrdem() {
    setOrdem((atual) =>
      atual === 'asc' ? 'desc' : 'asc'
    )

    setPagina(1)
  }

  // ==================================================
  // MODAL DE CADASTRO E EDIÇÃO
  // ==================================================

  function fecharForm() {
    setModalForm(null)
  }

  function salvouForm() {
    setModalForm(null)
    carregarAnimais()
  }

  // ==================================================
  // EXCLUIR ANIMAL
  // ==================================================

  async function confirmarExclusao() {
    if (!animalParaExcluir || excluindo) return

    setExcluindo(true)
    setErroExclusao('')

    try {
      await api.delete(`/animais/${animalParaExcluir.id}`)

      setAnimalParaExcluir(null)

      carregarAnimais()
    } catch (error) {
      console.error('Erro ao excluir animal:', error)

      setErroExclusao(
        error?.response?.data?.detail ||
        'Não foi possível excluir este animal.'
      )
    } finally {
      setExcluindo(false)
    }
  }

  // ==================================================
  // NOME DO USUÁRIO
  // ==================================================

  const nomeUsuario = String(
    usuario?.nome ||
    usuario?.nome_completo ||
    usuario?.nomeCompleto ||
    usuario?.name ||
    'usuário'
  )

  return (
    <div className="animais-page">

      <Sidebar
        perfil={usuario?.perfil}
        setSidebarAberto={setSidebarAberto}
      />

      <main
        className={`animais-content ${
          sidebarAberto ? 'aberto' : 'fechado'
        }`}
      >

        {/* CABEÇALHO */}

        <header className="animais-header">

          <div>
            <h1>Olá, {nomeUsuario}!</h1>
            <p>Seus pets cadastrados no Petonline24h</p>
          </div>

          <button
            className="btn-novo"
            type="button"
            onClick={() => setModalForm('novo')}
            disabled={carregandoCliente || !meuCliente}
            title={erroCliente || ''}
          >
            <Plus size={18} />
            Novo animal
          </button>

        </header>

        {/* ERRO DO CLIENTE */}

        {erroCliente && (
          <p className="animais-erro">
            {erroCliente}
          </p>
        )}

        {/* FERRAMENTAS DE BUSCA E ORDENAÇÃO */}

        <div className="animais-toolbar">

          <form
            className="busca-form"
            onSubmit={handleBuscar}
          >
            <Search size={16} />

            <input
              type="search"
              value={busca}
              onChange={(evento) => setBusca(evento.target.value)}
              placeholder="Buscar por nome..."
            />
          </form>

          <button
            className="btn-ordem"
            type="button"
            onClick={alternarOrdem}
          >
            <ArrowUpDown size={16} />
            Nome ({ordem === 'asc' ? 'A-Z' : 'Z-A'})
          </button>

        </div>

        {/* ERRO DA LISTAGEM */}

        {erro && (
          <p className="animais-erro">
            {erro}
          </p>
        )}

        {/* TABELA DE ANIMAIS */}

        <div className="animais-tabela-wrapper">

          <table className="animais-tabela animais-tabela--cartoes">

            <thead>
              <tr>
                <th>Nome</th>
                <th>Espécie</th>
                <th>Raça</th>
                <th>Idade</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>

            <tbody>

              {carregando && (
                <tr>
                  <td colSpan={5} className="tabela-status">
                    Carregando...
                  </td>
                </tr>
              )}

              {!carregando && !erro && animais.length === 0 && (
                <tr>
                  <td
                    colSpan={5}
                    className="tabela-status"
                    style={{
                      textAlign: 'center',
                      padding: '24px',
                    }}
                  >
                    Animal não encontrado.
                  </td>
                </tr>
              )}

              {!carregando &&
                !erro &&
                animais.map((animal) => (
                  <tr key={animal.id}>

                    <td
                      className="col-nome"
                      data-label="Nome"
                    >
                      {animal.nome}
                    </td>

                    <td data-label="Espécie">
                      {animal.especie}
                    </td>

                    <td data-label="Raça">
                      {animal.raca}
                    </td>

                    <td data-label="Idade">
                      {animal.idade} anos
                    </td>

                    <td className="col-acoes" data-label="Ações">

                      <button
                        className="btn-icone"
                        type="button"
                        title="Vacinas"
                        aria-label="Carteira de vacinação"
                        onClick={() => setAnimalVacinas(animal)}
                      >
                        <Syringe size={16} />
                      </button>

                      <button
                        className="btn-icone"
                        type="button"
                        title="Histórico"
                        aria-label="Histórico do animal"
                        onClick={() => setModalHistoricoId(animal.id)}
                      >
                        <History size={16} />
                      </button>

                      <button
                        className="btn-icone"
                        type="button"
                        title="Editar"
                        aria-label={`Editar ${animal.nome}`}
                        onClick={() => setModalForm(animal)}
                      >
                        <Pencil size={16} />
                      </button>

                      <button
                        className="btn-icone btn-icone-perigo"
                        type="button"
                        title="Excluir"
                        aria-label={`Excluir ${animal.nome}`}
                        onClick={() => {
                          setAnimalParaExcluir(animal)
                          setErroExclusao('')
                        }}
                      >
                        <Trash2 size={16} />
                      </button>

                    </td>

                  </tr>
                ))}

            </tbody>

          </table>

        </div>

        {/* PAGINAÇÃO */}

        <div className="animais-paginacao">

          <button
            type="button"
            onClick={() =>
              setPagina((atual) => Math.max(1, atual - 1))
            }
            disabled={pagina === 1 || carregando}
          >
            <ChevronLeft size={16} />
            Anterior
          </button>

          <span>Página {pagina}</span>

          <button
            type="button"
            onClick={() => setPagina((atual) => atual + 1)}
            disabled={
              carregando ||
              animais.length < LIMITE_POR_PAGINA
            }
          >
            Próxima
            <ChevronRight size={16} />
          </button>

        </div>

      </main>

      {/* MODAL DE CADASTRO E EDIÇÃO */}

      {modalForm && (
        <AnimalFormModal
          animal={modalForm === 'novo' ? null : modalForm}
          clienteFixo={modalForm === 'novo' ? meuCliente : null}
          onClose={fecharForm}
          onSalvo={salvouForm}
        />
      )}

      {/* MODAL DE HISTÓRICO */}

      {modalHistoricoId && (
        <AnimalHistoricoModal
          animalId={modalHistoricoId}
          onClose={() => setModalHistoricoId(null)}
        />
      )}

      {/* MODAL DE VACINAS */}

      {animalVacinas && (
        <AnimalVacinasModal
          animal={animalVacinas}
          onClose={() => setAnimalVacinas(null)}
        />
      )}

      {/* CONFIRMAÇÃO DE EXCLUSÃO */}

      {animalParaExcluir && (
        <ConfirmDialog
          titulo="Excluir animal"
          mensagem={`Tem certeza que deseja excluir "${animalParaExcluir.nome}"? Essa ação não pode ser desfeita.`}
          confirmando={excluindo}
          erro={erroExclusao}
          textoConfirmar="Excluir"
          onConfirmar={confirmarExclusao}
          onCancelar={() => setAnimalParaExcluir(null)}
        />
      )}

    </div>
  )
}

export default MeusAnimais
