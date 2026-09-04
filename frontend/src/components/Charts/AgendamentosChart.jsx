import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    CartesianGrid
} from "recharts";


function AgendamentosSemanaChart({dados}) {


    const data = (dados?.agendamentos_semana || []).map(item => {

        const data = new Date(item.dia + "T00:00:00");

        return {

            dia: data.toLocaleDateString("pt-BR", {
                weekday: "long"
            }),

            quantidade: item.quantidade

        };

    });

    if(data.length === 0){

        return (

            <div>
                Nenhum agendamento disponível
            </div>

        );

    }


    return (

        <ResponsiveContainer
            width="100%"
            height={250}
        >

            <BarChart
                data={data}
                layout="vertical"
                margin={{
                    left:30,
                    right:20
                }}
            >


                <CartesianGrid
                    strokeDasharray="3 3"
                />


                <XAxis
                    type="number"
                />


                <YAxis
                    type="category"
                    dataKey="dia"
                    width={70}
                />


                <Tooltip />


                <Bar

                    dataKey="quantidade"

                    fill="#0E7C93"

                    radius={[0,8,8,0]}

                />


            </BarChart>


        </ResponsiveContainer>

    );

}


export default AgendamentosSemanaChart;