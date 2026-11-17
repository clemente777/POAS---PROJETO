import { createContext, useContext, useState } from 'react'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => {
    const salvo = localStorage.getItem('usuario')

    return salvo ? JSON.parse(salvo) : null
  })

  function login(dadosUsuario) {
    setUsuario(dadosUsuario)

    localStorage.setItem('usuario', JSON.stringify(dadosUsuario))
  }

  function logout() {
    setUsuario(null)

    localStorage.removeItem('usuario')

    localStorage.removeItem('token')
  }

  return (
    <AuthContext.Provider
      value={{
        usuario,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// O hook mora junto do Provider de propósito (12 telas importam daqui).
// A regra abaixo só afeta o hot reload deste arquivo durante o desenvolvimento.
// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  return useContext(AuthContext)
}
