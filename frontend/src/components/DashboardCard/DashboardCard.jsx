import "./DashboardCard.css";

function DashboardCard({

    titulo,

    valor,

    icone,

    cor = "#0d8297"

}) {

    return (

        <div className="dashboard-card">

            <div

                className="card-icon"

                style={{ background: cor }}

            >

                {icone}

            </div>

            <div className="card-info">

                <h3>{titulo}</h3>

                <strong>{valor}</strong>

            </div>

        </div>

    );

}

export default DashboardCard;