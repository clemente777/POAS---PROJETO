import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer
} from "recharts";


function ConsultasVeterinarioChart({dados}) {


    const data = dados.consultas_semana || [];


    return (

        <ResponsiveContainer
            width="100%"
            height={250}
        >

            <BarChart data={data}>


                <XAxis 
                    dataKey="dia"
                />


                <YAxis />


                <Tooltip />


                <Bar
                    dataKey="quantidade"
                    fill="#18a999"
                />


            </BarChart>


        </ResponsiveContainer>

    );

}


export default ConsultasVeterinarioChart;