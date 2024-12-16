import { useState } from "react";
import { Paper, TextField, Typography, Button } from "@mui/material";
import { useNavigate } from "react-router-dom";
import {
    prefixList,
    booleanList,
    sortByOptions,
    orderByOptions,
} from "./SearchMenuItems";
import SearchDropDown from "./SearchDropDown";
import "../App.css";

export default function AdvancedSearch() {
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useState({
        subject: "all",
        prefix1: "title",
        keyword1: "",
        prefix2: "title",
        keyword2: "",
        operator: "AND",
        sortBy: "relevance",
        orderBy: "descending",
    });
    const [error, setError] = useState(false);

    const handleChange = (name: string, value: string) => {
        setSearchParams((prevState) => ({
            ...prevState,
            [name]: value,
        }));
    };

    const search = (event: React.FormEvent) => {
        event.preventDefault(); // Prevent default form submission behavior
        const {
            keyword1,
            keyword2,
            prefix1,
            prefix2,
            operator,
            orderBy,
            sortBy,
        } = searchParams;
        const searchParamsObject = new URLSearchParams([
            ["sort_order", orderBy],
            ["sort_by", sortBy],
        ]);
        if (keyword1.trim() === "") {
            setError(true); // Set error if keyword1 is empty
            return; // Prevent search if keyword1 is empty
        }
        setError(false);
        if (keyword1.trim()) {
            searchParamsObject.append(prefix1, keyword1.trim());
        }
        if (keyword2.trim()) {
            searchParamsObject.append("boolean_operator", operator);
            searchParamsObject.append(prefix2, keyword2.trim());
        }
        navigate({
            pathname: "/search_result",
            search: `?${searchParamsObject.toString()}`,
        });
    };

    return (
        <div>
            <Paper
                elevation={5}
                component="form"
                sx={{
                    width: { xs: 350, sm: 450, md: 550, lg: 650 },
                    padding: "20px",
                }}
                className="advSearch"
                onSubmit={search}
            >
                <Typography color="secondary" variant="h6" gutterBottom>
                    <b>Advanced Search</b>
                </Typography>

                <div className="row">
                    <SearchDropDown
                        id="adv-search-prefix-1"
                        label="Prefix"
                        value={searchParams.prefix1}
                        options={prefixList}
                        onChange={(value) => handleChange("prefix1", value)}
                        selectSize="medium"
                    />
                    <TextField
                        sx={{ flex: "auto" }}
                        variant="standard"
                        placeholder="Search term..."
                        value={searchParams.keyword1}
                        onChange={(e) =>
                            handleChange("keyword1", e.target.value)
                        }
                        error={error} // Show error if keyword1 is empty
                        helperText={error ? "This field is required" : ""} // Display error message
                    />
                </div>

                <div className="row">
                    <SearchDropDown
                        id="adv-search-boolean"
                        label="Operator"
                        value={searchParams.operator}
                        options={booleanList}
                        onChange={(value) => handleChange("operator", value)}
                        selectSize="medium"
                    />
                    <SearchDropDown
                        id="adv-search-prefix-2"
                        label="Prefix"
                        value={searchParams.prefix2}
                        options={prefixList}
                        onChange={(value) => handleChange("prefix2", value)}
                        selectSize="medium"
                    />
                    <TextField
                        sx={{ flex: "auto" }}
                        variant="standard"
                        placeholder="Search term..."
                        value={searchParams.keyword2}
                        onChange={(e) =>
                            handleChange("keyword2", e.target.value)
                        }
                    />
                </div>

                <div className="row">
                    <SearchDropDown
                        id="select-sortby"
                        label="Sort By"
                        value={searchParams.sortBy}
                        options={sortByOptions}
                        onChange={(value) => handleChange("sortBy", value)}
                        selectSize="medium"
                    />
                    <SearchDropDown
                        id="select-orderby"
                        label="Order By"
                        value={searchParams.orderBy}
                        options={orderByOptions}
                        onChange={(value) => handleChange("orderBy", value)}
                        selectSize="medium"
                    />
                </div>

                <Button
                    type="submit"
                    className="search-button"
                    variant="contained"
                    color="secondary"
                    sx={{ mt: 2 }}
                >
                    Search
                </Button>
            </Paper>
        </div>
    );
}
