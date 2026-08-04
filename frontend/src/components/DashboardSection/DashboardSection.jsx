import "./DashboardSection.css";

function DashboardSection({ titulo, children }) {

    return (

        <section className="dashboard-section">

            <h2>{titulo}</h2>

            <div className="section-content">

                {children}

            </div>

        </section>

    );

}

export default DashboardSection;