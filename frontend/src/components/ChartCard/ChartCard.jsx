import "./ChartCard.css";


function ChartCard({titulo, children}){


return (

<div className="chart-card">


    <h2>
        {titulo}
    </h2>


    <div className="chart-body">

        {children}

    </div>


</div>

)


}


export default ChartCard;