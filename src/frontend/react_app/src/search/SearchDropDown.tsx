import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

interface SearchDropDownProps {
    id: string;
    label: string;
    value: string;
    options: { value: string; label: string }[];
    onChange: (value: string) => void;
    selectSize: string;
}

const SearchDropDown: React.FC<SearchDropDownProps> = ({
    id,
    label,
    value,
    options,
    onChange,
    selectSize,
}) => {
    return (
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
            <InputLabel id={`${id}-label`}>{label}</InputLabel>
            <Select
                id={id}
                labelId={`${id}-label`}
                value={value}
                onChange={(e) => onChange(e.target.value)}
                variant="standard"
                sx={{ fontSize: selectSize }}
            >
                {options.map(({ value, label }) => (
                    <MenuItem
                        key={value}
                        value={value}
                        sx={{ fontSize: selectSize }}
                    >
                        {label}
                    </MenuItem>
                ))}
            </Select>
        </FormControl>
    );
};

export default SearchDropDown;
