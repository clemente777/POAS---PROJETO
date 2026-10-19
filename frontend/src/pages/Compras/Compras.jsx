import "../Dashboard/Dashboard.css";
import "./Compras.css";

import { useEffect, useState } from "react";
import { Navigate } from "react-router-dom";
import {
  Check,
  ChevronDown,
  Minus,
  Package,
  Plus,
  Receipt,
  ShoppingBag,
  Trash2,
} from "lucide-react";

import api from "../../services/api";
import tratarErro from "../../services/tratarErro";
import Sidebar from "../../components/Sidebar/Sidebar";

import { useAuth } from "../../contexts/AuthContext";

const POR_PAGINA = 10;

const moeda = new Intl.NumberFormat("pt-BR", {
  style: "currency",
  currency: "BRL",
});

function formatarDataHora(iso) {
  if (!iso) return "";

  return new Date(iso).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function rotuloItens(quantidade) {
  return `${quantidade} ${quantidade === 1 ? "item" : "itens"}`;
}

// ==================================================
// API
// ==================================================

// O cliente só enxerga o próprio carrinho (1 por cliente).
// Os itens vêm só com produto_id, então buscamos os produtos
// para mostrar nome, preço e estoque.
async function buscarCarrinho() {
  const { data: carrinhos } = await api.get("/carrinhos/", {
    params: { limit: 1 },
  });

  const carrinho = carrinhos[0] ?? null;

  if (!carrinho) {
    return { carrinho: null, itens: [] };
  }

  const { data: itens } = await api.get("/itens-carrinho/", {
    params: { carrinho_id: carrinho.id, limit: 100 },
  });

  const ids = [...new Set(itens.map((item) => item.produto_id))];

  const produtos = await Promise.all(
    ids.map((id) =>
      api
        .get(`/produtos/${id}`)
        .then((resposta) => resposta.data)
        .catch(() => null)
    )
  );

  const produtoPorId = new Map(ids.map((id, i) => [id, produtos[i]]));

  return {
    carrinho,
    itens: itens.map((item) => ({
      ...item,
      produto: produtoPorId.get(item.produto_id),
    })),
  };
}

async function buscarPedidos(skip) {
  const { data } = await api.get("/pedidos/", {
    params: { skip, limit: POR_PAGINA },
  });

  return data;
}

// ==================================================
// PÁGINA
// ==================================================

function Compras() {
  const { usuario } = useAuth();

  const ehCliente = usuario?.perfil === "Cliente";

  const [sidebarAberto, setSidebarAberto] = useState(true);
  const [aba, setAba] = useState("carrinho");

  const [carrinho, setCarrinho] = useState(null);
  const [itens, setItens] = useState([]);

  const [pedidos, setPedidos] = useState([]);
  const [temMais, setTemMais] = useState(false);
  const [expandido, setExpandido] = useState(null);

  const [carregando, setCarregando] = useState(true);
  const [ocupado, setOcupado] = useState(false);
  const [erro, setErro] = useState("");
  const [aviso, setAviso] = useState("");

  useEffect(() => {
    if (!ehCliente) return;

    let cancelado = false;

    async function iniciar() {
      try {
        const [dadosCarrinho, listaPedidos] = await Promise.all([
          buscarCarrinho(),
          buscarPedidos(0),
        ]);

        if (cancelado) return;

        setCarrinho(dadosCarrinho.carrinho);
        setItens(dadosCarrinho.itens);
        setPedidos(listaPedidos);
        setTemMais(listaPedidos.length === POR_PAGINA);
      } catch (error) {
        if (!cancelado) setErro(tratarErro(error).mensagem);
      } finally {
        if (!cancelado) setCarregando(false);
      }
    }

    iniciar();

    return () => {
      cancelado = true;
    };
  }, [ehCliente]);

  if (!usuario) return <Navigate to="/login" replace />;
  if (!ehCliente) return <Navigate to="/dashboard" replace />;

  if (carregando) {
    return <div className="loading-dashboard">Carregando suas compras...</div>;
  }

  // ---------- derivados do carrinho ----------

  const totalUnidades = itens.reduce((soma, item) => soma + item.quantidade, 0);

  const total = itens.reduce(
    (soma, item) =>
      soma + (item.produto ? item.produto.preco * item.quantidade : 0),
    0
  );

  function problemaDoItem(item) {
    const produto = item.produto;

    if (!produto) {
      return "Este produto não está mais disponível. Remova-o para finalizar.";
    }

    if (produto.estoque === 0) {
      return "Sem estoque no momento. Remova-o para finalizar.";
    }

    if (item.quantidade > produto.estoque) {
      return `Restam só ${produto.estoque} em estoque. Reduza a quantidade para finalizar.`;
    }

    return "";
  }

  const comProblema = itens.filter((item) => problemaDoItem(item));
  const podeFinalizar = itens.length > 0 && comProblema.length === 0;

  // ---------- ações ----------

  async function executar(acao, { manterAviso = false } = {}) {
    setOcupado(true);
    setErro("");
    if (!manterAviso) setAviso("");

    try {
      await acao();
    } catch (error) {
      setErro(tratarErro(error).mensagem);
    } finally {
      setOcupado(false);
    }
  }

  function alterarQuantidade(item, nova) {
    if (ocupado || nova < 1) return;

    if (item.produto && nova > item.produto.estoque) return;

    executar(async () => {
      await api.put(`/itens-carrinho/${item.id}`, { quantidade: nova });

      setItens((atual) =>
        atual.map((i) => (i.id === item.id ? { ...i, quantidade: nova } : i))
      );
    });
  }

  function removerItem(item) {
    if (ocupado) return;

    executar(async () => {
      await api.delete(`/itens-carrinho/${item.id}`);

      setItens((atual) => atual.filter((i) => i.id !== item.id));
    });
  }

  function finalizarCompra() {
    if (ocupado || !carrinho || !podeFinalizar) return;

    executar(async () => {
      const { data } = await api.post(`/carrinhos/${carrinho.id}/finalizar`);

      setAviso(
        `Compra finalizada: ${rotuloItens(data.quantidade_itens)}, ${moeda.format(
          data.valor_total
        )}.`
      );

      const [novoCarrinho, lista] = await Promise.all([
        buscarCarrinho(),
        buscarPedidos(0),
      ]);

      setCarrinho(novoCarrinho.carrinho);
      setItens(novoCarrinho.itens);
      setPedidos(lista);
      setTemMais(lista.length === POR_PAGINA);
      setExpandido(data.pedido_id ?? lista[0]?.id ?? null);
      setAba("historico");
    });
  }

  function carregarMais() {
    if (ocupado) return;

    executar(
      async () => {
        const lista = await buscarPedidos(pedidos.length);

        setPedidos((atual) => [...atual, ...lista]);
        setTemMais(lista.length === POR_PAGINA);
      },
      { manterAviso: true }
    );
  }

  function trocarAba(nova) {
    setAba(nova);
    setErro("");
    setAviso("");
  }

  // ---------- tela ----------

  return (
    <div className="dashboard">
      <Sidebar perfil={usuario.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`dashboard-content ${sidebarAberto ? "aberto" : "fechado"}`}>
        <header className="dashboard-header">
          <div className="dashboard-title">
            <h1>Minhas compras</h1>
            <p>Acompanhe seu carrinho e as compras que você já fez</p>
          </div>
        </header>

        <div className="compras-tabs" role="tablist" aria-label="Minhas compras">
          <button
            type="button"
            role="tab"
            id="aba-carrinho"
            aria-selected={aba === "carrinho"}
            aria-controls="painel-carrinho"
            className="compras-tab"
            onClick={() => trocarAba("carrinho")}
          >
            <ShoppingBag size={16} />
            Carrinho
            {itens.length > 0 && <span className="compras-badge">{itens.length}</span>}
          </button>

          <button
            type="button"
            role="tab"
            id="aba-historico"
            aria-selected={aba === "historico"}
            aria-controls="painel-historico"
            className="compras-tab"
            onClick={() => trocarAba("historico")}
          >
            <Receipt size={16} />
            Histórico
          </button>
        </div>

        {erro && (
          <p className="dashboard-erro" role="alert">
            {erro}
          </p>
        )}

        {aviso && (
          <p className="compras-aviso" role="status">
            <Check size={18} />
            {aviso}
          </p>
        )}

        {aba === "carrinho" && (
          <section id="painel-carrinho" role="tabpanel" aria-labelledby="aba-carrinho">
            {itens.length === 0 ? (
              <div className="compras-vazio">
                <ShoppingBag size={32} />
                <h2>Seu carrinho está vazio</h2>
                <p>Os produtos que você adicionar aparecem aqui, prontos para finalizar.</p>
              </div>
            ) : (
              <div className="compras-carrinho">
                <ul className="compras-itens">
                  {itens.map((item) => {
                    const produto = item.produto;
                    const problema = problemaDoItem(item);
                    const nome = produto ? produto.nome : "Produto indisponível";

                    return (
                      <li key={item.id} className="compra-item">
                        <div className="compra-item-icone">
                          <Package size={22} />
                        </div>

                        <div className="compra-item-info">
                          <strong>{nome}</strong>

                          {produto && (
                            <>
                              <span className="compra-item-desc">{produto.descricao}</span>
                              <span className="compra-item-preco">
                                {moeda.format(produto.preco)} cada
                              </span>
                            </>
                          )}

                          {problema && <span className="compra-item-alerta">{problema}</span>}
                        </div>

                        <div className="compra-qtd" role="group" aria-label={`Quantidade de ${nome}`}>
                          <button
                            type="button"
                            aria-label="Diminuir quantidade"
                            disabled={ocupado || item.quantidade <= 1}
                            onClick={() => alterarQuantidade(item, item.quantidade - 1)}
                          >
                            <Minus size={16} />
                          </button>

                          <span aria-live="polite">{item.quantidade}</span>

                          <button
                            type="button"
                            aria-label="Aumentar quantidade"
                            disabled={
                              ocupado ||
                              (produto ? item.quantidade >= produto.estoque : false)
                            }
                            onClick={() => alterarQuantidade(item, item.quantidade + 1)}
                          >
                            <Plus size={16} />
                          </button>
                        </div>

                        <strong className="compra-item-subtotal">
                          {produto ? moeda.format(produto.preco * item.quantidade) : "—"}
                        </strong>

                        <button
                          type="button"
                          className="compra-remover"
                          aria-label={`Remover ${nome} do carrinho`}
                          disabled={ocupado}
                          onClick={() => removerItem(item)}
                        >
                          <Trash2 size={18} />
                        </button>
                      </li>
                    );
                  })}
                </ul>

                <aside className="compras-resumo" aria-label="Resumo da compra">
                  <h2>Resumo</h2>

                  <dl>
                    <div>
                      <dt>Itens</dt>
                      <dd>{totalUnidades}</dd>
                    </div>

                    <div className="compras-resumo-total">
                      <dt>Total</dt>
                      <dd>{moeda.format(total)}</dd>
                    </div>
                  </dl>

                  <button
                    type="button"
                    className="compras-finalizar"
                    disabled={ocupado || !podeFinalizar}
                    onClick={finalizarCompra}
                  >
                    Finalizar compra
                  </button>

                  {comProblema.length > 0 && (
                    <p className="compras-resumo-nota">
                      Resolva os avisos nos itens para finalizar.
                    </p>
                  )}
                </aside>
              </div>
            )}
          </section>
        )}

        {aba === "historico" && (
          <section id="painel-historico" role="tabpanel" aria-labelledby="aba-historico">
            {pedidos.length === 0 ? (
              <div className="compras-vazio">
                <Receipt size={32} />
                <h2>Nenhuma compra ainda</h2>
                <p>Quando você finalizar um carrinho, a compra fica registrada aqui.</p>
              </div>
            ) : (
              <>
                <ul className="pedidos">
                  {pedidos.map((pedido) => {
                    const aberto = expandido === pedido.id;
                    const unidades = pedido.itens.reduce(
                      (soma, item) => soma + item.quantidade,
                      0
                    );

                    return (
                      <li key={pedido.id} className="pedido">
                        <button
                          type="button"
                          className="pedido-topo"
                          aria-expanded={aberto}
                          aria-controls={`pedido-${pedido.id}`}
                          onClick={() => setExpandido(aberto ? null : pedido.id)}
                        >
                          <span className="pedido-id">Compra #{pedido.id}</span>
                          <span className="pedido-data">
                            {formatarDataHora(pedido.data_compra)}
                          </span>
                          <span className="pedido-qtd">{rotuloItens(unidades)}</span>
                          <strong className="pedido-total">
                            {moeda.format(pedido.valor_total)}
                          </strong>
                          <ChevronDown
                            size={18}
                            className={`pedido-seta ${aberto ? "aberto" : ""}`}
                          />
                        </button>

                        {aberto && (
                          <ul id={`pedido-${pedido.id}`} className="pedido-itens">
                            {pedido.itens.map((item) => (
                              <li key={item.id}>
                                <span className="pedido-item-nome">{item.nome_produto}</span>
                                <span className="pedido-item-calculo">
                                  {item.quantidade} × {moeda.format(item.preco_unitario)}
                                </span>
                                <strong>
                                  {moeda.format(item.preco_unitario * item.quantidade)}
                                </strong>
                              </li>
                            ))}
                          </ul>
                        )}
                      </li>
                    );
                  })}
                </ul>

                {temMais && (
                  <button
                    type="button"
                    className="compras-mais"
                    disabled={ocupado}
                    onClick={carregarMais}
                  >
                    Ver compras anteriores
                  </button>
                )}
              </>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default Compras;
