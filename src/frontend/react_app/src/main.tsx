import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App";

createRoot(document.getElementById("root")!).render(
    // Commented out strict mode to avoid rendering twice
    // <StrictMode>
    <App />
    // </StrictMode>
);
