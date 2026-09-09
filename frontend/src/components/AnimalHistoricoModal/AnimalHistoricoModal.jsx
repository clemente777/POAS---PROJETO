import { useEffect, useState } from "react";
import { Stethoscope, PawPrint, User } from "lucide-react";

import Modal from "../Modal/Modal";
import api from "../../services/api";
import "./AnimalHistoricoModal.css";

function formatarData(isoString) {
  if (!isoString) return "-";

  return new Date(isoString).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function AnimalHistoricoModal({ animalId, onClose }) {
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    api
      .get(`/animais/${animalId}/historico`)
      .then((res) => setDados(res.data))
      .catch(() => setErro("Não foi possível carregar o histórico."))
      .finally(() => setCarregando(false));
  }, [animalId]);

  return (
    <Modal titulo="Histórico do animal" onClose={onClose} largura="620px">
      {carregando && <p className="historico-status">Carregando...</p>}

      {erro && <p className="historico-status erro">{erro}</p>}

      {dados && (
        <>
          <div className="historico-resumo">
            <div className="historico-resumo-item">
              <PawPrint size={18} />
              <div>
                <strong>{dados.animal.nome}</strong>
                <span>
                  {dados.animal.especie} · {dados.animal.raca} · {dados.animal.idade} anos
                </span>
              </div>
            </div>

            <div className="historico-resumo-item">
              <User size={18} />
              <div>
                <strong>{dados.cliente.nome}</strong>
                <span>
                  {dados.cliente.telefone} · {dados.cliente.email}
                </span>
              </div>
            </div>
          </div>

          <h3 className="historico-titulo">
            <Stethoscope size={16} /> Atendimentos
          </h3>

          {dados.historico.length === 0 ? (
            <p className="historico-vazio">Nenhum atendimento registrado ainda.</p>
          ) : (
            <ul className="historico-lista">
              {dados.historico.map((item, index) => (
                <li key={index} className="historico-item">
                  <div className="historico-item-topo">
                    <span className="historico-data">{formatarData(item.data)}</span>
                    {item.veterinario && (
                      <span className="historico-vet">Dr(a). {item.veterinario}</span>
                    )}
                  </div>
                  <p className="historico-diagnostico">{item.diagnostico}</p>
                  {item.observacoes && (
                    <p className="historico-observacoes">{item.observacoes}</p>
                  )}
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </Modal>
  );
}

export default AnimalHistoricoModal;
