import { useState } from "react";

import Modal from "../Modal/Modal";
import api from "../../services/api";
import tratarErro from "../../services/tratarErro";

// Reaproveita .animal-form, .campo, .erro-campo, .erro-servidor, .form-acoes...
import "../AnimalFormModal/AnimalFormModal.css";
// ...e o estilo de select/textarea e do contador de caracteres.
import "../ConsultaFormModal/ConsultaFormModal.css";

const DIAGNOSTICO_MAX = 500;
const OBSERVACOES_MAX = 1000;

// Data/hora atual no formato do <input type="datetime-local">
// (YYYY-MM-DDTHH:mm), em horário local.
function agoraParaInput() {
  const agora = new Date();
  agora.setMinutes(agora.getMinutes() - agora.getTimezoneOffset());
  return agora.toISOString().slice(0, 16);
}

function validarCampos({ animalId, dataHora, diagnostico, observacoes }, editando) {
  const erros = {};

  if (!editando) {
    if (!animalId) {
      erros.animal = "Selecione o animal.";
    }

    if (!dataHora) {
      erros.data = "Informe a data e o horário.";
    } else if (new Date(dataHora) > new Date()) {
      erros.data = "A data do atendimento não pode ser futura.";
    }
  }

  if (!diagnostico.trim()) {
    erros.diagnostico = "Informe o diagnóstico.";
  }

  if (observacoes.length > OBSERVACOES_MAX) {
    erros.observacoes = `Máximo de ${OBSERVACOES_MAX} caracteres.`;
  }

  return erros;
}

// Cria um atendimento ou, se receber `atendimento`, edita o diagnóstico
// e as observações dele (data, animal e veterinário não mudam depois de
// registrados: a API bloqueia a alteração de atendimentos finalizados).
//
// animais:           lista de animais para o select
// animalIdInicial:   pré-seleciona (e trava) o animal, ex.: vindo de um agendamento
// usuarioId:         id do veterinário que está registrando
function AtendimentoFormModal({
  animais,
  atendimento = null,
  animalIdInicial = null,
  usuarioId,
  onClose,
  onSalvo,
}) {
  const editando = Boolean(atendimento);
  const animalTravado = editando || animalIdInicial !== null;

  const [animalId, setAnimalId] = useState(
    atendimento
      ? String(atendimento.animal_id)
      : animalIdInicial !== null
        ? String(animalIdInicial)
        : ""
  );
  const [dataHora, setDataHora] = useState(agoraParaInput);
  const [diagnostico, setDiagnostico] = useState(atendimento?.diagnostico ?? "");
  const [observacoes, setObservacoes] = useState(atendimento?.observacoes ?? "");

  const [maximo] = useState(agoraParaInput);

  const [erros, setErros] = useState({});
  const [erroServidor, setErroServidor] = useState("");
  const [salvando, setSalvando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErroServidor("");

    const errosValidacao = validarCampos(
      { animalId, dataHora, diagnostico, observacoes },
      editando
    );
    setErros(errosValidacao);

    if (Object.keys(errosValidacao).length > 0) {
      return;
    }

    setSalvando(true);

    // A API rejeita observações só com espaços; vazio vira "sem observações".
    const obs = observacoes.trim() || null;

    try {
      if (editando) {
        await api.put(`/atendimentos/${atendimento.id}`, {
          diagnostico: diagnostico.trim(),
          observacoes: obs,
        });
      } else {
        await api.post("/atendimentos/", {
          animal_id: Number(animalId),
          usuario_id: usuarioId,
          diagnostico: diagnostico.trim(),
          observacoes: obs,
          // "2026-10-20T14:30" (sem fuso), igual ao que a API guarda e devolve
          data_atendimento: dataHora,
        });
      }

      onSalvo();
    } catch (err) {
      setErroServidor(tratarErro(err).mensagem);
    } finally {
      setSalvando(false);
    }
  }

  return (
    <Modal
      titulo={editando ? "Editar atendimento" : "Registrar atendimento"}
      onClose={onClose}
      largura="560px"
    >
      <form onSubmit={handleSubmit} className="animal-form consulta-form" noValidate>
        <div className="campo">
          <label htmlFor="atendimento-animal">Animal</label>
          <select
            id="atendimento-animal"
            value={animalId}
            disabled={animalTravado}
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

        {!editando && (
          <div className="campo">
            <label htmlFor="atendimento-data">Data e horário do atendimento</label>
            <input
              id="atendimento-data"
              type="datetime-local"
              max={maximo}
              value={dataHora}
              onChange={(e) => setDataHora(e.target.value)}
            />
            {erros.data && <span className="erro-campo">{erros.data}</span>}
          </div>
        )}

        <div className="campo">
          <label htmlFor="atendimento-diagnostico">Diagnóstico</label>
          <textarea
            id="atendimento-diagnostico"
            rows={3}
            maxLength={DIAGNOSTICO_MAX}
            value={diagnostico}
            onChange={(e) => setDiagnostico(e.target.value)}
            placeholder="Ex: Otite leve no ouvido direito"
          />
          <span className="contador-campo">
            {diagnostico.length}/{DIAGNOSTICO_MAX}
          </span>
          {erros.diagnostico && <span className="erro-campo">{erros.diagnostico}</span>}
        </div>

        <div className="campo">
          <label htmlFor="atendimento-observacoes">Observações (opcional)</label>
          <textarea
            id="atendimento-observacoes"
            rows={3}
            maxLength={OBSERVACOES_MAX}
            value={observacoes}
            onChange={(e) => setObservacoes(e.target.value)}
            placeholder="Tratamento indicado, retorno, recomendações ao tutor..."
          />
          <span className="contador-campo">
            {observacoes.length}/{OBSERVACOES_MAX}
          </span>
          {erros.observacoes && <span className="erro-campo">{erros.observacoes}</span>}
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
            {salvando ? "Salvando..." : editando ? "Salvar" : "Registrar"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default AtendimentoFormModal;
