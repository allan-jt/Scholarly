import SentimentDissatisfiedIcon from "@mui/icons-material/SentimentDissatisfied";
import { Box, Typography } from "@mui/material";

const NoResultDisplay = () => (
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
        <SentimentDissatisfiedIcon color="secondary" fontSize="large" />
        <Typography color="secondary" variant="subtitle1" gutterBottom>
            {"No result found."}
            <br /> {"Please try searching with other keywords"}.
        </Typography>
    </Box>
);
export default NoResultDisplay;
