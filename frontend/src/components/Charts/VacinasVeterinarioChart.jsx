import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";


function VacinasVeterinarioChart({dados}) {


    const data = [

        {
            nome:"Aplicadas",
            quantidade:
                dados.vacinas_aplicadas || 0
        },

        {
            nome:"Próximas doses",
            quantidade:
                dados.proximas_doses || 0
        }

    ];



    return (

        <ResponsiveContainer
            width="100%"
            height={250}
        >

            <BarChart data={data}>


                <XAxis
                    dataKey="nome"
                />


                <YAxis />


                <Tooltip />


                <Bar
                    dataKey="quantidade"
                    fill="#ff5b91"
                />


            </BarChart>

        </ResponsiveContainer>

    );

}


export default VacinasVeterinarioChart;