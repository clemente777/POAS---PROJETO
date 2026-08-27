import "./Home.css";

import { Link } from "react-router-dom";
import { PawPrint, CalendarCheck, Stethoscope } from "lucide-react";

import vetImage from "../../assets/vet-home.jpg";

import Navbar from "../../components/Navbar/Navbar";
import ServiceAreaMap from "../../components/ServiceAreaMap/ServiceAreaMap";

// Área de cobertura: todo o estado do Rio Grande do Norte (retângulo aproximado).
const coverageArea = [
  [-4.85, -38.6],
  [-4.85, -34.95],
  [-6.98, -34.95],
  [-6.98, -38.6],
];

// Ponto de destaque: Patu/RN.
const coveragePoints = [
  {
    id: "1",
    name: "Patu",
    description: "Atendimento presencial e emergências.",
    position: [-6.1066, -37.6356],
    type: "clinic",
  },
];

const services = [
  {
    icon: PawPrint,
    title: "Gestão de animais",
    description: "Cadastro completo dos pacientes, com histórico sempre à mão.",
  },
  {
    icon: CalendarCheck,
    title: "Agendamentos",
    description: "Controle consultas e horários sem depender de planilhas.",
  },
  {
    icon: Stethoscope,
    title: "Atendimentos",
    description: "Histórico médico organizado do primeiro ao último atendimento.",
  },
];

function HeartbeatDivider() {
  return (
    <svg
      className="heartbeat-divider"
      viewBox="0 0 1200 60"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <polyline
        points="0,30 260,30 300,10 330,50 360,30 900,30 940,8 970,52 1000,30 1200,30"
        fill="none"
        stroke="currentColor"
        strokeWidth="3"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

function Home() {
  return (
    <div className="home">
      <Navbar />

      <section className="hero">
        <div className="hero-text">
          <span className="eyebrow">Sistema para clínicas veterinárias</span>

          <h1>
            Cuidando do seu pet
            <br />
            com tecnologia e carinho
          </h1>

          <p>
            Um sistema completo para clínicas veterinárias. Controle
            animais, consultas e atendimentos em um único lugar.
          </p>

          <div className="hero-buttons">
            <Link to="/login" className="btn-primary">
              Acessar sistema
            </Link>

            <a href="#servicos" className="btn-secondary">
              Conheça nossos serviços
            </a>
          </div>
        </div>

        <div className="hero-image">
          <div className="hero-image-shape" aria-hidden="true" />
          <img src={vetImage} alt="Veterinário atendendo um animal" />
        </div>
      </section>

      <HeartbeatDivider />

      <section className="services" id="servicos">
        <h2>Nossos serviços</h2>

        <div className="service-grid">
          {services.map(({ icon: Icon, title, description }) => (
            <div className="service-card" key={title}>
              <div className="service-icon">
                <Icon size={22} strokeWidth={2} />
              </div>

              <h3>{title}</h3>
              <p>{description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="coverage" id="cobertura">
        <div className="coverage-intro">
          <span className="eyebrow">Onde atendemos</span>
          <h2>Confira a área de atendimento</h2>
          <p>
            Veja a região coberta e as unidades parceiras mais próximas
            de você.
          </p>
        </div>

        <ServiceAreaMap
          title="Área de atendimento"
          subtitle="Cobertura disponível em todo o Rio Grande do Norte"
          center={[-5.6, -36.6]}
          zoom={7}
          autoFit={false}
          coverageArea={coverageArea}
          points={coveragePoints}
        />
      </section>

      <section className="about" id="sobre">
        <h2>Tecnologia para cuidar melhor</h2>

        <p>
          O Petonline24h ajuda clínicas veterinárias a organizarem sua
          rotina, melhorarem o atendimento e acompanharem cada paciente.
        </p>
      </section>

      <footer id="contato">
        <PawPrint size={18} strokeWidth={2} />
        Petonline24h Clínica Veterinária
      </footer>
    </div>
  );
}

export default Home;
