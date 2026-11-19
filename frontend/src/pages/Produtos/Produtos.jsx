import { useEffect, useState } from 'react'
import { Navigate, useNavigate } from 'react-router-dom'
import {
  Search,
  ShoppingCart,
  Package,
  Plus,
  Minus,
  Pencil,
  Trash2,
  X,
  Save,
} from 'lucide-react'

import '../Dashboard/Dashboard.css'
import './Produtos.css'

import Sidebar from '../../components/Sidebar/Sidebar'
import { useAuth } from '../../contexts/AuthContext'
import api from '../../services/api'
import tratarErro from '../../services/tratarErro'

const moeda = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})

const FORM_INICIAL = {
  nome: '',
  descricao: '',
  preco: '',
  estoque: '',
}

function Produtos() {
  const { usuario } = useAuth()
  const navigate = useNavigate()

  const ehAdmin = usuario?.perfil === 'Administrador'
  const ehCliente = usuario?.perfil === 'Cliente'
  const acessoPermitido = ehAdmin || ehCliente

  const [sidebarAberto, setSidebarAberto] = useState(true)
  const [produtos, setProdutos] = useState([])
  const [busca, setBusca] = useState('')
  const [quantidades, setQuantidades] = useState({})
  const [carregando, setCarregando] = useState(true)
  const [adicionando, setAdicionando] = useState(null)

  const [erro, setErro] = useState('')
  const [aviso, setAviso] = useState('')

  const [modalAberto, setModalAberto] = useState(false)
  const [produtoEditando, setProdutoEditando] = useState(null)
  const [formulario, setFormulario] = useState(FORM_INICIAL)
  const [salvando, setSalvando] = useState(false)

  async function carregarProdutos() {
    setCarregando(true)
    setErro('')

    try {
      const resposta = await api.get('/produtos/', {
        params: {
          skip: 0,
          limit: 100,
          ...(ehCliente ? { em_estoque: true } : {}),
          sort_by: 'nome',
          order: 'asc',
        },
      })

      setProdutos(resposta.data)
    } catch (error) {
      setErro(tratarErro(error).mensagem)
    } finally {
      setCarregando(false)
    }
  }

  useEffect(() => {
    if (acessoPermitido) {
      carregarProdutos()
    } else {
      setCarregando(false)
    }
  }, [acessoPermitido])

  if (!usuario) {
    return <Navigate to="/login" replace />
  }

  if (!acessoPermitido) {
    return <Navigate to="/dashboard" replace />
  }

  const produtosFiltrados = produtos.filter((produto) =>
    `${produto.nome} ${produto.descricao}`
      .toLowerCase()
      .includes(busca.trim().toLowerCase())
  )

  function abrirCadastro() {
    setProdutoEditando(null)
    setFormulario(FORM_INICIAL)
    setErro('')
    setModalAberto(true)
  }

  function abrirEdicao(produto) {
    setProdutoEditando(produto)

    setFormulario({
      nome: produto.nome,
      descricao: produto.descricao,
      preco: String(produto.preco),
      estoque: String(produto.estoque),
    })

    setErro('')
    setModalAberto(true)
  }

  function fecharModal() {
    if (salvando) return

    setModalAberto(false)
    setProdutoEditando(null)
    setFormulario(FORM_INICIAL)
  }

  function atualizarCampo(e) {
    const { name, value } = e.target

    setFormulario((atual) => ({
      ...atual,
      [name]: value,
    }))
  }

  async function salvarProduto(e) {
    e.preventDefault()

    setErro('')
    setAviso('')

    const preco = Number(formulario.preco)
    const estoque = Number(formulario.estoque)

    if (
      !formulario.nome.trim() ||
      !formulario.descricao.trim() ||
      !formulario.preco ||
      !formulario.estoque
    ) {
      setErro('Preencha todos os campos.')
      return
    }

    if (!Number.isFinite(preco) || preco <= 0) {
      setErro('O preço deve ser maior que zero.')
      return
    }

    if (!Number.isInteger(estoque) || estoque < 0) {
      setErro('O estoque deve ser um número inteiro não negativo.')
      return
    }

    const dados = {
      nome: formulario.nome.trim(),
      descricao: formulario.descricao.trim(),
      preco,
      estoque,
    }

    setSalvando(true)

    try {
      if (produtoEditando) {
        await api.put(`/produtos/${produtoEditando.id}`, dados)
        setAviso('Produto atualizado com sucesso.')
      } else {
        await api.post('/produtos/', dados)
        setAviso('Produto cadastrado com sucesso.')
      }

      setModalAberto(false)
      setProdutoEditando(null)
      setFormulario(FORM_INICIAL)

      await carregarProdutos()
    } catch (error) {
      setErro(tratarErro(error).mensagem)
    } finally {
      setSalvando(false)
    }
  }

  async function excluirProduto(produto) {
    const confirmou = window.confirm(
      `Deseja realmente excluir o produto "${produto.nome}"?`
    )

    if (!confirmou) return

    setErro('')
    setAviso('')

    try {
      await api.delete(`/produtos/${produto.id}`)

      setAviso('Produto excluído com sucesso.')
      await carregarProdutos()
    } catch (error) {
      setErro(tratarErro(error).mensagem)
    }
  }

  async function obterCarrinhoId() {
    const { data: carrinhos } = await api.get('/carrinhos/', {
      params: { limit: 1 },
    })

    if (carrinhos[0]) {
      return carrinhos[0].id
    }

    const { data: clientes } = await api.get('/clientes/', {
      params: { limit: 1 },
    })

    const cliente = clientes[0]

    if (!cliente) {
      throw new Error('Cadastro de cliente não encontrado.')
    }

    const { data: novoCarrinho } = await api.post('/carrinhos/', {
      cliente_id: cliente.id,
    })

    return novoCarrinho.id
  }

  async function adicionarAoCarrinho(produto) {
    const quantidade = quantidades[produto.id] || 1

    setAdicionando(produto.id)
    setErro('')
    setAviso('')

    try {
      const carrinhoId = await obterCarrinhoId()

      await api.post('/itens-carrinho/', {
        carrinho_id: carrinhoId,
        produto_id: produto.id,
        quantidade,
      })

      setQuantidades((atual) => ({
        ...atual,
        [produto.id]: 1,
      }))

      setAviso(`${quantidade} × "${produto.nome}" adicionado ao carrinho.`)
    } catch (error) {
      setErro(tratarErro(error).mensagem)
    } finally {
      setAdicionando(null)
    }
  }

  return (
    <div className="dashboard">
      <Sidebar perfil={usuario.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`dashboard-content ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h1>{ehAdmin ? 'Gerenciamento de produtos' : 'Nossos produtos'}</h1>

            <p>
              {ehAdmin
                ? 'Cadastre, atualize e gerencie os produtos da loja.'
                : 'Encontre produtos para cuidar melhor do seu pet.'}
            </p>
          </div>

          {ehAdmin ? (
            <button type="button" className="produtos-novo" onClick={abrirCadastro}>
              <Plus size={18} />
              Novo produto
            </button>
          ) : (
            <button
              type="button"
              className="produtos-carrinho-link"
              onClick={() => navigate('/compras')}
            >
              <ShoppingCart size={19} />
              Minhas compras
            </button>
          )}
        </header>

        <div className="produtos-busca">
          <Search size={20} />

          <input
            type="search"
            placeholder="Buscar produto..."
            value={busca}
            onChange={(e) => setBusca(e.target.value)}
            aria-label="Buscar produtos"
          />
        </div>

        {erro && (
          <p className="dashboard-erro" role="alert">
            {erro}
          </p>
        )}

        {aviso && (
          <p className="produtos-aviso" role="status">
            {aviso}
          </p>
        )}

        {carregando ? (
          <p className="produtos-mensagem">Carregando produtos...</p>
        ) : produtosFiltrados.length === 0 ? (
          <div className="produtos-vazio">
            <Package size={38} />

            <h2>Nenhum produto encontrado</h2>

            <p>
              {ehAdmin
                ? 'Cadastre um produto ou altere sua pesquisa.'
                : 'Tente pesquisar por outro nome ou descrição.'}
            </p>
          </div>
        ) : (
          <section className="produtos-grade" aria-label="Produtos disponíveis">
            {produtosFiltrados.map((produto) => (
              <article className="produto-card" key={produto.id}>
                <div className="produto-imagem">
                  <Package size={48} />
                </div>

                <div className="produto-conteudo">
                  <h2>{produto.nome}</h2>

                  <p className="produto-descricao">{produto.descricao}</p>

                  <strong className="produto-preco">
                    {moeda.format(produto.preco)}
                  </strong>

                  <p className="produto-estoque">
                    {produto.estoque}{' '}
                    {produto.estoque === 1
                      ? 'unidade disponível'
                      : 'unidades disponíveis'}
                  </p>

                  {ehAdmin ? (
                    <div className="produto-admin-acoes">
                      <button
                        type="button"
                        className="produto-editar"
                        onClick={() => abrirEdicao(produto)}
                      >
                        <Pencil size={16} />
                        Editar
                      </button>

                      <button
                        type="button"
                        className="produto-excluir"
                        onClick={() => excluirProduto(produto)}
                      >
                        <Trash2 size={16} />
                        Excluir
                      </button>
                    </div>
                  ) : (
                    <div className="produto-acoes">
                      <div className="produto-quantidade">
                        <button
                          type="button"
                          aria-label={`Diminuir quantidade de ${produto.nome}`}
                          disabled={(quantidades[produto.id] || 1) <= 1}
                          onClick={() =>
                            setQuantidades((atual) => ({
                              ...atual,
                              [produto.id]: Math.max(1, (atual[produto.id] || 1) - 1),
                            }))
                          }
                        >
                          <Minus size={15} />
                        </button>

                        <span>{quantidades[produto.id] || 1}</span>

                        <button
                          type="button"
                          aria-label={`Aumentar quantidade de ${produto.nome}`}
                          disabled={(quantidades[produto.id] || 1) >= produto.estoque}
                          onClick={() =>
                            setQuantidades((atual) => ({
                              ...atual,
                              [produto.id]: Math.min(
                                produto.estoque,
                                (atual[produto.id] || 1) + 1
                              ),
                            }))
                          }
                        >
                          <Plus size={15} />
                        </button>
                      </div>

                      <button
                        type="button"
                        className="produto-adicionar"
                        disabled={adicionando === produto.id || produto.estoque <= 0}
                        onClick={() => adicionarAoCarrinho(produto)}
                      >
                        <ShoppingCart size={16} />
                        {adicionando === produto.id ? 'Adicionando...' : 'Adicionar'}
                      </button>
                    </div>
                  )}
                </div>
              </article>
            ))}
          </section>
        )}
      </main>

      {ehAdmin && modalAberto && (
        <div
          className="produto-modal-overlay"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) fecharModal()
          }}
        >
          <section
            className="produto-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="produto-modal-titulo"
          >
            <header className="produto-modal-header">
              <div>
                <h2 id="produto-modal-titulo">
                  {produtoEditando ? 'Editar produto' : 'Novo produto'}
                </h2>

                <p>Informe os dados do produto.</p>
              </div>

              <button
                type="button"
                aria-label="Fechar"
                onClick={fecharModal}
                disabled={salvando}
              >
                <X size={21} />
              </button>
            </header>

            <form onSubmit={salvarProduto}>
              <label htmlFor="produto-nome">Nome do produto</label>
              <input
                id="produto-nome"
                name="nome"
                value={formulario.nome}
                onChange={atualizarCampo}
                maxLength={100}
                required
              />

              <label htmlFor="produto-descricao">Descrição</label>
              <textarea
                id="produto-descricao"
                name="descricao"
                value={formulario.descricao}
                onChange={atualizarCampo}
                maxLength={255}
                rows={3}
                required
              />

              <div className="produto-modal-campos">
                <div>
                  <label htmlFor="produto-preco">Preço (R$)</label>
                  <input
                    id="produto-preco"
                    name="preco"
                    type="number"
                    min="0.01"
                    step="0.01"
                    value={formulario.preco}
                    onChange={atualizarCampo}
                    required
                  />
                </div>

                <div>
                  <label htmlFor="produto-estoque">Estoque</label>
                  <input
                    id="produto-estoque"
                    name="estoque"
                    type="number"
                    min="0"
                    step="1"
                    value={formulario.estoque}
                    onChange={atualizarCampo}
                    required
                  />
                </div>
              </div>

              <footer className="produto-modal-acoes">
                <button
                  type="button"
                  className="produto-cancelar"
                  onClick={fecharModal}
                  disabled={salvando}
                >
                  Cancelar
                </button>

                <button type="submit" className="produto-salvar" disabled={salvando}>
                  <Save size={17} />
                  {salvando ? 'Salvando...' : 'Salvar produto'}
                </button>
              </footer>
            </form>
          </section>
        </div>
      )}
    </div>
  )
}

export default Produtos
