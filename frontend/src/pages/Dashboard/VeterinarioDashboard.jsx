import {
  CalendarDays,
  Clock,
  ClipboardCheck,
  PawPrint,
  Syringe,
  Pill,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";
import ChartCard from "../../components/ChartCard/ChartCard";

import ConsultasVeterinarioChart from "../../components/Charts/ConsultasVeterinarioChart";
import VacinasVeterinarioChart from "../../components/Charts/VacinasVeterinarioChart";
import AgendamentosChart from "../../components/Charts/AgendamentosChart";
import AnimaisEspecieChart from "../../components/Charts/AnimaisEspecieChart";

function VeterinarioDashboard({ dados }) {
  const navigate = useNavigate();

  return (
    <>
      <DashboardSection titulo="Área do veterinário">
        <div onClick={() => navigate("/agendamentos")} style={{ cursor: "pointer" }}>
          <DashboardCard titulo="Consultas hoje" valor={dados.consultas_hoje} icone={CalendarDays} />
        </div>
        <div onClick={() => navigate("/agendamentos")} style={{ cursor: "pointer" }}>
          <DashboardCard titulo="Próximas consultas" valor={dados.proximas_consultas} icone={Clock} />
        </div>
        <div onClick={() => navigate("/atendimentos")} style={{ cursor: "pointer" }}>
          <DashboardCard
            titulo="Atendimentos realizados"
            valor={dados.atendimentos_realizados}
            icone={ClipboardCheck}
          />
        </div>
        <div onClick={() => navigate("/animais")} style={{ cursor: "pointer" }}>
          <DashboardCard titulo="Animais atendidos" valor={dados.animais_atendidos} icone={PawPrint} />
        </div>
        <div onClick={() => navigate("/vacinas")} style={{ cursor: "pointer" }}>
          <DashboardCard titulo="Vacinas aplicadas" valor={dados.vacinas_aplicadas} icone={Syringe} />
        </div>
        <div onClick={() => navigate("/vacinas")} style={{ cursor: "pointer" }}>
          <DashboardCard titulo="Próximas doses" valor={dados.proximas_doses} icone={Pill} />
        </div>
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
