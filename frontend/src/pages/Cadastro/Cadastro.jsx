
import './Cadastro.css'

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import api from '../../services/api'

import logo from '../../assets/logo.png'

import Input from '../../components/Input/Input'
import Button from '../../components/button/Button'

function Cadastro() {
  const navigate = useNavigate()

  const [nome, setNome] = useState('')
  const [cpf, setCpf] = useState('')
  const [telefone, setTelefone] = useState('')
  const [email, setEmail] = useState('')
  const [endereco, setEndereco] = useState('')
  const [senha, setSenha] = useState('')

  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState('')
  const [carregando, setCarregando] = useState(false)

  async function cadastrar(evento) {
    evento.preventDefault()

    if (carregando) return

    setErro('')
    setSucesso('')
    setCarregando(true)

    try {
      const dados = {
        nome: nome.trim(),
        cpf: cpf.trim(),
        telefone: telefone.trim(),
        email: email.trim().toLowerCase(),
        endereco: endereco.trim(),
        senha,
      }

      await api.post('/cadastro/', dados)

      setSucesso('Cadastro realizado com sucesso!')

      // Aguarda a atualização da interface antes de navegar.
      await new Promise((resolve) => setTimeout(resolve, 1500))

      navigate('/login', { replace: true })
    } catch (error) {
      console.error('Erro ao realizar cadastro:', error)

      if (error.response) {
        const detalhe = error.response.data?.detail

        if (Array.isArray(detalhe)) {
          setErro(
            detalhe
              .map((item) => {
                if (item.campo) {
                  return `${item.campo}: ${item.mensagem}`
                }

                return item.msg || 'Erro de validação.'
              })
              .join('\n')
          )
        } else {
          setErro(
            detalhe || `Não foi possível cadastrar. Erro ${error.response.status}.`
          )
        }
      } else if (error.request) {
        setErro(
          'Não foi possível conectar ao servidor. Verifique se o backend está funcionando.'
        )
      } else {
        setErro(
          error.message || 'Ocorreu um erro ao realizar o cadastro.'
        )
      }
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="cadastro">

      <div className="cadastro-info">

        <img
          src={logo}
          className="logo-poas"
          alt="Logo Petonline24h"
        />

        <h2>
          Cuidado completo para seu pet
        </h2>

        <p className="descricao-poas">
          Agende consultas, acompanhe históricos e cuide melhor
          do seu animal.
        </p>

      </div>

      <div className="cadastro-box">

        <h1>Criar Conta</h1>

        <p className="subtitulo">
          Cadastre-se no Petonline24h
        </p>

        <form onSubmit={cadastrar}>

          {erro && (
            <div className="mensagem erro" role="alert">
              <strong>Erro:</strong>
              <span style={{ whiteSpace: 'pre-line' }}>
                {erro}
              </span>
            </div>
          )}

          {sucesso && (
            <div className="mensagem sucesso" role="status">
              {sucesso}
            </div>
          )}

          <Input
            type="text"
            placeholder="Nome completo"
            autoComplete="name"
            required
            value={nome}
            onChange={(e) => setNome(e.target.value)}
            disabled={carregando}
          />

          <Input
            type="text"
            placeholder="CPF"
            autoComplete="off"
            required
            value={cpf}
            onChange={(e) => setCpf(e.target.value)}
            disabled={carregando}
          />

          <Input
            type="tel"
            placeholder="Telefone"
            autoComplete="tel"
            required
            value={telefone}
            onChange={(e) => setTelefone(e.target.value)}
            disabled={carregando}
          />

          <Input
            type="email"
            placeholder="Email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            disabled={carregando}
          />

          <Input
            type="text"
            placeholder="Endereço"
            autoComplete="street-address"
            required
            value={endereco}
            onChange={(e) => setEndereco(e.target.value)}
            disabled={carregando}
          />

          <Input
            type="password"
            placeholder="Senha"
            autoComplete="new-password"
            required
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            disabled={carregando}
          />

          <Button disabled={carregando}>
            {carregando ? 'Cadastrando...' : 'Criar conta'}
          </Button>

        </form>

        <button
          className="voltar"
          type="button"
          onClick={() => navigate('/login')}
          disabled={carregando}
        >
          Já tenho conta
        </button>

      </div>

    </div>
  )
}

export default Cadastro
