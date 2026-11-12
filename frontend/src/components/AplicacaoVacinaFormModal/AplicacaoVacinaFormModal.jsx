import { useState } from "react";

import Modal from "../Modal/Modal";
import api from "../../services/api";
import tratarErro from "../../services/tratarErro";

// Reaproveita .animal-form, .campo, .erro-campo, .erro-servidor, .form-acoes...
import "../AnimalFormModal/AnimalFormModal.css";
import "../VacinaFormModal/VacinaFormModal.css";

// Limites das colunas no banco (lote: 100, observações: 500).
const LOTE_MAX = 100;
const OBSERVACOES_MAX = 500;

// "2026-11-20T10:30:00" -> "2026-11-20" (formato do <input type="date">)
function isoParaInputData(iso) {
  return iso ? iso.slice(0, 10) : "";
}

// aplicacao: objeto existente (edição) ou null (nova aplicação).
// animais / vacinas: listas usadas nos selects e para mostrar os nomes.
function AplicacaoVacinaFormModal({
  aplicacao,
  animais,
  vacinas,
  onClose,
  onSalvo,
}) {
  const editando = Boolean(aplicacao);

  const [animalId, setAnimalId] = useState("");
  const [vacinaId, setVacinaId] = useState("");
  const [lote, setLote] = useState(aplicacao?.lote ?? "");
  const [observacoes, setObservacoes] = useState(aplicacao?.observacoes ?? "");
  const [proximaDose, setProximaDose] = useState(
    isoParaInputData(aplicacao?.proxima_dose)
  );

  const [erros, setErros] = useState({});
  const [erroServidor, setErroServidor] = useState("");
  const [salvando, setSalvando] = useState(false);

  const vacinaEscolhida = vacinas.find((v) => String(v.id) === vacinaId);

  const animalDaAplicacao = animais.find((a) => a.id === aplicacao?.animal_id);
  const vacinaDaAplicacao = vacinas.find((v) => v.id === aplicacao?.vacina_id);

  async function handleSubmit(e) {
    e.preventDefault();
    setErroServidor("");

    const errosValidacao = {};

    if (!editando) {
      if (!animalId) errosValidacao.animal = "Selecione o animal.";
      if (!vacinaId) errosValidacao.vacina = "Selecione a vacina.";
    }

    setErros(errosValidacao);

    if (Object.keys(errosValidacao).length > 0) {
      return;
    }

    setSalvando(true);

    try {
      if (editando) {
        const dados = {
          lote: lote.trim(),
          observacoes: observacoes.trim(),
        };

        // Só envia a data se foi alterada, para não perder o horário original.
        if (proximaDose && proximaDose !== isoParaInputData(aplicacao.proxima_dose)) {
          dados.proxima_dose = `${proximaDose}T00:00:00`;
        }

        await api.put(`/aplicacoes-vacina/${aplicacao.id}`, dados);
      } else {
        const dados = {
          animal_id: Number(animalId),
          vacina_id: Number(vacinaId),
        };

        if (lote.trim()) dados.lote = lote.trim();
        if (observacoes.trim()) dados.observacoes = observacoes.trim();

        // A próxima dose é calculada pela API (data de hoje + intervalo da vacina).
        await api.post("/aplicacoes-vacina/", dados);
      }

      onSalvo(editando);
    } catch (err) {
      setErroServidor(tratarErro(err).mensagem);
    } finally {
      setSalvando(false);
    }
  }

  return (
    <Modal
      titulo={editando ? "Editar aplicação" : "Aplicar vacina"}
      onClose={onClose}
    >
      <form onSubmit={handleSubmit} className="animal-form vacina-form" noValidate>
        {editando ? (
          <>
            <div className="campo">
              <label>Animal</label>
              <div className="campo-fixo">
                {animalDaAplicacao
                  ? `${animalDaAplicacao.nome} (${animalDaAplicacao.especie})`
                  : `Animal #${aplicacao.animal_id}`}
              </div>
            </div>

            <div className="campo">
              <label>Vacina</label>
              <div className="campo-fixo">
                {vacinaDaAplicacao?.nome ?? `Vacina #${aplicacao.vacina_id}`}
              </div>
            </div>
          </>
        ) : (
          <>
            <div className="campo">
              <label htmlFor="aplicacao-animal">Animal</label>
              <select
                id="aplicacao-animal"
                value={animalId}
                onChange={(e) => setAnimalId(e.target.value)}
              >
                <option value="">Selecione...</option>
                {animais.map((animal) => (
                  <option key={animal.id} value={animal.id}>
                    {animal.nome} ({animal.especie})
                  </option>
                ))}
              </select>
              {erros.animal && <span className="erro-campo">{erros.animal}</span>}
            </div>

            <div className="campo">
              <label htmlFor="aplicacao-vacina">Vacina</label>
              <select
                id="aplicacao-vacina"
                value={vacinaId}
                onChange={(e) => setVacinaId(e.target.value)}
              >
                <option value="">Selecione...</option>
                {vacinas.map((vacina) => (
                  <option key={vacina.id} value={vacina.id}>
                    {vacina.nome}
                  </option>
                ))}
              </select>
              {vacinaEscolhida && (
                <span className="campo-ajuda">
                  Próxima dose calculada automaticamente: daqui a{" "}
                  {vacinaEscolhida.intervalo_dias} dia(s). A data da aplicação
                  é a de hoje.
                </span>
              )}
              {erros.vacina && <span className="erro-campo">{erros.vacina}</span>}
            </div>
          </>
        )}

        <div className="campo">
          <label htmlFor="aplicacao-lote">Lote (opcional)</label>
          <input
            id="aplicacao-lote"
            value={lote}
            maxLength={LOTE_MAX}
            onChange={(e) => setLote(e.target.value)}
          />
        </div>

        {editando && (
          <div className="campo">
            <label htmlFor="aplicacao-proxima">Próxima dose</label>
            <input
              id="aplicacao-proxima"
              type="date"
              value={proximaDose}
              onChange={(e) => setProximaDose(e.target.value)}
            />
            <span className="campo-ajuda">
              Ajuste a data se o reforço for remarcado.
            </span>
          </div>
        )}

        <div className="campo">
          <label htmlFor="aplicacao-obs">Observações (opcional)</label>
          <textarea
            id="aplicacao-obs"
            rows={3}
            maxLength={OBSERVACOES_MAX}
            value={observacoes}
            onChange={(e) => setObservacoes(e.target.value)}
            placeholder="Reações, peso no dia, orientações ao tutor..."
          />
          <span className="contador-campo">
            {observacoes.length}/{OBSERVACOES_MAX}
          </span>
        </div>

        {erroServidor && <p className="erro-servidor">{erroServidor}</p>}

        <div className="form-acoes">
          <button
            type="button"
            className="btn-secundario"
            onClick={onClose}
            disabled={salvando}
          >
            Cancelar
          </button>

          <button type="submit" className="btn-primario" disabled={salvando}>
            {salvando
              ? "Salvando..."
              : editando
                ? "Salvar alterações"
                : "Registrar aplicação"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default AplicacaoVacinaFormModal;
