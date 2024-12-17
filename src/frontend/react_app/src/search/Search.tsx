import { Typography } from "@mui/material";
import Wave from "./Wave";
import SearchBar from "./SearchBar";
import "../App.css";

function Search() {
    return (
        <div
            className="content"
            style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
            }}
        >
            <Typography
                className="gradient-text"
                sx={{
                    fontSize: "60px",
                    fontWeight: 700,
                    margin: "80px 30px 30px 30px",
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
