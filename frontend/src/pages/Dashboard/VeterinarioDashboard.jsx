import {
  CalendarDays,
  Clock,
  ClipboardCheck,
  PawPrint,
  Syringe,
  Pill,
} from "lucide-react";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";
import ChartCard from "../../components/ChartCard/ChartCard";

import ConsultasVeterinarioChart from "../../components/Charts/ConsultasVeterinarioChart";
import VacinasVeterinarioChart from "../../components/Charts/VacinasVeterinarioChart";
import AgendamentosChart from "../../components/Charts/AgendamentosChart";
import AnimaisEspecieChart from "../../components/Charts/AnimaisEspecieChart";

function VeterinarioDashboard({ dados }) {
  return (
    <>
      <DashboardSection titulo="Área do veterinário">
        <DashboardCard titulo="Consultas hoje" valor={dados.consultas_hoje} icone={CalendarDays} />
        <DashboardCard titulo="Próximas consultas" valor={dados.proximas_consultas} icone={Clock} />
        <DashboardCard
          titulo="Atendimentos realizados"
          valor={dados.atendimentos_realizados}
          icone={ClipboardCheck}
        />
        <DashboardCard titulo="Animais atendidos" valor={dados.animais_atendidos} icone={PawPrint} />
        <DashboardCard titulo="Vacinas aplicadas" valor={dados.vacinas_aplicadas} icone={Syringe} />
        <DashboardCard titulo="Próximas doses" valor={dados.proximas_doses} icone={Pill} />
      </DashboardSection>

      <DashboardSection titulo="Análise">
        <div className="chart-container">
          <ChartCard titulo="Consultas da semana">
            <ConsultasVeterinarioChart dados={dados} />
          </ChartCard>

          <ChartCard titulo="Controle de vacinas">
            <VacinasVeterinarioChart dados={dados} />
          </ChartCard>

          <ChartCard titulo="Agendamentos da semana">
            <AgendamentosChart dados={dados} />
          </ChartCard>

          <ChartCard titulo="Animais por espécie">
            <AnimaisEspecieChart dados={dados} />
          </ChartCard>
        </div>
      </DashboardSection>
    </>
  );
}

export default VeterinarioDashboard;
