import { formatarData, textoDias } from '../../utils/vacinas'
import './DoseBadge.css'

// situacao: objeto devolvido por situacaoDaDose().
function DoseBadge({ situacao, proximaDose }) {
  return (
    <>
      <span className={`dose-badge dose-${situacao.valor}`}>{situacao.rotulo}</span>

      {situacao.dias !== null && (
        <span className="dose-detalhe">
          {formatarData(proximaDose)} · {textoDias(situacao.dias)}
        </span>
      )}
    </>
  )
}

export default DoseBadge
