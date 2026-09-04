import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
    Cell
} from "recharts";
import { CHART_COLORS } from "./chartColors";




function AnimaisEspecieChart({dados}) {


    const data = Array.isArray(dados?.animais_por_especie)

        ? dados.animais_por_especie

        :

        Object.entries(dados?.animais_por_especie || {})
        .map(([especie, quantidade]) => ({

            especie,
            quantidade

        }));


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


                <XAxis
                    type="number"
                />


                <YAxis
                    type="category"
                    dataKey="especie"
                    width={80}
                />


                <Tooltip />


                <Bar
                    dataKey="quantidade"
                    radius={[0,8,8,0]}
                >

                    {
                        data.map(
                            (item,index)=>(

                                <Cell
                                    key={index}
                                    fill={CHART_COLORS[index % CHART_COLORS.length]}
                                />

                            )
                        )
                    }


                </Bar>


            </BarChart>


        </ResponsiveContainer>

    );

}


export default AnimaisEspecieChart;