// Regras de apresentação de vacinas, compartilhadas entre a tela de
// Vacinas (Administrador/Veterinário) e a carteira do Cliente.

// Quantos dias antes do reforço a dose passa a aparecer como "vence em breve".
export const DIAS_AVISO = 30;

const MS_POR_DIA = 24 * 60 * 60 * 1000;

// A API devolve datas sem fuso ("2026-10-20T14:30:00"); o navegador
// interpreta como horário local, que é o mesmo que o usuário vê.
export function formatarData(iso) {
  const data = new Date(iso);

  if (!iso || Number.isNaN(data.getTime())) return "—";

  return data.toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
}

function inicioDoDia(data) {
  return new Date(data.getFullYear(), data.getMonth(), data.getDate());
}

export function textoDias(dias) {
  if (dias === 0) return "hoje";

  const quantidade = Math.abs(dias);
  const unidade = quantidade === 1 ? "dia" : "dias";

  return dias < 0 ? `há ${quantidade} ${unidade}` : `em ${quantidade} ${unidade}`;
}

// Só a última aplicação de cada vacina em cada animal conta como "dose
// vigente". As anteriores já foram sucedidas por outra aplicação, então não
// devem aparecer como atrasadas. Devolve o conjunto de ids das vigentes.
export function idsDosesVigentes(aplicacoes) {
  const maisRecentePorPar = new Map();

  aplicacoes.forEach((aplicacao) => {
    const par = `${aplicacao.animal_id}|${aplicacao.vacina_id}`;
    const atual = maisRecentePorPar.get(par);

    const maisNova =
      !atual ||
      new Date(aplicacao.data_aplicacao) > new Date(atual.data_aplicacao) ||
      (aplicacao.data_aplicacao === atual.data_aplicacao &&
        aplicacao.id > atual.id);

    if (maisNova) maisRecentePorPar.set(par, aplicacao);
  });

  return new Set(Array.from(maisRecentePorPar.values(), (a) => a.id));
}

export function situacaoDaDose(aplicacao, ehVigente) {
  if (!ehVigente) {
    return { valor: "reaplicada", rotulo: "Já reaplicada", dias: null };
  }

  if (!aplicacao.proxima_dose) {
    return { valor: "sem-reforco", rotulo: "Sem reforço", dias: null };
  }

  const hoje = inicioDoDia(new Date());
  const proxima = inicioDoDia(new Date(aplicacao.proxima_dose));
  const dias = Math.round((proxima - hoje) / MS_POR_DIA);

  if (dias < 0) return { valor: "atrasada", rotulo: "Atrasada", dias };
  if (dias <= DIAS_AVISO) {
    return { valor: "vence-em-breve", rotulo: "Vence em breve", dias };
  }

  return { valor: "em-dia", rotulo: "Em dia", dias };
}
