import { Typography } from "@mui/material";
import Wave from "./Wave";
import SearchBar from "./SearchBar";
import "../App.css";

function Search() {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                overflow: "hidden",
            }}
        >
            <Typography
                className="gradient-text"
                sx={{
                    fontSize: "60px",
                    fontWeight: 700,
                    margin: "150px 30px 30px 30px",
                }}
            >
                Scholarly
            </Typography>
            <SearchBar />
            <Wave />
        </div>
    );
}

export default Search;
