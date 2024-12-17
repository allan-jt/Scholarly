import { useState } from "react";
import {
    Paper,
    Select,
    MenuItem,
    TextField,
    Typography,
    Button,
    InputLabel,
    FormControl,
    // FormHelperText,
} from "@mui/material";
import { useNavigate } from "react-router-dom";
import { prefixList, booleanList } from "./SearchMenuItems";
import "../App.css";

// Constants for Sort and Order By options
const sortByOptions = [
    { value: "relevance", label: "Relevance" },
    { value: "submittedDate", label: "Submitted Date" },
    { value: "lastUpdatedDate", label: "Updated Date" },
];

const orderByOptions = [
    { value: "descending", label: "Descending" },
    { value: "ascending", label: "Ascending" },
];

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
    const renderDropdown = (
        id: string,
        label: string,
        value: string,
        options: { value: string; label: string }[],
        onChange: (value: string) => void
    ) => (
        <FormControl
            variant="standard"
            sx={
                label === "Sort By"
                    ? { width: "49%", marginRight: "1%" }
                    : label === "Order By"
                    ? { width: "49%", marginLeft: "1%" }
                    : { width: "auto", marginRight: "2%" }
            }
        >
            {(label === "Sort By" || label === "Order By") && (
                <InputLabel id={`${id}-label`}>{label}</InputLabel>
            )}
            <Select
                id={id}
                labelId={`${id}-label`}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                variant="standard"
            >
                {options.map(({ value, label }) => (
                    <MenuItem key={value} value={value}>
                        {label}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
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
            ["start", "0"],
            ["max_results", "10"],
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

                {/* <div className="row">
                    <Typography sx={{ mr: 2 }}>Search In</Typography>
                    {renderDropdown(
                        "adv-search-subject",
                        "Subject",
                        searchParams.subject,
                        subjectList,
                        (value) => handleChange("subject", value)
                    )}
                </div> */}

                <div className="row">
                    {renderDropdown(
                        `adv-search-prefix-1`,
                        "Prefix",
                        searchParams.prefix1,
                        prefixList,
                        (value) => handleChange("prefix1", value)
                    )}
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
                    {renderDropdown(
                        `adv-search-boolean`,
                        "Operator",
                        searchParams.operator,
                        booleanList,
                        (value) => handleChange("operator", value)
                    )}
                    {renderDropdown(
                        `adv-search-prefix-2`,
                        "Prefix",
                        searchParams.prefix2,
                        prefixList,
                        (value) => handleChange("prefix2", value)
                    )}
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
                    {renderDropdown(
                        "select-sortby",
                        "Sort By",
                        searchParams.sortBy,
                        sortByOptions,
                        (value) => handleChange("sortBy", value)
                    )}
                    {renderDropdown(
                        "select-orderby",
                        "Order By",
                        searchParams.orderBy,
                        orderByOptions,
                        (value) => handleChange("orderBy", value)
                    )}
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
