import { useEffect, useState } from 'react'
import {
  UserRound,
  Mail,
  LockKeyhole,
  Save,
  LoaderCircle,
  ShieldCheck,
} from 'lucide-react'

import api from '../../services/api'
import Sidebar from '../../components/Sidebar/Sidebar'
import { useAuth } from '../../contexts/AuthContext'

import './Perfil.css'

function Perfil() {
  const { usuario, login } = useAuth()

  const [sidebarAberto, setSidebarAberto] = useState(true)
  const [perfil, setPerfil] = useState(null)

  const [formulario, setFormulario] = useState({
    nome: '',
    email: '',
    cpf: '',
    telefone: '',
    endereco: '',
  })

  const [senhas, setSenhas] = useState({
    senha_atual: '',
    nova_senha: '',
    confirmar_senha: '',
  })

  const [carregando, setCarregando] = useState(true)
  const [salvando, setSalvando] = useState(false)
  const [salvandoSenha, setSalvandoSenha] = useState(false)

  const [erro, setErro] = useState('')
  const [sucesso, setSucesso] = useState('')

  const ehCliente = usuario?.perfil === 'Cliente'

  useEffect(() => {
    carregarPerfil()
  }, [])

  async function carregarPerfil() {
    try {
      setCarregando(true)
      setErro('')

      const resposta = await api.get('/usuarios/me')

      setPerfil(resposta.data)

      setFormulario({
        nome: resposta.data.nome || '',
        email: resposta.data.email || '',
        cpf: resposta.data.cpf || '',
        telefone: resposta.data.telefone || '',
        endereco: resposta.data.endereco || '',
      })
    } catch (error) {
      setErro(error.response?.data?.detail || 'Não foi possível carregar seu perfil.')
    } finally {
      setCarregando(false)
    }
  }

  function atualizarCampo(event) {
    const { name, value } = event.target

    setFormulario((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  function atualizarSenha(event) {
    const { name, value } = event.target

    setSenhas((anterior) => ({
      ...anterior,
      [name]: value,
    }))
  }

  async function salvarPerfil(event) {
    event.preventDefault()

    try {
      setSalvando(true)
      setErro('')
      setSucesso('')

      const dados = {
        nome: formulario.nome,
        email: formulario.email,
      }

      if (ehCliente) {
        dados.cpf = formulario.cpf
        dados.telefone = formulario.telefone
        dados.endereco = formulario.endereco
      }

      const resposta = await api.put('/usuarios/me', dados)

      setPerfil(resposta.data)

      // Atualiza os dados básicos da sessão no AuthContext.
      login({
        ...usuario,
        nome: resposta.data.nome,
        email: resposta.data.email,
      })

      setSucesso('Perfil atualizado com sucesso!')
    } catch (error) {
      setErro(error.response?.data?.detail || 'Não foi possível atualizar seu perfil.')
    } finally {
      setSalvando(false)
    }
  }

  async function alterarSenha(event) {
    event.preventDefault()

    setErro('')
    setSucesso('')

    if (senhas.nova_senha !== senhas.confirmar_senha) {
      setErro('A confirmação da nova senha não corresponde.')
      return
    }

    if (senhas.nova_senha.length < 6) {
      setErro('A nova senha deve possuir pelo menos 6 caracteres.')
      return
    }

    try {
      setSalvandoSenha(true)

      await api.put('/usuarios/me/senha', {
        senha_atual: senhas.senha_atual,
        nova_senha: senhas.nova_senha,
      })

      setSenhas({
        senha_atual: '',
        nova_senha: '',
        confirmar_senha: '',
      })

      setSucesso('Senha alterada com sucesso!')
    } catch (error) {
      setErro(error.response?.data?.detail || 'Não foi possível alterar sua senha.')
    } finally {
      setSalvandoSenha(false)
    }
  }

  if (carregando) {
    return (
      <div className="perfil-carregando">
        <LoaderCircle className="perfil-spinner" size={30} />
        <p>Carregando perfil...</p>
      </div>
    )
  }

  return (
    <div className="perfil-layout">
      <Sidebar perfil={usuario?.perfil} setSidebarAberto={setSidebarAberto} />

      <main className={`perfil-conteudo ${sidebarAberto ? 'aberto' : 'fechado'}`}>
        <header className="perfil-cabecalho">
          <div>
            <span className="perfil-subtitulo">MINHA CONTA</span>
            <h1>Meu perfil</h1>
            <p>Consulte e atualize suas informações pessoais.</p>
          </div>

          <div className="perfil-identificacao">
            <UserRound size={22} />
            <div>
              <strong>{perfil?.nome}</strong>
              <span>{perfil?.perfil}</span>
            </div>
          </div>
        </header>

        {erro && <div className="perfil-mensagem erro">{erro}</div>}
        {sucesso && <div className="perfil-mensagem sucesso">{sucesso}</div>}

        <section className="perfil-card">
          <div className="perfil-card-titulo">
            <div className="perfil-icone">
              <UserRound size={20} />
            </div>
            <div>
              <h2>Informações pessoais</h2>
              <p>Seus dados de identificação e contato.</p>
            </div>
          </div>

          <form onSubmit={salvarPerfil}>
            <div className="perfil-form-grid">
              <label className="perfil-campo">
                <span>Nome completo</span>
                <input
                  type="text"
                  name="nome"
                  value={formulario.nome}
                  onChange={atualizarCampo}
                  minLength={3}
                  maxLength={100}
                  required
                />
              </label>

              <label className="perfil-campo">
                <span>E-mail</span>
                <div className="perfil-input-icone">
                  <Mail size={17} />
                  <input
                    type="email"
                    name="email"
                    value={formulario.email}
                    onChange={atualizarCampo}
                    required
                  />
                </div>
              </label>

              {ehCliente && (
                <>
                  <label className="perfil-campo">
                    <span>CPF</span>
                    <input
                      type="text"
                      name="cpf"
                      value={formulario.cpf}
                      onChange={atualizarCampo}
                      maxLength={14}
                      required
                    />
                  </label>

                  <label className="perfil-campo">
                    <span>Telefone</span>
                    <input
                      type="tel"
                      name="telefone"
                      value={formulario.telefone}
                      onChange={atualizarCampo}
                      maxLength={15}
                      required
                    />
                  </label>

                  <label className="perfil-campo perfil-campo-largo">
                    <span>Endereço</span>
                    <input
                      type="text"
                      name="endereco"
                      value={formulario.endereco}
                      onChange={atualizarCampo}
                      maxLength={255}
                      required
                    />
                  </label>
                </>
              )}
            </div>

            <div className="perfil-card-rodape">
              <button type="submit" className="perfil-botao" disabled={salvando}>
                {salvando ? (
                  <LoaderCircle size={17} className="perfil-spinner" />
                ) : (
                  <Save size={17} />
                )}
                {salvando ? 'Salvando...' : 'Salvar alterações'}
              </button>
            </div>
          </form>
        </section>

        <section className="perfil-card">
          <div className="perfil-card-titulo">
            <div className="perfil-icone">
              <LockKeyhole size={20} />
            </div>
            <div>
              <h2>Segurança</h2>
              <p>Altere sua senha de acesso ao sistema.</p>
            </div>
          </div>

          <form onSubmit={alterarSenha}>
            <div className="perfil-form-grid">
              <label className="perfil-campo">
                <span>Senha atual</span>
                <input
                  type="password"
                  name="senha_atual"
                  value={senhas.senha_atual}
                  onChange={atualizarSenha}
                  autoComplete="current-password"
                  required
                />
              </label>

              <label className="perfil-campo">
                <span>Nova senha</span>
                <input
                  type="password"
                  name="nova_senha"
                  value={senhas.nova_senha}
                  onChange={atualizarSenha}
                  minLength={6}
                  autoComplete="new-password"
                  required
                />
              </label>

              <label className="perfil-campo">
                <span>Confirmar nova senha</span>
                <input
                  type="password"
                  name="confirmar_senha"
                  value={senhas.confirmar_senha}
                  onChange={atualizarSenha}
                  minLength={6}
                  autoComplete="new-password"
                  required
                />
              </label>
            </div>

            <div className="perfil-card-rodape">
              <button
                type="submit"
                className="perfil-botao perfil-botao-secundario"
                disabled={salvandoSenha}
              >
                {salvandoSenha ? (
                  <LoaderCircle size={17} className="perfil-spinner" />
                ) : (
                  <ShieldCheck size={17} />
                )}
                {salvandoSenha ? 'Alterando...' : 'Alterar senha'}
              </button>
            </div>
          </form>
        </section>

        <div className="perfil-nota">
          <ShieldCheck size={18} />
          <p>
            Seu perfil de acesso ({perfil?.perfil}) não pode ser alterado por esta
            página.
          </p>
        </div>
      </main>
    </div>
  )
}

export default Perfil
