import './DashboardCard.css'

function DashboardCard({ titulo, valor, icone: Icone, cor = 'var(--color-brand)' }) {
  const valorExibido = valor ?? '-'

  return (
    <div className="dashboard-card">
      <div className="card-icon" style={{ background: cor }}>
        {Icone && <Icone size={26} strokeWidth={2} />}
      </div>

      <div className="card-info">
        <h3>{titulo}</h3>
        <strong>{valorExibido}</strong>
      </div>

      <div className="card-detalhes" role="tooltip">
        <strong>{titulo}:</strong> {valorExibido}
      </div>
    </div>
  )
}

export default DashboardCard
