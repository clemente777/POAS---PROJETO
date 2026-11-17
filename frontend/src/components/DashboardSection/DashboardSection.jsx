import "./DashboardSection.css";

function DashboardSection({ titulo, children, classe = "" }) {

    return (

        <section className="dashboard-section">

            <h2>{titulo}</h2>

            <div className={`section-content ${classe}`.trim()}>

                {children}

            </div>

        </section>

    );

}

export default DashboardSection;
