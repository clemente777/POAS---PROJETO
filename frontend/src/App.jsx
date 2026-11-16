import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home/Home";
import Login from "./pages/Login/Login";
import Cadastro from "./pages/Cadastro/Cadastro";
import Dashboard from "./pages/Dashboard/Dashboard";
import Animais from "./pages/Animais/Animais";
import MeusAnimais from "./pages/MeusAnimais/MeusAnimais";
import MinhasConsultas from "./pages/MinhasConsultas/MinhasConsultas";
import Compras from "./pages/Compras/Compras";
import Produtos from "./pages/Produtos/Produtos";
import Vacinas from "./pages/Vacinas/Vacinas";
import Agendamentos from "./pages/Agendamentos/Agendamentos";
import Atendimentos from "./pages/Atendimentos/Atendimentos";


function App(){

  return (

    <BrowserRouter>

      <Routes>


        <Route 
          path="/" 
          element={<Home />}
        />


        <Route 
          path="/login" 
          element={<Login />}
        />


        <Route 
          path="/cadastro" 
          element={<Cadastro />}
        />


        <Route 
          path="/dashboard" 
          element={<Dashboard />}
        />


        <Route
          path="/animais"
          element={<Animais />}
        />


        <Route
          path="/meus-animais"
          element={<MeusAnimais />}
        />

        <Route
          path="/minhas-consultas"
          element={<MinhasConsultas />}
        />
        <Route 
          path="/compras" 
          element={<Compras />} 
        />

        <Route
          path="/produtos"
          element={<Produtos />}
        />

        <Route
          path="/vacinas"
          element={<Vacinas />}
        />

        <Route
          path="/agendamentos"
          element={<Agendamentos />}
        />

        <Route
          path="/atendimentos"
          element={<Atendimentos />}
        />

      </Routes>

    </BrowserRouter>

  );

}


export default App;