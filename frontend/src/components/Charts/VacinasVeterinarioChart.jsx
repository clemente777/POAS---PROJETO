import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

// Usado no dashboard do Veterinário (vacinas_aplicadas) e do Administrador
// (aplicacoes_vacina).
function VacinasVeterinarioChart({ dados }) {
  const data = [
    {
      nome: "Aplicadas",
      quantidade: dados.vacinas_aplicadas ?? dados.aplicacoes_vacina ?? 0,
    },
    {
      nome: "Próximas doses",
      quantidade: dados.proximas_doses || 0,
    },
  ];

  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={data}>
        <XAxis dataKey="nome" />
        <YAxis allowDecimals={false} />
        <Tooltip />
        <Bar dataKey="quantidade" fill="#F2615D" />
      </BarChart>
    </ResponsiveContainer>
  );
}

export default VacinasVeterinarioChart;
