import {
  PawPrint,
  CalendarCheck,
  CalendarPlus,
  Clock,
  ClipboardCheck,
  ShoppingBag,
  ShoppingCart,
  Wallet,
  Syringe,
  ArrowRight,
} from "lucide-react";

import { Link } from "react-router-dom";
import DashboardCard from "../../components/DashboardCard/DashboardCard";
import DashboardSection from "../../components/DashboardSection/DashboardSection";

function formatarData(isoString) {
  if (!isoString) return null;

  const data = new Date(isoString);

  return data.toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

// Ações mais usadas pelo cliente, a um toque de distância.
const ATALHOS = [
  {
    rota: "/minhas-consultas?agendar=1",
    titulo: "Agendar consulta",
    descricao: "Escolha o pet e o horário",
    Icone: CalendarPlus,
    destaque: true,
  },
  {
    rota: "/meus-animais",
    titulo: "Vacinas e pets",
    descricao: "Carteira de vacinação",
    Icone: Syringe,
  },
  {
    rota: "/produtos",
    titulo: "Comprar produtos",
    descricao: "Veja o que está disponível",
    Icone: ShoppingCart,
  },
  {
    rota: "/compras",
    titulo: "Minhas compras",
    descricao: "Acompanhe seus pedidos",
    Icone: ShoppingBag,
  },
];

function ClienteDashboard({ dados }) {
  const proxima = dados.proxima_consulta;

  return (
    <>
      {/* 1. O que vem agora: próxima consulta ou convite para agendar */}
      <section className="cliente-hero">
        <div className="cliente-hero-icone">
          <Clock size={24} />
        </div>

        <div className="cliente-hero-texto">
          <span className="cliente-hero-rotulo">Próxima consulta</span>

          {proxima ? (
            <>
              <strong>{proxima.animal}</strong>
              <p>
                {proxima.descricao} · {formatarData(proxima.data)}
              </p>
            </>
          ) : (
            <>
              <strong>Nenhuma consulta agendada</strong>
              <p>Agende em poucos toques.</p>
            </>
          )}
        </div>

        <Link
          className="cliente-hero-botao"
          to={proxima ? "/minhas-consultas" : "/minhas-consultas?agendar=1"}
        >
          {proxima ? "Ver consultas" : "Agendar agora"}
          <ArrowRight size={16} />
        </Link>
      </section>

      {/* 2. Atalhos para as tarefas mais comuns */}
      <DashboardSection titulo="Acesso rápido" classe="atalhos-grid">
        {ATALHOS.map(({ rota, titulo, descricao, Icone, destaque }) => (
          <Link
            key={rota}
            to={rota}
            className={`atalho ${destaque ? "atalho-destaque" : ""}`}
          >
            <span className="atalho-icone">
              <Icone size={22} />
            </span>

            <span className="atalho-texto">
              <strong>{titulo}</strong>
              <small>{descricao}</small>
            </span>
          </Link>
        ))}
      </DashboardSection>

      {/* 3. Resumo em números */}
      <DashboardSection titulo="Resumo">
        <Link to="/meus-animais" className="card-link">
          <DashboardCard
            titulo="Meus animais"
            valor={dados.total_animais}
            icone={PawPrint}
          />
        </Link>

        <Link to="/minhas-consultas" className="card-link">
          <DashboardCard
            titulo="Consultas agendadas"
            valor={dados.consultas_agendadas}
            icone={CalendarCheck}
          />
        </Link>

        <Link to="/minhas-consultas" className="card-link">
          <DashboardCard
            titulo="Consultas realizadas"
            valor={dados.consultas_realizadas}
            icone={ClipboardCheck}
          />
        </Link>

        <Link to="/meus-animais" className="card-link">
          <DashboardCard
            titulo="Próximas doses de vacina"
            valor={dados.proximas_doses_vacina}
            icone={Syringe}
          />
        </Link>

        <Link to="/compras" className="card-link">
          <DashboardCard
            titulo="Minhas compras"
            valor={dados.compras}
            icone={ShoppingBag}
          />
        </Link>

        <Link to="/compras" className="card-link">
          <DashboardCard
            titulo="Total gasto"
            valor={`R$ ${Number(dados.valor_total_compras || 0).toFixed(2)}`}
            icone={Wallet}
            cor="var(--color-accent)"
          />
        </Link>
      </DashboardSection>

      {/* 4. Pets */}
      {dados.meus_animais?.length > 0 && (
        <DashboardSection titulo="Meus animais">
          {dados.meus_animais.map((animal, index) => (
            <Link
              key={`${animal.nome}-${index}`}
              to="/meus-animais"
              className="card-link"
            >
              <DashboardCard
                titulo={animal.nome}
                valor={`${animal.idade} anos`}
                icone={PawPrint}
                cor="var(--color-brand-dark)"
              />
            </Link>
          ))}
        </DashboardSection>
      )}
    </>
  );
}

export default ClienteDashboard;
