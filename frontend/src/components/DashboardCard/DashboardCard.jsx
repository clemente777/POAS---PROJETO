import "./DashboardCard.css";

function DashboardCard({
  titulo,
  valor,
  icone: Icone,
  cor = "var(--color-brand)",
}) {
  return (
    <div className="dashboard-card">
      <div className="card-icon" style={{ background: cor }}>
        {Icone && <Icone size={26} strokeWidth={2} />}
      </div>

      <div className="card-info">
        <h3>{titulo}</h3>
        <strong>{valor ?? "-"}</strong>
      </div>
    </div>
  );
}

export default DashboardCard;
