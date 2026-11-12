import { useEffect, useMemo, useState } from "react";
import { Syringe } from "lucide-react";

import Modal from "../Modal/Modal";
import DoseBadge from "../DoseBadge/DoseBadge";
import api from "../../services/api";
import tratarErro from "../../services/tratarErro";
import { formatarData, idsDosesVigentes, situacaoDaDose } from "../../utils/vacinas";
import "./AnimalVacinasModal.css";

// Carteira de vacinação de um animal do cliente logado.
function AnimalVacinasModal({ animal, onClose }) {
  const [aplicacoes, setAplicacoes] = useState([]);
  const [carregando, setCarregando] = useState(true);
  const [erro, setErro] = useState("");

  useEffect(() => {
    let ignorar = false;

    const requisicao = equipe
      ? Promise.all([
          api.get(`/aplicacoes-vacina/animal/${animal.id}`),
          api.get("/vacinas/"),
        ]).then(([resAplicacoes, resVacinas]) => {
          const porId = Object.fromEntries(
            (resVacinas.data || []).map((v) => [v.id, v])
          );

          return (resAplicacoes.data || []).map((a) => ({
            ...a,
            vacina_nome: porId[a.vacina_id]?.nome ?? `Vacina #${a.vacina_id}`,
            fabricante: porId[a.vacina_id]?.fabricante ?? "",
            veterinario_nome: null,
          }));
        })
      : api
          .get(`/aplicacoes-vacina/carteira/${animal.id}`)
          .then((res) => res.data || []);

    requisicao
      .then((dados) => {
        if (!ignorar) setAplicacoes(dados);
      })
      .catch((err) => {
        if (!ignorar) setErro(tratarErro(err).mensagem);
      })
      .finally(() => {
        if (!ignorar) setCarregando(false);
      });

    return () => {
      ignorar = true;
    };
  }, [animal.id, equipe]);

    const itens = useMemo(() => {
    const vigentes = idsDosesVigentes(aplicacoes);

    return aplicacoes.map((aplicacao) => ({
      ...aplicacao,
      situacao: situacaoDaDose(aplicacao, vigentes.has(aplicacao.id)),
    }));
  }, [aplicacoes]);

    const atrasadas = itens.filter((i) => i.situacao.valor === "atrasada").length;
    const aVencer = itens.filter((i) => i.situacao.valor === "vence-em-breve").length;

    return (
      <Modal
        titulo={`Vacinas de ${animal.nome}`}
        onClose={onClose}
        largura="620px"
      >
        {carregando && <p className="vacinas-modal-status">Carregando...</p>}

        {erro && <p className="vacinas-modal-status erro">{erro}</p>}

        {!carregando && !erro && itens.length === 0 && (
          <p className="vacinas-modal-status">
            Nenhuma vacina registrada para {animal.nome} ainda.
          </p>
        )}

        {!carregando && !erro && itens.length > 0 && (
          <>
            {(atrasadas > 0 || aVencer > 0) && (
              <div className="vacinas-modal-resumo">
                {atrasadas > 0 && (
                  <span className="resumo-atrasada">
                    {atrasadas} {atrasadas === 1 ? "reforço atrasado" : "reforços atrasados"}
                  </span>
                )}
                {aVencer > 0 && (
                  <span className="resumo-vencer">
                    {aVencer} {aVencer === 1 ? "reforço vence" : "reforços vencem"} em breve
                  </span>
                )}
              </div>
            )}

            <ul className="vacinas-modal-lista">
              {itens.map((item) => (
                <li key={item.id} className="vacinas-modal-item">
                  <div className="vacinas-modal-topo">
                    <div className="vacinas-modal-titulo">
                      <Syringe size={16} />
                      <strong>{item.vacina_nome}</strong>
                    </div>

                    <div className="vacinas-modal-dose">
                      <DoseBadge
                        situacao={item.situacao}
                        proximaDose={item.proxima_dose}
                      />
                    </div>
                  </div>

                  <p className="vacinas-modal-info">
                    Aplicada em {formatarData(item.data_aplicacao)}
                    {item.veterinario_nome && ` · Dr(a). ${item.veterinario_nome}`}
                    {item.lote && ` · Lote ${item.lote}`}
                  </p>

                  {item.observacoes && (
                    <p className="vacinas-modal-obs">{item.observacoes}</p>
                  )}
                </li>
              ))}
            </ul>
          </>
        )}
      </Modal>
    );
  }

export default AnimalVacinasModal;
