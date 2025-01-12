import GitHubIcon from "@mui/icons-material/GitHub";
import "../App.css";
import lightWave from "../assets/lightWave.png";
import darkWave from "../assets/darkWave.png";
import { CSSProperties } from "react";

export default function Wave() {
    const savedTheme =
        typeof window !== "undefined"
            ? localStorage.getItem("theme") || "light"
            : "light";
    const waveImg = savedTheme === "light" ? lightWave : darkWave;
    const waveColor = savedTheme === "light" ? "#36beff" : "#016391";

    const waveStyles: CSSProperties = {
        backgroundRepeat: "repeat-x",
        backgroundSize: "1000px 100px",
    };

    const waves = ["wave1", "wave2", "wave3", "wave4"];
    return (
        <footer style={{ background: waveColor }}>
            <div>
                {waves.map((item, index) => (
                    <div
                        key={index}
                        className="wave"
                        id={item}
                        style={{
                            backgroundImage: `url(${waveImg})`,
                            ...waveStyles,
                        }}
                    ></div>
                ))}
            </div>
            <ul className="social-icons">
                <li>
                    <a href="https://github.com/allan-jt/Scholarly">
                        <GitHubIcon fontSize="large" />
                    </a>
                </li>
            </ul>
        </footer>
    );
}
