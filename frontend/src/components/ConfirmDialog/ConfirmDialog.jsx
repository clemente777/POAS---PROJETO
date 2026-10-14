import Modal from "../Modal/Modal";
import "./ConfirmDialog.css";

function ConfirmDialog({
  titulo = "Confirmar ação",
  mensagem,
  confirmando = false,
  erro = "",
  textoConfirmar = "Confirmar",
  textoConfirmando = "Excluindo...",
  textoCancelar = "Cancelar",
  onConfirmar,
  onCancelar,
}) {
  return (
    <Modal titulo={titulo} onClose={onCancelar} largura="420px">
      <p className="confirm-mensagem">{mensagem}</p>

      {erro && <p className="confirm-erro">{erro}</p>}

      <div className="confirm-acoes">
        <button className="btn-secundario" onClick={onCancelar} disabled={confirmando}>
          {textoCancelar}
        </button>

        <button className="btn-perigo" onClick={onConfirmar} disabled={confirmando}>
          {confirmando ? textoConfirmando : textoConfirmar}
        </button>
      </div>
    </Modal>
  );
}

export default ConfirmDialog;