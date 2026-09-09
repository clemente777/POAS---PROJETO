import { useCallback, useEffect, useState } from "react";
import {
  Plus,
  Search,
  Pencil,
  Trash2,
  History,
  ChevronLeft,
  ChevronRight,
  ArrowUpDown,
} from "lucide-react";

import api from "../../services/api";
import { useAuth } from "../../contexts/AuthContext";

import Sidebar from "../../components/Sidebar/Sidebar";
import AnimalFormModal from "../../components/AnimalFormModal/AnimalFormModal";
import AnimalHistoricoModal from "../../components/AnimalHistoricoModal/AnimalHistoricoModal";
import ConfirmDialog from "../../components/ConfirmDialog/ConfirmDialog";

import "./Animais.css";

const LIMITE_POR_PAGINA = 10;

function Animais() {
  const { usuario } = useAuth();

  const [sidebarAberto, setSidebarAberto] = useState(true);

  const [animais, setAnimais] = useState([]);
  const [clientesMap, setClientesMap] = useState({});

  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  const [busca, setBusca] = useState("");
  const [buscaAplicada, setBuscaAplicada] = useState("");
  const [ordem, setOrdem] = useState("asc");
  const [pagina, setPagina] = useState(1);

  const [modalForm, setModalForm] = useState(null); // null | "novo" | animal (edição)
  const [modalHistoricoId, setModalHistoricoId] = useState(null);
  const [animalParaExcluir, setAnimalParaExcluir] = useState(null);
  const [excluindo, setExcluindo] = useState(false);
  const [erroExclusao, setErroExclusao] = useState("");

  const carregarAnimais = useCallback(async () => {
    setCarregando(true);
    setErro("");

    try {
      const res = await api.get("/animais/", {
        params: {
          pagina,
          limite: LIMITE_POR_PAGINA,
          nome: buscaAplicada || undefined,
          ordem,
        },
      });

      setAnimais(res.data || []);
    } catch (err) {
      setErro(
        err?.response?.data?.detail || "Não foi possível carregar os animais."
      );
    } finally {
      setCarregando(false);
    }
  }, [pagina, buscaAplicada, ordem]);

  useEffect(() => {
    carregarAnimais();
  }, [carregarAnimais]);

  // Carrega um mapa id -> nome de clientes pra exibir o tutor na tabela
  // (a resposta de /animais/ só traz cliente_id).
  useEffect(() => {
    api
      .get("/clientes/", { params: { limit: 200 } })
      .then((res) => {
        const mapa = {};
        (res.data || []).forEach((c) => {
          mapa[c.id] = c.nome;
        });
        setClientesMap(mapa);
      })
      .catch(() => setClientesMap({}));
  }, []);

  function handleBuscar(e) {
    e.preventDefault();
    setPagina(1);
    setBuscaAplicada(busca);
  }

  function alternarOrdem() {
    setOrdem((atual) => (atual === "asc" ? "desc" : "asc"));
    setPagina(1);
  }

  function abrirNovo() {
    setModalForm("novo");
  }

  function abrirEdicao(animal) {
    setModalForm(animal);
  }

  function fecharForm() {
    setModalForm(null);
  }

  function salvouForm() {
    setModalForm(null);
    carregarAnimais();
  }

  async function confirmarExclusao() {
    setExcluindo(true);
    setErroExclusao("");

    try {
      await api.delete(`/animais/${animalParaExcluir.id}`);
      setAnimalParaExcluir(null);
      carregarAnimais();
    } catch (err) {
      setErroExclusao(
        err?.response?.data?.detail || "Não foi possível excluir este animal."
      );
    } finally {
      setExcluindo(false);
    }
  }

  return (
    <div className="animais-page">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`animais-content ${sidebarAberto ? "aberto" : "fechado"}`}>
        <header className="animais-header">
          <div>
            <h1>Animais</h1>
            <p>Gerencie os animais cadastrados no sistema</p>
          </div>

          <button className="btn-novo" onClick={abrirNovo}>
            <Plus size={18} /> Novo animal
          </button>
        </header>

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
            Nome ({ordem === "asc" ? "A-Z" : "Z-A"})
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
                <th>Tutor</th>
                <th className="col-acoes">Ações</th>
              </tr>
            </thead>

            <tbody>
              {carregando && (
                <tr>
                  <td colSpan={6} className="tabela-status">
                    Carregando...
                  </td>
                </tr>
              )}

              {!carregando && animais.length === 0 && (
                <tr>
                  <td colSpan={6} className="tabela-status">
                    Nenhum animal encontrado.
                  </td>
                </tr>
              )}

              {!carregando &&
                animais.map((animal) => (
                  <tr key={animal.id}>
                    <td className="col-nome">{animal.nome}</td>
                    <td>{animal.especie}</td>
                    <td>{animal.raca}</td>
                    <td>{animal.idade} anos</td>
                    <td>{clientesMap[animal.cliente_id] || "-"}</td>
                    <td className="col-acoes">
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
                        onClick={() => abrirEdicao(animal)}
                      >
                        <Pencil size={16} />
                      </button>

                      <button
                        className="btn-icone btn-icone-perigo"
                        title="Excluir"
                        onClick={() => {
                          setAnimalParaExcluir(animal);
                          setErroExclusao("");
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
            <ChevronLeft size={16} /> Anterior
          </button>

          <span>Página {pagina}</span>

          <button
            onClick={() => setPagina((p) => p + 1)}
            disabled={carregando || animais.length < LIMITE_POR_PAGINA}
          >
            Próxima <ChevronRight size={16} />
          </button>
        </div>
      </main>

      {modalForm && (
        <AnimalFormModal
          animal={modalForm === "novo" ? null : modalForm}
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
  );
}

export default Animais;
