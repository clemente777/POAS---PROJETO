/*
|--------------------------------------------------------------------------
| Arquivo: App.jsx
| Projeto: Petonline24h
|--------------------------------------------------------------------------
|
| Finalidade:
| Componente principal responsável por organizar a navegação do sistema.
|
| Responsabilidades:
| - Configurar o roteamento da aplicação.
| - Associar cada endereço à sua respectiva página.
| - Utilizar carregamento sob demanda (Lazy Loading).
| - Apresentar um conteúdo temporário durante o carregamento das páginas.
|
| Tecnologias:
| - React: construção da interface.
| - React Router DOM: gerenciamento das rotas.
| - React.lazy: carregamento sob demanda dos componentes.
| - Suspense: gerenciamento do estado de carregamento.
|
|--------------------------------------------------------------------------
*/

import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { lazy, Suspense } from 'react'

/*
|--------------------------------------------------------------------------
| CARREGAMENTO SOB DEMANDA (LAZY LOADING)
|--------------------------------------------------------------------------
|
| O React.lazy permite importar componentes somente quando necessário.
|
| Dessa forma, as páginas não precisam ser carregadas todas de uma vez
| quando o usuário acessa o sistema.
|
| Benefícios:
| - Redução do JavaScript carregado inicialmente.
| - Divisão do código em arquivos menores.
| - Melhoria no carregamento inicial da aplicação.
|
*/

// Página inicial
const Home = lazy(() => import('./pages/Home/Home'))

// Autenticação e cadastro
const Login = lazy(() => import('./pages/Login/Login'))
const Cadastro = lazy(() => import('./pages/Cadastro/Cadastro'))

// Painel administrativo e gerenciamento
const Dashboard = lazy(() => import('./pages/Dashboard/Dashboard'))
const Animais = lazy(() => import('./pages/Animais/Animais'))
const Clientes = lazy(() => import('./pages/Clientes/Clientes'))

// Funcionalidades destinadas aos clientes
const MeusAnimais = lazy(() => import('./pages/MeusAnimais/MeusAnimais'))
const MinhasConsultas = lazy(() => import('./pages/MinhasConsultas/MinhasConsultas'))
const Compras = lazy(() => import('./pages/Compras/Compras'))

// Produtos e serviços veterinários
const Produtos = lazy(() => import('./pages/Produtos/Produtos'))
const Vacinas = lazy(() => import('./pages/Vacinas/Vacinas'))
const Agendamentos = lazy(() => import('./pages/Agendamentos/Agendamentos'))
const Atendimentos = lazy(() => import('./pages/Atendimentos/Atendimentos'))

/*
|--------------------------------------------------------------------------
| COMPONENTE PRINCIPAL
|--------------------------------------------------------------------------
|
| O BrowserRouter disponibiliza o sistema de navegação baseado no
| histórico do navegador.
|
| O componente Routes agrupa as rotas disponíveis.
|
| Cada Route associa um caminho (path) a um componente (element).
|
| O Suspense apresenta uma mensagem enquanto uma página importada
| com React.lazy ainda está sendo carregada.
|
*/

function App() {
  return (
    <BrowserRouter>
      <Suspense fallback={<div>Carregando página...</div>}>
        <Routes>
          {/* Página inicial */}
          <Route path="/" element={<Home />} />

          {/* Autenticação e cadastro */}
          <Route path="/login" element={<Login />} />
          <Route path="/cadastro" element={<Cadastro />} />

          {/* Painel e gerenciamento de animais */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/animais" element={<Animais />} />
          <Route path="/clientes" element={<Clientes />} />
          {/* Área do cliente */}
          <Route path="/meus-animais" element={<MeusAnimais />} />
          <Route path="/minhas-consultas" element={<MinhasConsultas />} />
          <Route path="/compras" element={<Compras />} />

          {/* Produtos e funcionalidades veterinárias */}
          <Route path="/produtos" element={<Produtos />} />
          <Route path="/vacinas" element={<Vacinas />} />
          <Route path="/agendamentos" element={<Agendamentos />} />
          <Route path="/atendimentos" element={<Atendimentos />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}

// Disponibiliza o componente principal para inicialização da aplicação.
export default App
