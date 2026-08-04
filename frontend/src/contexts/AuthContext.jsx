import { createContext, useContext, useState } from "react";

const AuthContext = createContext();


export function AuthProvider({ children }) {

    const [usuario, setUsuario] = useState(() => {

        const salvo = localStorage.getItem("usuario");

        return salvo ? JSON.parse(salvo) : null;

    });



    function login(dadosUsuario) {

        setUsuario(dadosUsuario);

        localStorage.setItem(
            "usuario",
            JSON.stringify(dadosUsuario)
        );

    }



    function logout(){

        setUsuario(null);

        localStorage.removeItem("usuario");

        localStorage.removeItem("token");

    }



    return (

        <AuthContext.Provider

            value={{
                usuario,
                login,
                logout
            }}

        >

            {children}

        </AuthContext.Provider>

    );

}



export function useAuth(){

    return useContext(AuthContext);

}