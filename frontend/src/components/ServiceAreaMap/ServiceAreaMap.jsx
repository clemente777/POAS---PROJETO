import { useMemo, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Polygon,
  Marker,
  Popup,
  useMap,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import "./ServiceAreaMap.css";

/**
 * ServiceAreaMap
 * -----------------------------------------------------------------------
 * Mapa de área de atendimento com região destacada, pontos de referência
 * e um painel de legenda. Usa a mesma paleta de marca do resto do site
 * (teal + coral, tirados da logo Petonline24h).
 *
 * Props:
 * - center: [lat, lng] — centro inicial do mapa
 * - zoom: number — zoom inicial
 * - coverageArea: [[lat, lng], ...] — polígono da área coberta
 * - points: [{ id, name, description, position: [lat, lng], type }]
 * - title / subtitle: textos do painel de legenda
 */

function createPinIcon(color, { pulse = false } = {}) {
  const pulseRing = pulse
    ? `<span class="sam-pulse" style="background:${color}"></span>`
    : "";
  const svg = `
    <div class="sam-pin-inner">
      ${pulseRing}
      <svg width="32" height="42" viewBox="0 0 34 44" xmlns="http://www.w3.org/2000/svg">
        <path d="M17 0C7.6 0 0 7.6 0 17c0 12.4 17 27 17 27s17-14.6 17-27C34 7.6 26.4 0 17 0z" fill="${color}"/>
        <circle cx="17" cy="17" r="7" fill="white"/>
      </svg>
    </div>`;
  return L.divIcon({
    html: svg,
    className: "sam-pin",
    iconSize: [32, 42],
    iconAnchor: [16, 42],
    popupAnchor: [0, -36],
  });
}

const CLINIC_PIN = createPinIcon("#F2615D", { pulse: true }); // accent (coral)
const POINT_PIN = createPinIcon("#0E7C93"); // brand (teal)

function FitBounds({ coverageArea }) {
  const map = useMap();
  useMemo(() => {
    if (coverageArea?.length) {
      const bounds = L.latLngBounds(coverageArea);
      map.fitBounds(bounds, { padding: [40, 40] });
    }
  }, [coverageArea, map]);
  return null;
}

export default function ServiceAreaMap({
  center = [-5.7945, -35.211],
  zoom = 12,
  coverageArea = [],
  points = [],
  title = "Área de atendimento",
  subtitle = "Cobertura disponível na região destacada",
  autoFit = true,
}) {
  const [activePoint, setActivePoint] = useState(null);

  return (
    <div className="sam-wrapper">
      <div className="sam-panel">
        <span className="sam-eyebrow">Cobertura</span>
        <h3 className="sam-title">{title}</h3>
        <p className="sam-subtitle">{subtitle}</p>

        <div className="sam-legend">
          <div className="sam-legend-item">
            <span className="sam-dot sam-dot--area" />
            Região atendida
          </div>
          <div className="sam-legend-item">
            <span className="sam-dot sam-dot--point" />
            Unidades parceiras
          </div>
        </div>

        {points.length > 0 && (
          <ul className="sam-point-list">
            {points.map((p) => (
              <li
                key={p.id}
                className={`sam-point-item ${
                  activePoint === p.id ? "is-active" : ""
                }`}
                onClick={() => setActivePoint(p.id)}
              >
                {p.name}
              </li>
            ))}
          </ul>
        )}
      </div>

      <div className="sam-map-frame">
        <MapContainer
          center={center}
          zoom={zoom}
          scrollWheelZoom={false}
          className="sam-map"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {coverageArea.length > 0 && (
            <>
              <Polygon
                positions={coverageArea}
                pathOptions={{
                  color: "#0E7C93",
                  weight: 2,
                  fillColor: "#0E7C93",
                  fillOpacity: 0.12,
                }}
              />
              {autoFit && <FitBounds coverageArea={coverageArea} />}
            </>
          )}

          {points.map((p) => (
            <Marker
              key={p.id}
              position={p.position}
              icon={p.type === "clinic" ? CLINIC_PIN : POINT_PIN}
              eventHandlers={{
                click: () => setActivePoint(p.id),
              }}
            >
              <Popup>
                <strong>{p.name}</strong>
                {p.description && <p>{p.description}</p>}
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
