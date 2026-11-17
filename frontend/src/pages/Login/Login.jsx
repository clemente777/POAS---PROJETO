
import './Login.css'

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import api from '../../services/api'

import logo from '../../assets/logo.png'
import Input from '../../components/Input/Input'
import Button from '../../components/button/Button'

import { useAuth } from '../../contexts/AuthContext'

function Login() {
  const navigate = useNavigate()
  const { login } = useAuth()

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [mensagemErro, setMensagemErro] = useState('')
  const [carregando, setCarregando] = useState(false)

  async function entrar(e) {
    e.preventDefault()

    if (carregando) return

    setMensagemErro('')
    setCarregando(true)

    try {
      const dados = new URLSearchParams()

      dados.append('username', email.trim().toLowerCase())
      dados.append('password', senha)

      const resposta = await api.post('/login/', dados, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      })

      const { access_token, usuario } = resposta.data

      if (!access_token || !usuario) {
        throw new Error('Resposta de autenticação inválida.')
      }

      localStorage.setItem('token', access_token)

      login(usuario)

      navigate('/dashboard', { replace: true })
    } catch (erro) {
      console.error('Erro ao realizar login:', erro)

      if (erro.response) {
        const detalhe = erro.response.data?.detail

        if (Array.isArray(detalhe)) {
          setMensagemErro(
            detalhe.map((item) => item.msg).join(', ')
          )
        } else {
          setMensagemErro(
            detalhe || `Não foi possível entrar. Erro ${erro.response.status}.`
          )
        }
      } else if (erro.request) {
        setMensagemErro(
          'Não foi possível conectar ao servidor. Verifique se o backend está funcionando.'
        )
      } else {
        setMensagemErro(
          erro.message || 'Ocorreu um erro ao realizar o login.'
        )
      }
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="login">
      <div className="left">
        <img src={logo} alt="Logo Petonline24h" />
      </div>

      <div className="right">
        <div className="box">
          <h1>Bem-Vindo!</h1>

          <form onSubmit={entrar}>
            {mensagemErro && (
              <p className="erro-login" role="alert">
                {mensagemErro}
              </p>
            )}

            <Input
              type="email"
              placeholder="Email"
              autoComplete="email"
              inputMode="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={carregando}
            />

            <Input
              type="password"
              placeholder="Senha"
              autoComplete="current-password"
              required
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              disabled={carregando}
            />

            <Button>
              {carregando ? 'Entrando...' : 'Entrar'}
            </Button>
          </form>

          <div className="links">
            <Link to="/cadastro">Criar conta</Link>

            <a href="#" onClick={(e) => e.preventDefault()}>
              Esqueci minha senha
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Login
