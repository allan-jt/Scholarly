import { useState, ChangeEvent, KeyboardEvent } from "react";
import { Paper, InputBase, IconButton, Fab } from "@mui/material";
import { Add as AddIcon, Search as SearchIcon } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import AdvancedSearch from "./SearchAdvanced";
import "../App.css";

export default function SearchBar() {
    const navigate = useNavigate();
    const [isOpen, setIsOpen] = useState<boolean>(false);
    const [query, setQuery] = useState<string>("");

    const toggleOpen = () => setIsOpen((prev) => !prev);

    const search = () => {
        const trimmedQuery = query.trim();
        if (trimmedQuery) {
            const searchParams = new URLSearchParams({
                all: trimmedQuery,
            });
            navigate({
                pathname: "/search_result",
                search: `?${searchParams.toString()}`,
            });
        }
    };

    const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
        if (event.key === "Enter") {
            event.preventDefault();
            search();
        }
    };

    // Update query state
    const handleQuery = (event: ChangeEvent<HTMLInputElement>) => {
        setQuery(event.target.value);
    };

    return (
        <>
            <div style={{ display: "flex", alignItems: "center" }}>
                <Paper
                    component="form"
                    sx={{
                        p: "2px 4px",
                        display: "flex",
                        alignItems: "center",
                        width: { xs: 350, sm: 450, md: 550, lg: 650 },
                        borderRadius: "25px",
                        backgroundColor: "#ECECEC",
                        boxShadow: "none",
                    }}
                    onSubmit={(e) => e.preventDefault()}
                >
                    <InputBase
                        sx={{
                            ml: 1,
                            flex: 1,
                            marginLeft: "20px",
                            fontWeight: "300",
                        }}
                        style={{ color: "black" }}
                        placeholder="Search from all scholarly resources"
                        autoFocus
                        disabled={isOpen}
                        value={query}
                        onChange={handleQuery}
                        onKeyDown={handleKeyDown}
                    />
                    <IconButton
                        type="button"
                        sx={{ p: "10px" }}
                        aria-label="search"
                        disabled={isOpen}
                        onClick={search}
                        color="secondary"
                    >
                        <SearchIcon />
                    </IconButton>
                </Paper>
                <Fab
                    className={`plus-icon ${isOpen ? "open" : ""}`}
                    onClick={toggleOpen}
                    color="secondary"
                    size="small"
                    aria-label="add"
                    sx={{ marginLeft: "10px", boxShadow: "none" }}
                >
                    <AddIcon style={{ color: "white" }} />
                </Fab>
            </div>
            {isOpen && <AdvancedSearch />}
        </>
    );
}
