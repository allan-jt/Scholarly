import { useSearchParams } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import { Box, Paper, Typography } from "@mui/material";
import Backdrop from "@mui/material/Backdrop";
import CircularProgress from "@mui/material/CircularProgress";
import ReportGmailerrorredIcon from "@mui/icons-material/ReportGmailerrorred";
import SearchResultTable, { Article } from "./SearchResultTable";

export default function SearchResult() {
    const api = import.meta.env.VITE_BACKEND_URL;
    const [searchParams] = useSearchParams();
    const [data, setData] = useState<Article[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchData = async () => {
            setLoading(true);
            setError("");
            try {
                // Determine endpoint based on param length
                const endpoint =
                    searchParams.toString().split("&").length > 3
                        ? "/query/advanced"
                        : "/query";
                const queryParams = searchParams.toString();
                const response = await axios.get(
                    `${api}${endpoint}?${queryParams}`
                );
                const result = response.data.arxiv.feed.entry || [];
                if (Array.isArray(result)) {
                    setData(result);
                } else {
                    setData([result]);
                }
            } catch (e) {
                setError(
                    e instanceof Error ? e.message : "An unknown error occurred"
                );
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [searchParams, api]);

    if (error) {
        console.log(error);
        return (
            <>
                <Box
                    component="section"
                    sx={{
                        p: 2,
                        width: "40%",
                        position: "fixed",
                        top: "20%",
                        left: "30%",
                        borderRadius: "10px",
                        textAlign: "center",
                        backgroundColor: (theme) =>
                            theme.palette.mode === "light"
                                ? "#FAFAFE"
                                : "#202031",
                    }}
                >
                    <ReportGmailerrorredIcon
                        color="secondary"
                        fontSize="large"
                    />
                    <Typography
                        color="secondary"
                        variant="subtitle1"
                        gutterBottom
                    >
                        An error occured! Please try searching again.
                    </Typography>
                </Box>
            </>
        );
    }

    return (
        <div style={{ display: "flex" }}>
            <Backdrop
                sx={(theme) => ({
                    color: "#fff",
                    zIndex: theme.zIndex.drawer + 1,
                })}
                open={loading}
            >
                <CircularProgress color="inherit" />
            </Backdrop>

            <Box
                component="section"
                sx={{
                    p: 2,
                    width: { xs: "76%", sm: "76%", md: "40%", lg: "40%" },
                    height: "80vh",
                    marginTop: { xs: "2%", sm: "2%", md: "2%", lg: "2%" },
                    marginLeft: { xs: "0%", sm: "0%", md: "2%", lg: "2%" },
                    padding: "2%",
                    position: "fixed",
                    left: { xs: "12%", sm: "12%", md: "55%", lg: "55%" },
                    zIndex: { sm: 100, md: -100 },
                    borderRadius: "10px",
                    backgroundColor: (theme) =>
                        theme.palette.mode === "light" ? "#FAFAFE" : "#202031",
                }}
            >
                {!loading && (
                    <Typography
                        color="secondary"
                        variant="body1"
                        fontWeight={500}
                        textAlign="center"
                        lineHeight="70vh"
                        gutterBottom
                    >
                        Select an article to view the summary.
                    </Typography>
                )}
            </Box>
            <Paper
                component="section"
                elevation={0}
                sx={{
                    p: 2,
                    width: { xs: "100%", sm: "94%", md: "52%", lg: "52%" },
                    maxHeight: "90%",
                    margin: "2% 0 3% 3%",
                    padding: 0,
                    borderRadius: "10px",
                }}
            >
                {!loading && Array.isArray(data) && data.length === 0 ? (
                    <Typography variant="body1" sx={{ padding: 2 }}>
                        No results found.
                    </Typography>
                ) : (
                    Array.isArray(data) &&
                    data.length > 0 &&
                    data.map((item, index) => {
                        const articleData: Article = {
                            id: item.id || "",
                            title: item.title || "Untitled",
                            author: item.author || [],
                            summary: item.summary || "No summary available",
                            published: item.published || "",
                            updated: item.updated || "",
                        };
                        return (
                            <SearchResultTable key={index} {...articleData} />
                        );
                    })
                )}
            </Paper>
        </div>
    );
}
