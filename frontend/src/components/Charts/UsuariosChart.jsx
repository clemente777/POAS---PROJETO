import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend
} from "recharts";
import { CHART_COLORS } from "./chartColors";


function UsuariosChart({dados}) {


    const data = [
        {
            name:"Administradores",
            value:dados.administradores
        },
        {
            name:"Veterinários",
            value:dados.veterinarios
        },
        {
            name:"Clientes",
            value:dados.clientes_sistema
        }
    ];


    return (

        <PieChart width={350} height={300}>

            <Pie

                data={data}

                dataKey="value"

                nameKey="name"

                cx="50%"

                cy="50%"

                outerRadius={100}

            >

                {
                    data.map(
                        (entry,index)=>(

                            <Cell
                                key={index}
                                fill={CHART_COLORS[index]}
                            />

                        )
                    )
                }

            </Pie>

            <Tooltip />

            <Legend />

        </PieChart>

    );

}

export default UsuariosChart;