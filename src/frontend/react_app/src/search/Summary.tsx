import {
    Box,
    Card,
    CardContent,
    Typography,
    LinearProgress,
} from "@mui/material";
import Markdown from "react-markdown";

export interface SummaryItem {
    header: string;
    summary: string;
}

export interface SummaryProp {
    title: string;
    summary: SummaryItem[];
    status: string;
}

const GeneratingStatus: React.FC<{ status: string }> = ({ status }) => (
    <CardContent>
        <Typography
            color="secondary"
            variant="subtitle2"
            fontWeight={500}
            sx={{ margin: "16px 0" }}
        >
            {status === "error"
                ? "Error generating the summary. Please try again."
                : status === "generating"
                ? "Generating summary."
                : "Select a paper to generate summary."}
        </Typography>
        {status === "generating" && (
            <LinearProgress color="secondary" sx={{ margin: "16px 0" }} />
        )}
    </CardContent>
);

const SummaryContent: React.FC<{ title: string; summary: SummaryItem[] }> = ({
    title,
    summary,
}) => (
    <CardContent>
        <Typography color="secondary" variant="subtitle2" fontWeight={500}>
            Summary
        </Typography>
        <Box
            sx={{
                overflow: "auto",
                maxHeight: { xs: "300px", md: "630px" },
                fontSize: "14px",
            }}
        >
            <Typography variant="body1" fontWeight={600} marginBottom={1}>
                {title}
            </Typography>
            {summary.map((item, index) => (
                <div key={index} style={{ marginBottom: "10px" }}>
                    <Typography variant="subtitle2" fontWeight={600}>
                        {item.header}
                    </Typography>
                    <Markdown>{item.summary}</Markdown>
                </div>
            ))}
        </Box>
    </CardContent>
);

const Summary: React.FC<SummaryProp> = ({ summary = [], status, title }) => {
    const isDone = status === "done";

    return (
        <Card
            elevation={2}
            sx={{
                position: { xs: "block", md: "fixed" },
                width: { xs: "100%", md: "46%" },
                // height: "-webkit-fill-available",
                left: { xs: "0", md: "51%" },
                padding: "10px",
                marginBottom: "40px",
                borderRadius: "15px",
                backgroundColor: (theme) =>
                    theme.palette.mode === "light" ? "#FAFAFE" : "#202031",
            }}
        >
            {isDone ? (
                <SummaryContent title={title} summary={summary} />
            ) : (
                <GeneratingStatus status={status} />
            )}
        </Card>
    );
};

export default Summary;
