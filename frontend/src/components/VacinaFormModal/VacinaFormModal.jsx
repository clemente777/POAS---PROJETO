import { useState } from 'react'

import Modal from '../Modal/Modal'
import api from '../../services/api'
import tratarErro from '../../services/tratarErro'

// Reaproveita .animal-form, .campo, .erro-campo, .erro-servidor, .form-acoes...
import '../AnimalFormModal/AnimalFormModal.css'
import './VacinaFormModal.css'

// Mesmos limites do VacinaCreate no back-end.
const TEXTO_MIN = 2
const TEXTO_MAX = 100
const DESCRICAO_MAX = 300

function validarCampos({ nome, fabricante, doses, intervalo }) {
  const erros = {}

  if (nome.trim().length < TEXTO_MIN) {
    erros.nome = `Informe o nome da vacina (mínimo ${TEXTO_MIN} caracteres).`
  }

  if (fabricante.trim().length < TEXTO_MIN) {
    erros.fabricante = `Informe o fabricante (mínimo ${TEXTO_MIN} caracteres).`
  }

  if (!/^\d+$/.test(doses) || Number(doses) < 1) {
    erros.doses = 'Informe um número inteiro maior que zero.'
  }

  if (!/^\d+$/.test(intervalo) || Number(intervalo) < 1) {
    erros.intervalo = 'Informe um número inteiro maior que zero.'
  }

  return erros
}

// vacina: objeto existente (edição) ou null (cadastro).
function VacinaFormModal({ vacina, onClose, onSalvo }) {
  const editando = Boolean(vacina)

  const [nome, setNome] = useState(vacina?.nome ?? '')
  const [fabricante, setFabricante] = useState(vacina?.fabricante ?? '')
  const [doses, setDoses] = useState(vacina ? String(vacina.quantidade_doses) : '1')
  const [intervalo, setIntervalo] = useState(
    vacina ? String(vacina.intervalo_dias) : ''
  )
  const [descricao, setDescricao] = useState(vacina?.descricao ?? '')

  const [erros, setErros] = useState({})
  const [erroServidor, setErroServidor] = useState('')
  const [salvando, setSalvando] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setErroServidor('')

    const errosValidacao = validarCampos({
      nome,
      fabricante,
      doses,
      intervalo,
    })
    setErros(errosValidacao)

    if (Object.keys(errosValidacao).length > 0) {
      return
    }

    const dados = {
      nome: nome.trim(),
      fabricante: fabricante.trim(),
      quantidade_doses: Number(doses),
      intervalo_dias: Number(intervalo),
    }

    // No PUT, "" limpa a descrição; no POST, melhor omitir o campo vazio.
    if (editando) {
      dados.descricao = descricao.trim()
    } else if (descricao.trim()) {
      dados.descricao = descricao.trim()
    }

    setSalvando(true)

    try {
      if (editando) {
        await api.put(`/vacinas/${vacina.id}`, dados)
      } else {
        await api.post('/vacinas/', dados)
      }

      onSalvo(editando)
    } catch (err) {
      setErroServidor(tratarErro(err).mensagem)
    } finally {
      setSalvando(false)
    }
  }

  return (
    <Modal titulo={editando ? 'Editar vacina' : 'Nova vacina'} onClose={onClose}>
      <form onSubmit={handleSubmit} className="animal-form vacina-form" noValidate>
        <div className="campo">
          <label htmlFor="vacina-nome">Nome</label>
          <input
            id="vacina-nome"
            value={nome}
            maxLength={TEXTO_MAX}
            onChange={(e) => setNome(e.target.value)}
            placeholder="Ex: V10, Antirrábica, Tríplice felina"
          />
          {erros.nome && <span className="erro-campo">{erros.nome}</span>}
        </div>

        <div className="campo">
          <label htmlFor="vacina-fabricante">Fabricante</label>
          <input
            id="vacina-fabricante"
            value={fabricante}
            maxLength={TEXTO_MAX}
            onChange={(e) => setFabricante(e.target.value)}
          />
          {erros.fabricante && <span className="erro-campo">{erros.fabricante}</span>}
        </div>

        <div className="linha-dupla">
          <div className="campo">
            <label htmlFor="vacina-doses">Quantidade de doses</label>
            <input
              id="vacina-doses"
              type="number"
              min={1}
              step={1}
              inputMode="numeric"
              value={doses}
              onChange={(e) => setDoses(e.target.value)}
            />
            {erros.doses && <span className="erro-campo">{erros.doses}</span>}
          </div>

          <div className="campo">
            <label htmlFor="vacina-intervalo">Intervalo (dias)</label>
            <input
              id="vacina-intervalo"
              type="number"
              min={1}
              step={1}
              inputMode="numeric"
              value={intervalo}
              onChange={(e) => setIntervalo(e.target.value)}
              placeholder="Ex: 365"
            />
            {erros.intervalo && <span className="erro-campo">{erros.intervalo}</span>}
          </div>
        </div>

        <span className="campo-ajuda">
          O intervalo é usado para calcular a data da próxima dose quando a vacina é
          aplicada.
        </span>

        <div className="campo">
          <label htmlFor="vacina-descricao">Descrição (opcional)</label>
          <textarea
            id="vacina-descricao"
            rows={3}
            maxLength={DESCRICAO_MAX}
            value={descricao}
            onChange={(e) => setDescricao(e.target.value)}
            placeholder="Contra quais doenças protege, indicações..."
          />
          <span className="contador-campo">
            {descricao.length}/{DESCRICAO_MAX}
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
            {salvando ? 'Salvando...' : editando ? 'Salvar alterações' : 'Cadastrar'}
          </button>
        </div>
      </form>
    </Modal>
  )
}

export default VacinaFormModal
