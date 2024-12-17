import Pagination from "@mui/material/Pagination";
import Stack from "@mui/material/Stack";

export default function BasicPagination(pages: number) {
    return (
        <Stack spacing={2}>
            <Pagination count={pages} color="secondary" />
        </Stack>
    );
}
