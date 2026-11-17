/*
|--------------------------------------------------------------------------
| Arquivo: vite.config.js
| Projeto: Petonline24h
|--------------------------------------------------------------------------
|
| Finalidade:
| Configurar o Vite, ferramenta responsável pelo ambiente de
| desenvolvimento e pela compilação do frontend para produção.
|
| Responsabilidades:
| - Definir as configurações do ambiente Vite.
| - Integrar o React ao processo de desenvolvimento.
| - Habilitar o processamento de componentes JSX.
| - Disponibilizar os recursos necessários para a compilação.
|
| Tecnologia:
| - Vite: ferramenta de desenvolvimento e build.
| - @vitejs/plugin-react: plugin de integração com React.
|
|--------------------------------------------------------------------------
*/

// Importa a função responsável por definir a configuração do Vite.
import { defineConfig } from 'vite'

// Importa o plugin responsável pela integração com React.
import react from '@vitejs/plugin-react'

/*
|--------------------------------------------------------------------------
| CONFIGURAÇÃO PRINCIPAL DO VITE
|--------------------------------------------------------------------------
|
| A função defineConfig organiza as configurações do projeto.
|
| A propriedade plugins registra os plugins utilizados durante
| o desenvolvimento e a compilação.
|
| O plugin react habilita os recursos necessários para trabalhar
| com componentes React e arquivos JSX.
|
*/

export default defineConfig({
  plugins: [react()],

  // host: true libera o acesso pela rede local (ex.: celular no mesmo Wi-Fi).
  server: {
    host: true,
    port: 5173,
  },
})
