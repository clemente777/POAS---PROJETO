import { useEffect, useMemo, useState } from 'react'
import { Syringe } from 'lucide-react'

import Modal from '../Modal/Modal'
import DoseBadge from '../DoseBadge/DoseBadge'
import api from '../../services/api'
import tratarErro from '../../services/tratarErro'
import { formatarData, idsDosesVigentes, situacaoDaDose } from '../../utils/vacinas'
import './AnimalVacinasModal.css'

// Carteira de vacinação de um animal.
// - Cliente: rota própria, que só devolve animais dele.
// - Administrador/Veterinário: lista as aplicações do animal e cruza com o
//   catálogo para mostrar o nome da vacina.
function AnimalVacinasModal({ animal, perfil = 'Cliente', onClose }) {
  const ehEquipe = perfil === 'Administrador' || perfil === 'Veterinário'

  const [aplicacoes, setAplicacoes] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')

  useEffect(() => {
    // Se o modal fechar antes da resposta chegar, ignora a resposta.
    let ignorar = false

    const buscar = ehEquipe
      ? Promise.all([
          api.get(`/aplicacoes-vacina/animal/${animal.id}`),
          api.get('/vacinas/'),
        ]).then(([resAplicacoes, resVacinas]) => {
          const vacinas = Object.fromEntries(
            (resVacinas.data || []).map((vacina) => [vacina.id, vacina])
          )

          return (resAplicacoes.data || [])
            .map((aplicacao) => ({
              ...aplicacao,
              vacina_nome:
                vacinas[aplicacao.vacina_id]?.nome || `Vacina #${aplicacao.vacina_id}`,
              veterinario_nome: null,
            }))
            .sort((a, b) => new Date(b.data_aplicacao) - new Date(a.data_aplicacao))
        })
      : api
          .get(`/aplicacoes-vacina/carteira/${animal.id}`)
          .then((res) => res.data || [])

    buscar
      .then((lista) => {
        if (!ignorar) setAplicacoes(lista)
      })
      .catch((err) => {
        if (!ignorar) setErro(tratarErro(err).mensagem)
      })
      .finally(() => {
        if (!ignorar) setCarregando(false)
      })

    return () => {
      ignorar = true
    }
  }, [animal.id, ehEquipe])

  const itens = useMemo(() => {
    const vigentes = idsDosesVigentes(aplicacoes)

    return aplicacoes.map((aplicacao) => ({
      ...aplicacao,
      situacao: situacaoDaDose(aplicacao, vigentes.has(aplicacao.id)),
    }))
  }, [aplicacoes])

  const atrasadas = itens.filter((i) => i.situacao.valor === 'atrasada').length
  const aVencer = itens.filter((i) => i.situacao.valor === 'vence-em-breve').length

  return (
    <Modal titulo={`Vacinas de ${animal.nome}`} onClose={onClose} largura="620px">
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
                  {atrasadas}{' '}
                  {atrasadas === 1 ? 'reforço atrasado' : 'reforços atrasados'}
                </span>
              )}
              {aVencer > 0 && (
                <span className="resumo-vencer">
                  {aVencer} {aVencer === 1 ? 'reforço vence' : 'reforços vencem'} em
                  breve
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
  )
}

export default AnimalVacinasModal
