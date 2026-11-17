import axios from "axios";


/*
| URL da API.
| - Se existir VITE_API_URL (arquivo frontend/.env), ela é usada.
| - Caso contrário, usa o mesmo endereço em que o site foi aberto, na porta 8000.
|   Assim funciona no PC (localhost) e no celular (ex.: http://192.168.0.10:5173),
|   pois "127.0.0.1" no celular aponta para o próprio celular, não para o PC.
*/
export const API_URL =
    import.meta.env.VITE_API_URL ||
    `${window.location.protocol}//${window.location.hostname}:8000`;


const api = axios.create({

    baseURL: API_URL

});


api.interceptors.request.use(

    (config)=>{


        const token = localStorage.getItem("token");


        if(token){

            config.headers.Authorization =
            `Bearer ${token}`;

        }


        return config;

    },


    (error)=>{

        return Promise.reject(error);

    }

);


export default api;
