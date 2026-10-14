import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import {
  Plus,
  Search,
  CalendarX,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from "lucide-react";

import api from "../../services/api";
import tratarErro from "../../services/tratarErro";
import { useAuth } from "../../contexts/AuthContext";

import Sidebar from "../../components/Sidebar/Sidebar";
import ConsultaFormModal from "../../components/ConsultaFormModal/ConsultaFormModal";
import ConfirmDialog from "../../components/ConfirmDialog/ConfirmDialog";

// Layout base (sidebar, cabeçalho, tabela, paginação) é o mesmo de Animais.
import "../Animais/Animais.css";
import "./MinhasConsultas.css";

const LIMITE_POR_PAGINA = 10;

// Mesmos valores aceitos pela API (STATUS_VALIDOS no service de agendamentos).
const STATUS_OPCOES = ["Pendente", "Confirmado", "Finalizado", "Cancelado"];

// Só dá pra cancelar o que ainda não foi finalizado/cancelado.
const STATUS_CANCELAVEIS = ["Pendente", "Confirmado"];

// A API devolve a data sem fuso ("2026-10-20T14:30:00"); o navegador
// interpreta como horário local, que é o mesmo que o cliente digitou.
function formatarDataHora(iso) {
  const data = new Date(iso);

  if (Number.isNaN(data.getTime())) return "—";

  return data.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function MinhasConsultas() {
  const { usuario } = useAuth();

  const [sidebarAberto, setSidebarAberto] = useState(true);

  // Animais do cliente: usados no formulário e pra mostrar o nome na tabela
  // (a API de agendamentos só devolve o animal_id).
  const [animais, setAnimais] = useState([]);
  const [carregandoAnimais, setCarregandoAnimais] = useState(true);
  const [erroAnimais, setErroAnimais] = useState("");

  const [busca, setBusca] = useState("");
  const [buscaAplicada, setBuscaAplicada] = useState("");
  const [status, setStatus] = useState("");
  const [ordem, setOrdem] = useState("desc");
  const [pagina, setPagina] = useState(1);

  // Incrementar força a lista a ser buscada de novo (após agendar/cancelar).
  const [recarga, setRecarga] = useState(0);

  // Resultado da última busca, junto com a "chave" dos filtros que o gerou.
  // Se a chave atual for diferente da guardada, ainda estamos carregando.
  const [resultado, setResultado] = useState({
    chave: null,
    consultas: [],
    erro: "",
  });

  const [modalNovo, setModalNovo] = useState(false);
  const [aviso, setAviso] = useState("");

  const [consultaParaCancelar, setConsultaParaCancelar] = useState(null);
  const [cancelando, setCancelando] = useState(false);
  const [erroCancelamento, setErroCancelamento] = useState("");

  useEffect(() => {
    api
      .get("/animais/", { params: { pagina: 1, limite: 100 } })
      .then((res) => setAnimais(res.data || []))
      .catch((err) => setErroAnimais(tratarErro(err).mensagem))
      .finally(() => setCarregandoAnimais(false));
  }, []);

  const nomesAnimais = useMemo(
    () => Object.fromEntries(animais.map((animal) => [animal.id, animal.nome])),
    [animais]
  );

  const chaveBusca = `${pagina}|${status}|${buscaAplicada}|${ordem}|${recarga}`;

  useEffect(() => {
    // Se os filtros mudarem antes da resposta chegar, ignora a resposta antiga.
    let ignorar = false;

    api
      .get("/agendamentos/", {
        params: {
          skip: (pagina - 1) * LIMITE_POR_PAGINA,
          limit: LIMITE_POR_PAGINA,
          status: status || undefined,
          descricao: buscaAplicada || undefined,
          sort_by: "data_agendamento",
          order: ordem,
        },
      })
      .then((res) => {
        if (ignorar) return;
        setResultado({ chave: chaveBusca, consultas: res.data || [], erro: "" });
      })
      .catch((err) => {
        if (ignorar) return;
        setResultado({
          chave: chaveBusca,
          consultas: [],
          erro: tratarErro(err).mensagem,
        });
      });

    return () => {
      ignorar = true;
    };
  }, [chaveBusca, pagina, status, buscaAplicada, ordem]);

  const carregando = resultado.chave !== chaveBusca;
  const consultas = resultado.consultas;
  const erro = carregando ? "" : resultado.erro;

  function recarregar() {
    setRecarga((n) => n + 1);
  }

  function handleBuscar(e) {
    e.preventDefault();
    setPagina(1);
    setBuscaAplicada(busca.trim());
  }

  function handleStatus(e) {
    setStatus(e.target.value);
    setPagina(1);
  }

  function alternarOrdem() {
    setOrdem((atual) => (atual === "asc" ? "desc" : "asc"));
    setPagina(1);
  }

  function salvouConsulta() {
    setModalNovo(false);
    setAviso("Consulta agendada com sucesso!");
    recarregar();
  }

  function pedirCancelamento(consulta) {
    setConsultaParaCancelar(consulta);
    setErroCancelamento("");
  }

  async function confirmarCancelamento() {
    setCancelando(true);
    setErroCancelamento("");

    try {
      await api.post(`/agendamentos/${consultaParaCancelar.id}/cancelar`);

      setConsultaParaCancelar(null);
      setAviso("Consulta cancelada.");
      recarregar();
    } catch (err) {
      setErroCancelamento(tratarErro(err).mensagem);
    } finally {
      setCancelando(false);
    }
  }

  const temFiltro = Boolean(status || buscaAplicada);
  const semAnimais = !carregandoAnimais && !erroAnimais && animais.length === 0;

  return (
    <div className="animais-page consultas-page">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? "aberto" : "fechado"}`}>
        <header className="animais-header">
          <div>
            <h1>Minhas Consultas</h1>
            <p>Acompanhe e agende as consultas dos seus pets</p>
          </div>

          <button
            className="btn-novo"
            onClick={() => {
              setAviso("");
              setModalNovo(true);
            }}
            disabled={carregandoAnimais || animais.length === 0}
            title={
              semAnimais ? "Cadastre um animal para poder agendar" : erroAnimais || ""
            }
          >
            <Plus size={18} /> Agendar consulta
          </button>
        </header>

        {aviso && <p className="consultas-aviso consultas-aviso-sucesso">{aviso}</p>}

        {semAnimais && (
          <p className="consultas-aviso consultas-aviso-info">
            Para agendar uma consulta, primeiro cadastre um animal em{" "}
            <Link to="/meus-animais">Meus Animais</Link>.
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
            Data ({ordem === "desc" ? "mais recentes" : "mais antigas"})
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
                <th>Motivo</th>
                <th>Status</th>
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

              {!carregando && consultas.length === 0 && (
                <tr>
                  <td colSpan={5} className="tabela-status">
                    {temFiltro
                      ? "Nenhuma consulta encontrada com esses filtros."
                      : "Você ainda não tem consultas agendadas."}
                  </td>
                </tr>
              )}

              {!carregando &&
                consultas.map((consulta) => (
                  <tr key={consulta.id}>
                    <td className="col-data">
                      {formatarDataHora(consulta.data_agendamento)}
                    </td>
                    <td className="col-nome">
                      {nomesAnimais[consulta.animal_id] ||
                        `Animal #${consulta.animal_id}`}
                    </td>
                    <td className="col-descricao">{consulta.descricao}</td>
                    <td>
                      <span
                        className={`status-badge status-${consulta.status.toLowerCase()}`}
                      >
                        {consulta.status}
                      </span>
                    </td>
                    <td className="col-acoes">
                      {STATUS_CANCELAVEIS.includes(consulta.status) && (
                        <button
                          className="btn-icone btn-icone-perigo"
                          title="Cancelar consulta"
                          aria-label="Cancelar consulta"
                          onClick={() => pedirCancelamento(consulta)}
                        >
                          <CalendarX size={16} />
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
            disabled={carregando || consultas.length < LIMITE_POR_PAGINA}
          >
            Próxima <ChevronRight size={16} />
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
            nomesAnimais[consultaParaCancelar.animal_id] || "seu animal"
          }" marcada para ${formatarDataHora(
            consultaParaCancelar.data_agendamento
          )}?`}
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
  );
}

export default MinhasConsultas;