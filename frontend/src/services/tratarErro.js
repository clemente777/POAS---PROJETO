function tratarErro(error){


    // ====================================
    // ERRO VINDO DO FASTAPI
    // ====================================

    if(error.response){


        const status = error.response.status;

        const detalhe = error.response.data.detail;



        // Erro simples do HTTPException

        if(typeof detalhe === "string"){


            return {

                titulo: "Erro na operação",

                mensagem: detalhe,

                status: status

            };


        }



        // Erro de validação Pydantic

        if(Array.isArray(detalhe)){


            const mensagens = detalhe.map((item)=>{


                const campo = item.loc
                    ? item.loc[item.loc.length - 1]
                    : "campo";


                return `${campo}: ${item.msg}`;


            });



            return {


                titulo:
                "Dados inválidos",


                mensagem:
                mensagens.join("\n"),


                status: status


            };


        }



        return {


            titulo:
            "Erro no servidor",


            mensagem:
            "O servidor retornou um erro.",


            status: status


        };


    }



    // ====================================
    // SERVIDOR NÃO RESPONDEU
    // ====================================


    if(error.request){


        return {


            titulo:
            "Servidor offline",


            mensagem:
            "Não foi possível conectar com a API.",


            status:
            null


        };


    }



    // ====================================
    // ERRO DESCONHECIDO
    // ====================================


    return {


        titulo:
        "Erro inesperado",


        mensagem:
        error.message,


        status:
        null


    };


}


export default tratarErro;