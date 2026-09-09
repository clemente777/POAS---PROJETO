import { useEffect, useRef, useState } from "react";
import { Search } from "lucide-react";

import Modal from "../Modal/Modal";
import api from "../../services/api";
import "./AnimalFormModal.css";

const ESPECIE_LIMITE = 100;

function validarCampos({ nome, especie, raca, idade, clienteId, ehEdicao, clienteFixo }) {
  const erros = {};

  if (!nome || nome.trim().length < 2) {
    erros.nome = "Informe pelo menos 2 caracteres.";
  }

  if (!especie || especie.trim().length < 2) {
    erros.especie = "Informe pelo menos 2 caracteres.";
  }

  if (!raca || raca.trim().length < 2) {
    erros.raca = "Informe pelo menos 2 caracteres.";
  }

  const idadeNum = Number(idade);

  if (idade === "" || Number.isNaN(idadeNum) || idadeNum < 0 || idadeNum > 100) {
    erros.idade = "Idade deve ser entre 0 e 100.";
  }

  if (!ehEdicao && !clienteFixo && !clienteId) {
    erros.cliente = "Selecione um tutor.";
  }

  return erros;
}

// clienteFixo: { id, nome } — quando informado (tela "Meus Animais" do
// Cliente), pula a busca de tutor e usa sempre o próprio cliente logado.
function AnimalFormModal({ animal, clienteFixo = null, onClose, onSalvo }) {
  const ehEdicao = Boolean(animal);

  const [nome, setNome] = useState(animal?.nome || "");
  const [especie, setEspecie] = useState(animal?.especie || "");
  const [raca, setRaca] = useState(animal?.raca || "");
  const [idade, setIdade] = useState(animal?.idade ?? "");

  const [clienteId, setClienteId] = useState(animal?.cliente_id || null);
  const [clienteNome, setClienteNome] = useState("");
  const [buscaCliente, setBuscaCliente] = useState("");
  const [resultadosCliente, setResultadosCliente] = useState([]);
  const [buscandoCliente, setBuscandoCliente] = useState(false);
  const [listaClienteAberta, setListaClienteAberta] = useState(false);

  const [erros, setErros] = useState({});
  const [erroServidor, setErroServidor] = useState("");
  const [salvando, setSalvando] = useState(false);

  const debounceRef = useRef(null);

  // Em edição, busca o nome do tutor atual só pra exibir (não é editável)
  useEffect(() => {
    if (ehEdicao && animal?.cliente_id) {
      api
        .get(`/clientes/${animal.cliente_id}`)
        .then((res) => setClienteNome(res.data?.nome || ""))
        .catch(() => setClienteNome(""));
    }
  }, [ehEdicao, animal]);

  // Busca com debounce enquanto o usuário digita o tutor (só na criação)
  useEffect(() => {
    if (ehEdicao) return;

    if (debounceRef.current) clearTimeout(debounceRef.current);

    if (!buscaCliente || buscaCliente.trim().length < 2) {
      setResultadosCliente([]);
      return;
    }

    debounceRef.current = setTimeout(async () => {
      setBuscandoCliente(true);
      try {
        const res = await api.get("/clientes/", {
          params: { nome: buscaCliente, limit: 8 },
        });
        setResultadosCliente(res.data || []);
      } catch {
        setResultadosCliente([]);
      } finally {
        setBuscandoCliente(false);
      }
    }, 400);

    return () => clearTimeout(debounceRef.current);
  }, [buscaCliente, ehEdicao]);

  function selecionarCliente(cliente) {
    setClienteId(cliente.id);
    setClienteNome(cliente.nome);
    setBuscaCliente("");
    setResultadosCliente([]);
    setListaClienteAberta(false);
    setErros((prev) => ({ ...prev, cliente: undefined }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setErroServidor("");

    const errosValidacao = validarCampos({
      nome,
      especie,
      raca,
      idade,
      clienteId,
      ehEdicao,
      clienteFixo,
    });

    setErros(errosValidacao);

    if (Object.keys(errosValidacao).length > 0) {
      return;
    }

    setSalvando(true);

    try {
      if (ehEdicao) {
        await api.put(`/animais/${animal.id}`, {
          nome,
          especie,
          raca,
          idade: Number(idade),
        });
      } else {
        await api.post("/animais/", {
          nome,
          especie,
          raca,
          idade: Number(idade),
          cliente_id: clienteFixo ? clienteFixo.id : clienteId,
        });
      }

      onSalvo();
    } catch (err) {
      setErroServidor(
        err?.response?.data?.detail || "Erro ao salvar o animal. Tente novamente."
      );
    } finally {
      setSalvando(false);
    }
  }

  return (
    <Modal titulo={ehEdicao ? "Editar animal" : "Novo animal"} onClose={onClose}>
      <form onSubmit={handleSubmit} className="animal-form" noValidate>
        <div className="campo">
          <label>Nome</label>
          <input
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            maxLength={100}
            placeholder="Ex: Rex"
          />
          {erros.nome && <span className="erro-campo">{erros.nome}</span>}
        </div>

        <div className="linha-dupla">
          <div className="campo">
            <label>Espécie</label>
            <input
              value={especie}
              onChange={(e) => setEspecie(e.target.value)}
              maxLength={ESPECIE_LIMITE}
              placeholder="Ex: Cachorro"
            />
            {erros.especie && <span className="erro-campo">{erros.especie}</span>}
          </div>

          <div className="campo">
            <label>Raça</label>
            <input
              value={raca}
              onChange={(e) => setRaca(e.target.value)}
              maxLength={100}
              placeholder="Ex: Labrador"
            />
            {erros.raca && <span className="erro-campo">{erros.raca}</span>}
          </div>
        </div>

        <div className="campo">
          <label>Idade</label>
          <input
            type="number"
            min={0}
            max={100}
            value={idade}
            onChange={(e) => setIdade(e.target.value)}
            placeholder="Anos"
          />
          {erros.idade && <span className="erro-campo">{erros.idade}</span>}
        </div>

        {ehEdicao ? (
          <div className="campo">
            <label>Tutor</label>
            <div className="tutor-readonly">{clienteNome || "Carregando..."}</div>
          </div>
        ) : clienteFixo ? (
          <div className="campo">
            <label>Tutor</label>
            <div className="tutor-readonly">{clienteFixo.nome} (você)</div>
          </div>
        ) : (
          <div className="campo campo-cliente">
            <label>Tutor</label>

            {clienteId ? (
              <div className="cliente-selecionado">
                <span>{clienteNome}</span>
                <button
                  type="button"
                  onClick={() => {
                    setClienteId(null);
                    setClienteNome("");
                  }}
                >
                  Trocar
                </button>
              </div>
            ) : (
              <div className="cliente-busca-wrapper">
                <Search size={16} className="icone-busca" />
                <input
                  value={buscaCliente}
                  onChange={(e) => {
                    setBuscaCliente(e.target.value);
                    setListaClienteAberta(true);
                  }}
                  onFocus={() => setListaClienteAberta(true)}
                  placeholder="Buscar tutor pelo nome..."
                />

                {listaClienteAberta && buscaCliente.trim().length >= 2 && (
                  <div className="cliente-resultados">
                    {buscandoCliente && (
                      <div className="cliente-resultado-vazio">Buscando...</div>
                    )}

                    {!buscandoCliente && resultadosCliente.length === 0 && (
                      <div className="cliente-resultado-vazio">
                        Nenhum tutor encontrado.
                      </div>
                    )}

                    {resultadosCliente.map((cliente) => (
                      <button
                        type="button"
                        key={cliente.id}
                        className="cliente-resultado-item"
                        onClick={() => selecionarCliente(cliente)}
                      >
                        <strong>{cliente.nome}</strong>
                        <span>{cliente.email}</span>
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}

            {erros.cliente && <span className="erro-campo">{erros.cliente}</span>}
          </div>
        )}

        {erroServidor && <p className="erro-servidor">{erroServidor}</p>}

        <div className="form-acoes">
          <button type="button" className="btn-secundario" onClick={onClose} disabled={salvando}>
            Cancelar
          </button>

          <button type="submit" className="btn-primario" disabled={salvando}>
            {salvando ? "Salvando..." : "Salvar"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default AnimalFormModal;
