
import { useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import {
  Search,
  ShoppingCart,
  Package,
  Plus,
  Minus,
} from "lucide-react";

import "../Dashboard/Dashboard.css";
import "./Produtos.css";

import Sidebar from "../../components/Sidebar/Sidebar";
import { useAuth } from "../../contexts/AuthContext";
import api from "../../services/api";
import tratarErro from "../../services/tratarErro";

const moeda = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function Produtos() {
  const { usuario } = useAuth();
  const navigate = useNavigate();

  const ehCliente = usuario?.perfil === "Cliente";

  const [sidebarAberto, setSidebarAberto] = useState(true);
  const [produtos, setProdutos] = useState([]);
  const [busca, setBusca] = useState("");
  const [quantidades, setQuantidades] = useState({});
  const [carregando, setCarregando] = useState(true);
  const [adicionando, setAdicionando] = useState(null);
  const [erro, setErro] = useState("");
  const [aviso, setAviso] = useState("");

  useEffect(() => {
    if (!ehCliente) return;

    let cancelado = false;

    async function carregarProdutos() {
      try {
        const resposta = await api.get("/produtos/", {
          params: {
            skip: 0,
            limit: 100,
            em_estoque: true,
            sort_by: "nome",
            order: "asc",
          },
        });

        if (!cancelado) {
          setProdutos(resposta.data);
        }
      } catch (error) {
        if (!cancelado) {
          setErro(tratarErro(error).mensagem);
        }
      } finally {
        if (!cancelado) {
          setCarregando(false);
        }
      }
    }

    carregarProdutos();

    return () => {
      cancelado = true;
    };
  }, [ehCliente]);

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  if (!ehCliente) {
    return <Navigate to="/dashboard" replace />;
  }

  const produtosFiltrados = produtos.filter((produto) =>
    `${produto.nome} ${produto.descricao}`
      .toLowerCase()
      .includes(busca.trim().toLowerCase())
  );

  async function adicionarAoCarrinho(produto) {
    setAdicionando(produto.id);
    setErro("");
    setAviso("");

    try {
      /*
       * Na próxima etapa vamos conectar esta ação
       * ao carrinho do cliente no backend.
       */
      setAviso(
        `Produto "${produto.nome}" selecionado.`
      );
    } catch (error) {
      setErro(tratarErro(error).mensagem);
    } finally {
      setAdicionando(null);
    }
  }

  return (
    <div className="dashboard">
      <Sidebar
        perfil={usuario.perfil}
        setSidebarAberto={setSidebarAberto}
      />

      <main
        className={`dashboard-content ${
          sidebarAberto ? "aberto" : "fechado"
        }`}
      >
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h1>Nossos produtos</h1>
            <p>
              Encontre produtos para cuidar melhor do seu pet.
            </p>
          </div>

          <button
            type="button"
            className="produtos-carrinho-link"
            onClick={() => navigate("/compras")}
          >
            <ShoppingCart size={19} />
            Minhas compras
          </button>
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
          <p className="produtos-mensagem">
            Carregando produtos...
          </p>
        ) : produtosFiltrados.length === 0 ? (
          <div className="produtos-vazio">
            <Package size={38} />
            <h2>Nenhum produto encontrado</h2>
            <p>
              Tente pesquisar por outro nome ou descrição.
            </p>
          </div>
        ) : (
          <section
            className="produtos-grade"
            aria-label="Produtos disponíveis"
          >
            {produtosFiltrados.map((produto) => (
              <article
                className="produto-card"
                key={produto.id}
              >
                <div className="produto-imagem">
                  <Package size={48} />
                </div>

                <div className="produto-conteudo">
                  <h2>{produto.nome}</h2>

                  <p className="produto-descricao">
                    {produto.descricao}
                  </p>

                  <strong className="produto-preco">
                    {moeda.format(produto.preco)}
                  </strong>

                  <p className="produto-estoque">
                    {produto.estoque}{" "}
                    {produto.estoque === 1
                      ? "unidade disponível"
                      : "unidades disponíveis"}
                  </p>

                  <div className="produto-acoes">
                    <div className="produto-quantidade">
                      <button
                        type="button"
                        aria-label={`Diminuir quantidade de ${produto.nome}`}
                        disabled={
                          (quantidades[produto.id] || 1) <= 1
                        }
                        onClick={() =>
                          setQuantidades((atual) => ({
                            ...atual,
                            [produto.id]: Math.max(
                              1,
                              (atual[produto.id] || 1) - 1
                            ),
                          }))
                        }
                      >
                        <Minus size={15} />
                      </button>

                      <span>
                        {quantidades[produto.id] || 1}
                      </span>

                      <button
                        type="button"
                        aria-label={`Aumentar quantidade de ${produto.nome}`}
                        disabled={
                          (quantidades[produto.id] || 1) >=
                          produto.estoque
                        }
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
                      disabled={adicionando === produto.id}
                      onClick={() =>
                        adicionarAoCarrinho(produto)
                      }
                    >
                      <ShoppingCart size={16} />
                      {adicionando === produto.id
                        ? "Adicionando..."
                        : "Adicionar"}
                    </button>
                  </div>
                </div>
              </article>
            ))}
          </section>
        )}
      </main>
    </div>
  );
}

export default Produtos;
