import { Card, CardContent, Typography } from "@mui/material";
import { Summary } from "./SearchResultTable";
const SummaryCard: React.FC<Summary> = ({ header, summary }) => {
    console.log(header);
    return (
        <>
            <Card
                elevation={2}
                sx={{
                    width: { xs: "100%", sm: "100%", md: "50%", lg: "50%" },
                    height: "320px",
                    marginLeft: {
                        xs: "0",
                        sm: "0",
                        md: "2px",
                        lg: "2px",
                    },
                    marginBottom: {
                        xs: "20px",
                        sm: "20px",
                        md: "20px",
                        lg: "20px",
                    },
                    padding: "10px",
                    borderRadius: "15px",
                    backgroundColor: (theme) =>
                        theme.palette.mode === "light" ? "#FAFAFE" : "#202031",
                }}
            >
                <CardContent>
                    <Typography
                        color="secondary"
                        variant="subtitle2"
                        fontWeight={500}
                        marginBottom={"10px"}
                    >
                        Summary
                    </Typography>
                    <div
                        style={{
                            overflow: "auto",
                            height: "240px",
                            fontSize: "14px",
                        }}
                    >
                        <p>
                            <b>{header}</b>
                        </p>
                        <p style={{ margin: "0" }}>{summary}</p>
                    </div>
                </CardContent>
            </Card>
        </>
    );
};
export default SummaryCard;
