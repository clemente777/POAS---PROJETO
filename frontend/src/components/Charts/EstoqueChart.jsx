import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Cell
} from "recharts";

const CORES = [
    "#18a999",
    "#ffb703",
    "#ff5b91"
];

function EstoqueChart({dados}) {


    const data = [

        {
            nome:"Normal",
            quantidade:
            dados.produtos - dados.estoque_baixo - dados.produtos_sem_estoque
        },

        {
            nome:"Baixo",
            quantidade:dados.estoque_baixo
        },

        {
            nome:"Sem estoque",
            quantidade:dados.produtos_sem_estoque
        }

    ];


    return (


            <ResponsiveContainer 
                width="100%" 
                height={300}
            >

                <BarChart data={data}>


                    <XAxis 
                        dataKey="nome"
                    />

                    <YAxis/>

                    <Tooltip/>


                    <Bar
                        dataKey="quantidade"
                    >
                    {
                        data.map(
                            (item,index)=>(

                                <Cell
                                    key={index}
                                    fill={CORES[index]}
                                />

                            )
                        )
                    }

                    </Bar>

                </BarChart>

            </ResponsiveContainer>




    );

}


export default EstoqueChart;