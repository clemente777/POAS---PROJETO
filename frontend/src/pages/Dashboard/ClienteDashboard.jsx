import {
  PawPrint,
  CalendarCheck,
  Clock,
  ClipboardCheck,
  ShoppingBag,
  Wallet,
  Syringe,
} from "lucide-react";

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

function ClienteDashboard({ dados }) {
  const proxima = dados.proxima_consulta;

  return (
    <>
      <DashboardSection titulo="Minha área">
        <DashboardCard titulo="Meus animais" valor={dados.total_animais} icone={PawPrint} />
        <DashboardCard
          titulo="Consultas agendadas"
          valor={dados.consultas_agendadas}
          icone={CalendarCheck}
        />
        <DashboardCard
          titulo="Consultas realizadas"
          valor={dados.consultas_realizadas}
          icone={ClipboardCheck}
        />
        <DashboardCard
          titulo="Próximas doses de vacina"
          valor={dados.proximas_doses_vacina}
          icone={Syringe}
        />
        <DashboardCard titulo="Minhas compras" valor={dados.compras} icone={ShoppingBag} />
        <DashboardCard
          titulo="Total gasto"
          valor={`R$ ${Number(dados.valor_total_compras || 0).toFixed(2)}`}
          icone={Wallet}
          cor="var(--color-accent)"
        />
      </DashboardSection>

      {proxima && (
        <DashboardSection titulo="Próxima consulta">
          <div className="proxima-consulta-card">
            <div className="proxima-consulta-icon">
              <Clock size={22} />
            </div>

            <div>
              <strong>{proxima.animal}</strong>
              <p>{proxima.descricao}</p>
              <span>{formatarData(proxima.data)}</span>
            </div>
          </div>
        </DashboardSection>
      )}

      {dados.meus_animais?.length > 0 && (
        <DashboardSection titulo="Meus animais">
          {dados.meus_animais.map((animal, index) => (
            <DashboardCard
              key={`${animal.nome}-${index}`}
              titulo={animal.nome}
              valor={`${animal.idade} anos`}
              icone={PawPrint}
              cor="var(--color-brand-dark)"
            />
          ))}
        </DashboardSection>
      )}
    </>
  );
}

export default ClienteDashboard;
