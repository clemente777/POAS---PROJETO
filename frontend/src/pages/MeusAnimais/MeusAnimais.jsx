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

  const [busca, setBusca] = useState('')
  const [buscaAplicada, setBuscaAplicada] = useState('')
  const [ordem, setOrdem] = useState('asc')
  const [pagina, setPagina] = useState(1)

  const [modalForm, setModalForm] = useState(null)
  const [modalHistoricoId, setModalHistoricoId] = useState(null)
  const [animalVacinas, setAnimalVacinas] = useState(null)
  const [animalParaExcluir, setAnimalParaExcluir] = useState(null)
  const [excluindo, setExcluindo] = useState(false)
  const [erroExclusao, setErroExclusao] = useState('')

  // ---------------------------------------------------------------
  // Cadastro de cliente do usuário logado
  // ---------------------------------------------------------------

  const email = usuario?.email

  // Resultado da busca do cliente, junto com o e-mail que o gerou.
  // Se o e-mail atual for diferente do guardado, ainda estamos carregando.
  const [resultadoCliente, setResultadoCliente] = useState({
    email: null,
    cliente: null,
    erro: '',
  })

  useEffect(() => {
    if (!email) return

    let ignorar = false

    api
      .get('/clientes/', {
        params: { email, limit: 1 },
      })
      .then((res) => {
        if (ignorar) return

        const clientes = Array.isArray(res.data)
          ? res.data
          : res.data?.items || res.data?.clientes || []

        const encontrado =
          clientes.find((cliente) => cliente.email === email) || clientes[0]

        setResultadoCliente({
          email,
          cliente: encontrado || null,
          erro: encontrado ? '' : 'Não encontramos seu cadastro de cliente.',
        })
      })
      .catch(() => {
        if (ignorar) return

        setResultadoCliente({
          email,
          cliente: null,
          erro: 'Não foi possível carregar seus dados.',
        })
      })

    return () => {
      ignorar = true
    }
  }, [email])

  const clienteAtual = Boolean(email) && resultadoCliente.email === email

  const carregandoCliente = Boolean(email) && !clienteAtual
  const meuCliente = clienteAtual ? resultadoCliente.cliente : null
  const erroCliente = !email
    ? 'Não foi possível identificar o usuário conectado.'
    : clienteAtual
      ? resultadoCliente.erro
      : ''

  // ---------------------------------------------------------------
  // Lista de animais
  // ---------------------------------------------------------------

  // Incrementar força a lista a ser buscada de novo (após salvar/excluir).
  const [recarga, setRecarga] = useState(0)

  // Resultado da última busca, junto com a "chave" dos filtros que o gerou.
  // Se a chave atual for diferente da guardada, ainda estamos carregando.
  const [resultado, setResultado] = useState({
    chave: null,
    animais: [],
    erro: '',
  })

  const chaveBusca = `${pagina}|${buscaAplicada}|${ordem}|${recarga}`

  useEffect(() => {
    // Se os filtros mudarem antes da resposta chegar, ignora a resposta antiga.
    let ignorar = false

    api
      .get('/animais/', {
        params: {
          pagina,
          limite: LIMITE_POR_PAGINA,
          nome: buscaAplicada || undefined,
          ordem,
        },
      })
      .then((res) => {
        if (ignorar) return

        const dados = Array.isArray(res.data)
          ? res.data
          : Array.isArray(res.data?.items)
            ? res.data.items
            : Array.isArray(res.data?.animais)
              ? res.data.animais
              : []

        setResultado({ chave: chaveBusca, animais: dados, erro: '' })
      })
      .catch((err) => {
        if (ignorar) return

        setResultado({
          chave: chaveBusca,
          animais: [],
          erro:
            err?.response?.data?.detail || 'Não foi possível carregar seus animais.',
        })
      })

    return () => {
      ignorar = true
    }
  }, [chaveBusca, pagina, buscaAplicada, ordem])

  const carregando = resultado.chave !== chaveBusca
  const animais = resultado.animais
  const erro = carregando ? '' : resultado.erro

  // Busca a lista de novo (mantém o nome usado pelos handlers abaixo).
  function carregarAnimais() {
    setRecarga((n) => n + 1)
  }

  function handleBuscar(e) {
    e.preventDefault()
    setPagina(1)
    setBuscaAplicada(busca.trim())
  }

  function alternarOrdem() {
    setOrdem((atual) => (atual === 'asc' ? 'desc' : 'asc'))
    setPagina(1)
  }

  function fecharForm() {
    setModalForm(null)
  }

  function salvouForm() {
    setModalForm(null)
    carregarAnimais()
  }

  async function confirmarExclusao() {
    if (!animalParaExcluir) return

    setExcluindo(true)
    setErroExclusao('')

    try {
      await api.delete(`/animais/${animalParaExcluir.id}`)
      setAnimalParaExcluir(null)
      await carregarAnimais()
    } catch (err) {
      setErroExclusao(
        err?.response?.data?.detail || 'Não foi possível excluir este animal.'
      )
    } finally {
      setExcluindo(false)
    }
  }

  const nomeUsuario =
    usuario?.nome ||
    usuario?.nome_completo ||
    usuario?.nomeCompleto ||
    usuario?.name ||
    'usuário'

  return (
    <div className="animais-page">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="animais-header">
          <div>
            <h1>Olá, {nomeUsuario}!</h1>
            <p>Seus pets cadastrados no Petonline24h</p>
          </div>

          <button
            className="btn-novo"
            onClick={() => setModalForm('novo')}
            disabled={carregandoCliente || !meuCliente}
            title={erroCliente || ''}
          >
            <Plus size={18} />
            Novo animal
          </button>
        </header>

        {erroCliente && <p className="animais-erro">{erroCliente}</p>}

        <div className="animais-toolbar">
          <form className="busca-form" onSubmit={handleBuscar}>
            <Search size={16} />

            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar por nome..."
            />
          </form>

          <button className="btn-ordem" onClick={alternarOrdem} type="button">
            <ArrowUpDown size={16} />
            Nome ({ordem === 'asc' ? 'A-Z' : 'Z-A'})
          </button>
        </div>

        {erro && <p className="animais-erro">{erro}</p>}

        <div className="animais-tabela-wrapper">
          <table className="animais-tabela">
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
                    style={{ textAlign: 'center', padding: '24px' }}
                  >
                    Animal não encontrado.
                  </td>
                </tr>
              )}

              {!carregando &&
                !erro &&
                animais.map((animal) => (
                  <tr key={animal.id}>
                    <td className="col-nome">{animal.nome}</td>
                    <td>{animal.especie}</td>
                    <td>{animal.raca}</td>
                    <td>{animal.idade} anos</td>

                    <td className="col-acoes">
                      <button
                        className="btn-icone"
                        title="Vacinas"
                        aria-label="Carteira de vacinação"
                        onClick={() => setAnimalVacinas(animal)}
                      >
                        <Syringe size={16} />
                      </button>

                      <button
                        className="btn-icone"
                        title="Histórico"
                        onClick={() => setModalHistoricoId(animal.id)}
                      >
                        <History size={16} />
                      </button>

                      <button
                        className="btn-icone"
                        title="Editar"
                        onClick={() => setModalForm(animal)}
                      >
                        <Pencil size={16} />
                      </button>

                      <button
                        className="btn-icone btn-icone-perigo"
                        title="Excluir"
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

        <div className="animais-paginacao">
          <button
            onClick={() => setPagina((p) => Math.max(1, p - 1))}
            disabled={pagina === 1 || carregando}
          >
            <ChevronLeft size={16} />
            Anterior
          </button>

          <span>Página {pagina}</span>

          <button
            onClick={() => setPagina((p) => p + 1)}
            disabled={carregando || animais.length < LIMITE_POR_PAGINA}
          >
            Próxima
            <ChevronRight size={16} />
          </button>
        </div>
      </main>

      {modalForm && (
        <AnimalFormModal
          animal={modalForm === 'novo' ? null : modalForm}
          clienteFixo={modalForm === 'novo' ? meuCliente : null}
          onClose={fecharForm}
          onSalvo={salvouForm}
        />
      )}

      {modalHistoricoId && (
        <AnimalHistoricoModal
          animalId={modalHistoricoId}
          onClose={() => setModalHistoricoId(null)}
        />
      )}

      {animalVacinas && (
        <AnimalVacinasModal
          animal={animalVacinas}
          onClose={() => setAnimalVacinas(null)}
        />
      )}

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
