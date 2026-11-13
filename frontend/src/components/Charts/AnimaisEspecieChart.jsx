import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { CHART_COLORS } from "./chartColors";

// Recebe o objeto { Cachorro: 3, Gato: 2 } (como a API devolve) ou uma
// lista [{ especie, quantidade }].
function AnimaisEspecieChart({ animais_por_especie }) {
  const data = Array.isArray(animais_por_especie)
    ? animais_por_especie
    : Object.entries(animais_por_especie || {}).map(
        ([especie, quantidade]) => ({ especie, quantidade })
      );

  return (
    <ResponsiveContainer width="100%" height={250}>
      <BarChart data={data} layout="vertical" margin={{ left: 30, right: 20 }}>
        <XAxis type="number" allowDecimals={false} />
        <YAxis type="category" dataKey="especie" width={80} />
        <Tooltip />

        <Bar dataKey="quantidade" radius={[0, 8, 8, 0]}>
          {data.map((item, index) => (
            <Cell key={index} fill={CHART_COLORS[index % CHART_COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}

export default AnimaisEspecieChart;
