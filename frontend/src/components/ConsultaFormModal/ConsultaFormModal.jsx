import { useState } from "react";
import { Link } from "react-router-dom";

import Modal from "../Modal/Modal";
import api from "../../services/api";
import tratarErro from "../../services/tratarErro";

// Reaproveita .animal-form, .campo, .erro-campo, .erro-servidor, .form-acoes...
import "../AnimalFormModal/AnimalFormModal.css";
import "./ConsultaFormModal.css";

const DESCRICAO_MIN = 5;
const DESCRICAO_MAX = 255;

// Data/hora atual no formato do <input type="datetime-local">
// (YYYY-MM-DDTHH:mm), em horário local.
function agoraParaInput() {
  const agora = new Date();
  agora.setMinutes(agora.getMinutes() - agora.getTimezoneOffset());
  return agora.toISOString().slice(0, 16);
}

function validarCampos({ animalId, dataHora, descricao }) {
  const erros = {};

  if (!animalId) {
    erros.animal = "Selecione o animal.";
  }

  if (!dataHora) {
    erros.data = "Informe a data e o horário.";
  } else if (new Date(dataHora) <= new Date()) {
    erros.data = "Escolha um horário no futuro.";
  }

  if (descricao.trim().length < DESCRICAO_MIN) {
    erros.descricao = `Descreva o motivo (mínimo ${DESCRICAO_MIN} caracteres).`;
  }

  return erros;
}

// animais: lista dos animais do cliente logado (vem da página).
function ConsultaFormModal({ animais, onClose, onSalvo }) {
  // Se o cliente só tem um animal, já deixa selecionado.
  const [animalId, setAnimalId] = useState(
    animais.length === 1 ? String(animais[0].id) : ""
  );
  const [dataHora, setDataHora] = useState("");
  const [descricao, setDescricao] = useState("");

  const [minimo] = useState(agoraParaInput);

  const [erros, setErros] = useState({});
  const [erroServidor, setErroServidor] = useState("");
  const [salvando, setSalvando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErroServidor("");

    const errosValidacao = validarCampos({ animalId, dataHora, descricao });
    setErros(errosValidacao);

    if (Object.keys(errosValidacao).length > 0) {
      return;
    }

    setSalvando(true);

    try {
      await api.post("/agendamentos/", {
        animal_id: Number(animalId),
        // "2026-10-20T14:30" (sem fuso), igual ao que a API guarda e devolve
        data_agendamento: dataHora,
        descricao: descricao.trim(),
      });

      onSalvo();
    } catch (err) {
      setErroServidor(tratarErro(err).mensagem);
    } finally {
      setSalvando(false);
    }
  }

  return (
    <Modal titulo="Agendar consulta" onClose={onClose}>
      {animais.length === 0 ? (
        <div className="consulta-sem-animal">
          <p>Você precisa cadastrar um animal antes de agendar uma consulta.</p>
          <Link to="/meus-animais" className="btn-primario">
            Ir para Meus Animais
          </Link>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="animal-form consulta-form" noValidate>
          <div className="campo">
            <label htmlFor="consulta-animal">Animal</label>
            <select
              id="consulta-animal"
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
            <label htmlFor="consulta-data">Data e horário</label>
            <input
              id="consulta-data"
              type="datetime-local"
              min={minimo}
              value={dataHora}
              onChange={(e) => setDataHora(e.target.value)}
            />
            {erros.data && <span className="erro-campo">{erros.data}</span>}
          </div>

          <div className="campo">
            <label htmlFor="consulta-descricao">Motivo da consulta</label>
            <textarea
              id="consulta-descricao"
              rows={3}
              maxLength={DESCRICAO_MAX}
              value={descricao}
              onChange={(e) => setDescricao(e.target.value)}
              placeholder="Ex: Check-up anual, vacina, coceira na pele..."
            />
            <span className="contador-campo">
              {descricao.length}/{DESCRICAO_MAX}
            </span>
            {erros.descricao && <span className="erro-campo">{erros.descricao}</span>}
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
              {salvando ? "Agendando..." : "Agendar"}
            </button>
          </div>
        </form>
      )}
    </Modal>
  );
}

export default ConsultaFormModal;