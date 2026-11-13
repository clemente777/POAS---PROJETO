import {
  Users,
  ShieldCheck,
  Stethoscope,
  UsersRound,
  PawPrint,
  CalendarCheck,
  ClipboardList,
  ClipboardCheck,
  ShoppingCart,
  Wallet,
  AlertTriangle,
  XCircle,
  CalendarDays,
  CalendarClock,
  CalendarX,
  Cake,
  TrendingUp,
  UserRound,
  Syringe,
  Pill,
  BookOpen,
  Trophy,
  Tag,
} from "lucide-react";

import { useNavigate } from "react-router-dom";

import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";
import ChartCard from "../../components/ChartCard/ChartCard";

import UsuariosChart from "../../components/Charts/UsuariosChart";
import EstoqueChart from "../../components/Charts/EstoqueChart";
import AgendamentosChart from "../../components/Charts/AgendamentosChart";
import AnimaisEspecieChart from "../../components/Charts/AnimaisEspecieChart";
import VacinasVeterinarioChart from "../../components/Charts/VacinasVeterinarioChart";

function moeda(valor) {
  return Number(valor || 0).toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}

function textoProduto(produto) {
  if (!produto) return "-";

  return `${produto.nome} (${moeda(produto.preco)})`;
}

// Card clicável que leva para outra tela.
function Atalho({ para, children }) {
  const navigate = useNavigate();

  return (
    <div
      role="link"
      tabIndex={0}
      style={{ cursor: "pointer" }}
      onClick={() => navigate(para)}
      onKeyDown={(e) => {
        if (e.key === "Enter") navigate(para);
      }}
    >
      {children}
    </div>
  );
}

function AdminDashboard({ dados }) {
  return (
    <>
      <DashboardSection titulo="Estatísticas gerais">
        <DashboardCard titulo="Usuários" valor={dados.usuarios} icone={Users} />
        <DashboardCard titulo="Administradores" valor={dados.administradores} icone={ShieldCheck} />
        <DashboardCard titulo="Veterinários" valor={dados.veterinarios} icone={Stethoscope} />
        <DashboardCard titulo="Clientes" valor={dados.clientes} icone={UsersRound} />

        <Atalho para="/animais">
          <DashboardCard titulo="Animais" valor={dados.animais} icone={PawPrint} />
        </Atalho>

        <DashboardCard titulo="Agendamentos" valor={dados.agendamentos} icone={CalendarCheck} />
        <DashboardCard titulo="Atendimentos" valor={dados.atendimentos} icone={ClipboardList} />

        <Atalho para="/produtos">
          <DashboardCard titulo="Produtos" valor={dados.produtos} icone={ShoppingCart} />
        </Atalho>
      </DashboardSection>

      <DashboardSection titulo="Agenda e atendimentos">
        <DashboardCard titulo="Agendamentos hoje" valor={dados.agendamentos_hoje} icone={CalendarDays} />
        <DashboardCard titulo="Agendamentos futuros" valor={dados.agendamentos_futuros} icone={CalendarClock} />
        <DashboardCard
          titulo="Agendamentos cancelados"
          valor={dados.agendamentos_cancelados}
          icone={CalendarX}
          cor="var(--color-accent-dark)"
        />
        <DashboardCard titulo="Atendimentos hoje" valor={dados.atendimentos_hoje} icone={ClipboardList} />
        <DashboardCard
          titulo="Atendimentos finalizados"
          valor={dados.atendimentos_finalizados}
          icone={ClipboardCheck}
        />
      </DashboardSection>

      <DashboardSection titulo="Estoque">
        <DashboardCard
          titulo="Valor total"
          valor={moeda(dados.valor_total_estoque)}
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
        <DashboardCard
          titulo="Produto mais caro"
          valor={textoProduto(dados.produto_mais_caro)}
          icone={Tag}
        />
        <DashboardCard
          titulo="Produto mais barato"
          valor={textoProduto(dados.produto_mais_barato)}
          icone={Tag}
        />
      </DashboardSection>

      <DashboardSection titulo="Vacinas">
        <Atalho para="/vacinas">
          <DashboardCard titulo="Vacinas no catálogo" valor={dados.vacinas} icone={BookOpen} />
        </Atalho>

        <Atalho para="/vacinas">
          <DashboardCard titulo="Aplicações registradas" valor={dados.aplicacoes_vacina} icone={Syringe} />
        </Atalho>

        <Atalho para="/vacinas">
          <DashboardCard titulo="Próximas doses" valor={dados.proximas_doses} icone={Pill} />
        </Atalho>

        <Atalho para="/vacinas">
          <DashboardCard
            titulo="Vacina mais aplicada"
            valor={
              dados.vacina_mais_aplicada
                ? `${dados.vacina_mais_aplicada.nome} (${dados.vacina_mais_aplicada.quantidade})`
                : "-"
            }
            icone={Trophy}
            cor="var(--color-accent)"
          />
        </Atalho>
      </DashboardSection>

      <DashboardSection titulo="Animais">
        <DashboardCard
          titulo="Animal mais velho"
          valor={dados.animal_mais_velho?.nome || "-"}
          icone={PawPrint}
        />
        <DashboardCard
          titulo="Idade do mais velho"
          valor={dados.animal_mais_velho ? `${dados.animal_mais_velho.idade} anos` : "-"}
          icone={Cake}
        />
        <DashboardCard titulo="Média de idade" valor={dados.media_idade_animais} icone={TrendingUp} />
      </DashboardSection>

      <DashboardSection titulo="Clientes">
        <DashboardCard
          titulo="Cliente com mais animais"
          valor={dados.cliente_com_mais_animais?.nome || "-"}
          icone={UserRound}
        />
        <DashboardCard
          titulo="Quantidade de animais"
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

          <ChartCard titulo="Controle de vacinas">
            <VacinasVeterinarioChart dados={dados} />
          </ChartCard>

          <ChartCard titulo="Animais por espécie">
            <AnimaisEspecieChart animais_por_especie={dados.animais_por_especie} />
          </ChartCard>
        </div>
      </DashboardSection>
    </>
  );
}

export default AdminDashboard;
