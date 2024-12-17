import { FormControl, Select, MenuItem } from "@mui/material";
import { SelectChangeEvent } from "@mui/material/Select";

interface Dict {
    [key: string]: string;
}

export const prefixList = [
    { value: "title", label: "Title" },
    { value: "author", label: "Author" },
    { value: "abstract", label: "Abstract" },
    { value: "comment", label: "Comment" },
    { value: "journal_reference", label: "Journal Reference" },
    { value: "report_number", label: "Report Number" },
    { value: "id_list", label: "arXiv Id" },
    { value: "subject_category", label: "Subject Category" },
];

export const booleanList = [
    { value: "AND", label: "AND" },
    { value: "OR", label: "OR" },
    { value: "ANDNOT", label: "AND NOT" },
];

// export const subjectList = [
//     { value: "all", label: "All" },
//     { value: "cs", label: "Computer Science" },
//     { value: "econ", label: "Economics" },
//     { value: "eess", label: "Electricial Engineering and Systems Science" },
//     { value: "math", label: "Mathematics" },
//     { value: "physics", label: "Physics" },
//     { value: "q-bio", label: "Quantitative Biology" },
//     { value: "q-fin", label: "Quantitative Finance" },
//     { value: "stat", label: "Statistics" },
// ];

export const sortByOptions = [
    { value: "relevance", label: "Relevance" },
    { value: "submittedDate", label: "Submitted Date" },
    { value: "lastUpdatedDate", label: "Updated Date" },
];

export const orderByOptions = [
    { value: "descending", label: "Descending" },
    { value: "ascending", label: "Ascending" },
];

export default function SearchMenuItems(
    id: string,
    default_val: string,
    value: string,
    items: Array<Dict>,
    handler: (event: SelectChangeEvent) => void
) {
    return (
        <FormControl variant="standard">
            <Select
                style={{ marginRight: 10 }}
                variant="standard"
                value={value}
                defaultValue={default_val}
                id={id}
                onChange={handler}
                autoWidth
            >
                {items.map((item) => (
                    <MenuItem value={item.value}>{item.label}</MenuItem>
                ))}
            </Select>
        </FormControl>
    );
}
