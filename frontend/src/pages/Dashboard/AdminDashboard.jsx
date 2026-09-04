import {
  Users,
  ShieldCheck,
  Stethoscope,
  UsersRound,
  PawPrint,
  CalendarCheck,
  ClipboardList,
  ShoppingCart,
  Wallet,
  AlertTriangle,
  XCircle,
  CalendarDays,
  CalendarClock,
  Cake,
  TrendingUp,
  UserRound,
} from "lucide-react";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";
import ChartCard from "../../components/ChartCard/ChartCard";

import UsuariosChart from "../../components/Charts/UsuariosChart";
import EstoqueChart from "../../components/Charts/EstoqueChart";
import AgendamentosChart from "../../components/Charts/AgendamentosChart";
import AnimaisEspecieChart from "../../components/Charts/AnimaisEspecieChart";

function AdminDashboard({ dados }) {
  return (
    <>
      <DashboardSection titulo="Estatísticas gerais">
        <DashboardCard titulo="Usuários" valor={dados.usuarios} icone={Users} />
        <DashboardCard titulo="Administradores" valor={dados.administradores} icone={ShieldCheck} />
        <DashboardCard titulo="Veterinários" valor={dados.veterinarios} icone={Stethoscope} />
        <DashboardCard titulo="Clientes" valor={dados.clientes} icone={UsersRound} />
        <DashboardCard titulo="Animais" valor={dados.animais} icone={PawPrint} />
        <DashboardCard titulo="Agendamentos" valor={dados.agendamentos} icone={CalendarCheck} />
        <DashboardCard titulo="Atendimentos" valor={dados.atendimentos} icone={ClipboardList} />
        <DashboardCard titulo="Produtos" valor={dados.produtos} icone={ShoppingCart} />
      </DashboardSection>

      <DashboardSection titulo="Estoque">
        <DashboardCard
          titulo="Valor total"
          valor={`R$ ${dados.valor_total_estoque}`}
          icone={Wallet}
          cor="var(--color-accent)"
        />
        <DashboardCard
          titulo="Estoque baixo"
          valor={dados.estoque_baixo}
          icone={AlertTriangle}
          cor="var(--color-accent)"
        />
        <DashboardCard
          titulo="Sem estoque"
          valor={dados.produtos_sem_estoque}
          icone={XCircle}
          cor="var(--color-accent-dark)"
        />
      </DashboardSection>

      <DashboardSection titulo="Agenda">
        <DashboardCard titulo="Hoje" valor={dados.agendamentos_hoje} icone={CalendarDays} />
        <DashboardCard titulo="Futuros" valor={dados.agendamentos_futuros} icone={CalendarClock} />
      </DashboardSection>

      <DashboardSection titulo="Animais">
        <DashboardCard
          titulo="Animal mais velho"
          valor={dados.animal_mais_velho?.nome || "-"}
          icone={PawPrint}
        />
        <DashboardCard titulo="Idade" valor={dados.animal_mais_velho?.idade || "-"} icone={Cake} />
        <DashboardCard titulo="Média de idade" valor={dados.media_idade_animais} icone={TrendingUp} />
      </DashboardSection>

      <DashboardSection titulo="Clientes">
        <DashboardCard
          titulo="Cliente com mais animais"
          valor={dados.cliente_com_mais_animais?.nome || "-"}
          icone={UserRound}
        />
        <DashboardCard
          titulo="Quantidade"
          valor={dados.cliente_com_mais_animais?.quantidade || 0}
          icone={PawPrint}
        />
      </DashboardSection>

      <DashboardSection titulo="Análise">
        <div className="chart-container">
          <ChartCard titulo="Usuários por perfil">
            <UsuariosChart dados={dados} />
          </ChartCard>

          <ChartCard titulo="Situação do estoque">
            <EstoqueChart dados={dados} />
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

export default AdminDashboard;
