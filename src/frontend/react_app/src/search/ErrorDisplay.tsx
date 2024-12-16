import ReportGmailerrorredIcon from "@mui/icons-material/ReportGmailerrorred";
import { Box, Typography } from "@mui/material";

// Reusable UI Components
const ErrorDisplay = () => (
    <Box
        sx={{
            p: 2,
            width: "40%",
            position: "fixed",
            top: "20%",
            left: "30%",
            borderRadius: "10px",
            textAlign: "center",
            backgroundColor: (theme) =>
                theme.palette.mode === "light" ? "#FAFAFE" : "#202031",
        }}
    >
        <ReportGmailerrorredIcon color="secondary" fontSize="large" />
        <Typography color="secondary" variant="subtitle1" gutterBottom>
            An error occurred! Please try searching again.
        </Typography>
    </Box>
);
export default ErrorDisplay;
