
import { useState } from "react";

import Modal from "../Modal/Modal";
import api from "../../services/api";
import "./AnimalFormModal.css";

const ESPECIE_LIMITE = 100;

function validarCampos({ nome, especie, raca, idade }) {
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

  return erros;
}

function AnimalFormModal({ animal, clienteFixo = null, onClose, onSalvo }) {
  const ehEdicao = Boolean(animal);

  const [nome, setNome] = useState(animal?.nome || "");
  const [especie, setEspecie] = useState(animal?.especie || "");
  const [raca, setRaca] = useState(animal?.raca || "");
  const [idade, setIdade] = useState(animal?.idade ?? "");

  const [erros, setErros] = useState({});
  const [erroServidor, setErroServidor] = useState("");
  const [salvando, setSalvando] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setErroServidor("");

    const errosValidacao = validarCampos({
      nome,
      especie,
      raca,
      idade,
    });

    setErros(errosValidacao);

    if (Object.keys(errosValidacao).length > 0) {
      return;
    }

    if (!ehEdicao && !clienteFixo?.id) {
      setErroServidor(
        "Não foi possível identificar o tutor. Entre novamente na sua conta e tente de novo."
      );
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
          cliente_id: clienteFixo.id,
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
            {salvando ? "Salvando..." : "Salvar"}
          </button>
        </div>
      </form>
    </Modal>
  );
}

export default AnimalFormModal;
