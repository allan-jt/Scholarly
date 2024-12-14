import GitHubIcon from "@mui/icons-material/GitHub";
import "../App.css";

export default function Wave() {
    return (
        <footer>
            <div className="waves">
                <div className="wave" id="wave1"></div>
                <div className="wave" id="wave2"></div>
                <div className="wave" id="wave3"></div>
                <div className="wave" id="wave4"></div>
            </div>
            <ul className="social-icons">
                <li>
                    <a href="/">
                        <GitHubIcon fontSize="large" />
                    </a>
                </li>
            </ul>
        </footer>
    );
}
