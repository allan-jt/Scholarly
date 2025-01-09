import { useSearchParams } from "react-router-dom";
import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import {
    Button,
    Paper,
    Typography,
    Backdrop,
    CircularProgress,
    Box,
    Card,
} from "@mui/material";
import Pagination from "@mui/material/Pagination";
import { useTheme } from "@mui/material/styles";
import SearchDropDown from "./SearchDropDown";
import SearchResultTable, { Article } from "./SearchResultTable";
import { sortByOptions, orderByOptions } from "./SearchMenuItems";
import ErrorDisplay from "./ErrorDisplay";
import Summary, { SummaryItem } from "./Summary";

const ITEMS_PER_PAGE = 5;

function SearchResult() {
    const api = import.meta.env.VITE_BACKEND_URL;
    const theme = useTheme();

    const [searchParams, setSearchParams] = useSearchParams();
    const [data, setData] = useState<Article[]>([]);
    const [summaryRes, setSummaryRes] = useState<SummaryItem[]>([]);
    const [summaryTitle, setSummaryTitle] = useState("");
    const [summaryStat, setSummaryStat] = useState("ready"); // "ready", "generating", "done", "error"
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [resultCount, setResultCount] = useState(0);
    const [pageNum, setPageNum] = useState(1);

    const sort_by = searchParams.get("sort_by") || "relevance";
    const sort_order = searchParams.get("sort_order") || "descending";

    const updateSearchParams = useCallback(
        (key: string, value: string) => {
            const updatedParams = new URLSearchParams(searchParams.toString());
            updatedParams.set(key, value);
            setSearchParams(updatedParams);
        },
        [searchParams, setSearchParams]
    );

    const handleCardClick = async (pdf_link: string, title: string) => {
        if (!pdf_link) return;

        try {
            // Scroll to top for sm,xs screens
            if (window.innerWidth < theme.breakpoints.values.md) {
                window.scrollTo({ top: 0, behavior: "smooth" });
            }
            setSummaryStat("generating");
            setSummaryTitle(title);
            console.log(`${api}/query/summarize?pdf_link=${pdf_link}`);
            const response = await axios.get(
                `${api}/query/summarize?pdf_link=${pdf_link}`
            );
            setSummaryRes(response.data.summary || []);
            setSummaryStat("done");
        } catch (error) {
            console.error("Error fetching summary:", error);
            setSummaryStat("error");
        }
    };

    const fetchData = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const start = (pageNum - 1) * ITEMS_PER_PAGE + 1;
            const queryParams = new URLSearchParams(searchParams.toString());
            queryParams.set("start", start.toString());
            queryParams.set("max_results", ITEMS_PER_PAGE.toString());
            queryParams.set("sort_by", sort_by);
            queryParams.set("sort_order", sort_order);

            const endpoint = searchParams.has("all")
                ? "/query"
                : "/query/advanced";
            const response = await axios.get(
                `${api}${endpoint}?${queryParams.toString()}`
            );
            const result = response.data.arxiv || [];
            const count = response.data.totalResults || 0;
            setResultCount(count);
            setData(Array.isArray(result) ? result : [result]);
        } catch (e) {
            setError(
                e instanceof Error ? e.message : "An unknown error occurred."
            );
        } finally {
            setLoading(false);
        }
    }, [api, searchParams, pageNum, sort_by, sort_order]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    // Handlers for dropdown and pagination
    const handleDropdownChange = (name: string, value: string) =>
        updateSearchParams(name, value);

    const handlePageChange = (_: React.ChangeEvent<unknown>, value: number) => {
        setPageNum(value);
        window.scrollTo({ top: 0, behavior: "smooth" });
    };

    const ResultStats = () => (
        <Typography
            fontWeight={500}
            color="secondary"
            variant="subtitle2"
            sx={{ width: "40%", marginRight: "1%" }}
        >
            {`Showing ${(pageNum - 1) * ITEMS_PER_PAGE + 1} to ${Math.min(
                pageNum * ITEMS_PER_PAGE,
                resultCount
            )} of ${resultCount} results`}
        </Typography>
    );

    if (error && !loading) return <ErrorDisplay />;

    return (
        <div
            className="content"
            style={{ display: "flex", flexDirection: "column" }}
        >
            <Backdrop
                sx={{
                    color: "#fff",
                    zIndex: (theme) => theme.zIndex.drawer + 1,
                }}
                open={loading}
            >
                <CircularProgress color="inherit" />
            </Backdrop>
            {!loading && (
                <Paper
                    component="section"
                    elevation={0}
                    sx={{
                        padding: { xs: "6%", md: "3%" },
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        borderRadius: "10px",
                    }}
                >
                    <Box
                        sx={{
                            display: "flex",
                            flexDirection: { xs: "column", md: "row" },
                            width: "100%",
                        }}
                    >
                        <Summary
                            title={summaryTitle}
                            summary={summaryRes}
                            status={summaryStat}
                        />
                        <Box sx={{ width: { xs: "100%", md: "47%" } }}>
                            <Box
                                sx={{
                                    display: "flex",
                                    flexDirection: "row",
                                    justifyContent: "space-between",
                                    alignItems: "flex-start",
                                    width: "100%",
                                    marginBottom: "20px",
                                }}
                            >
                                <ResultStats />
                                <Box sx={{ width: "300px" }}>
                                    <SearchDropDown
                                        id="sort_by_search-result"
                                        label="Sort By"
                                        value={sort_by}
                                        options={sortByOptions}
                                        onChange={(value) =>
                                            handleDropdownChange(
                                                "sort_by",
                                                value
                                            )
                                        }
                                        selectSize="small"
                                    />
                                    <SearchDropDown
                                        id="order_by_search-result"
                                        label="Order By"
                                        value={sort_order}
                                        options={orderByOptions}
                                        onChange={(value) =>
                                            handleDropdownChange(
                                                "sort_order",
                                                value
                                            )
                                        }
                                        selectSize="small"
                                    />
                                </Box>
                            </Box>
                            {data.length === 0 ? (
                                <Typography variant="body1" sx={{ padding: 2 }}>
                                    No results found.
                                </Typography>
                            ) : (
                                data.map((item, index) => (
                                    <Card
                                        key={index}
                                        elevation={2}
                                        sx={{
                                            padding: "10px",
                                            marginBottom: "20px",
                                            borderRadius: "15px",
                                            ":hover": {
                                                boxShadow:
                                                    theme.palette.mode ===
                                                    "light"
                                                        ? "0 0 10px rgba(100, 100, 100, 0.5)"
                                                        : "0 0 15px rgba(255,255,255,.5)",
                                            },
                                        }}
                                    >
                                        <SearchResultTable
                                            id={item.id || ""}
                                            pdf={item.pdf || ""}
                                            title={item.title || "Untitled"}
                                            author={item.author || []}
                                            abstract={
                                                item.abstract ||
                                                "No abstract available"
                                            }
                                            published={item.published || ""}
                                            updated={item.updated || ""}
                                        />
                                        <Button
                                            className="search-button"
                                            variant="contained"
                                            color="secondary"
                                            sx={{
                                                margin: "0 16px 16px 16px",
                                                color: "white",
                                            }}
                                            onClick={() =>
                                                handleCardClick(
                                                    item.pdf,
                                                    item.title
                                                )
                                            }
                                        >
                                            Summarize
                                        </Button>
                                    </Card>
                                ))
                            )}
                            <Pagination
                                sx={{
                                    margin: "20px",
                                    display: "flex",
                                    justifyContent: "center",
                                }}
                                count={Math.ceil(resultCount / ITEMS_PER_PAGE)}
                                page={pageNum}
                                onChange={handlePageChange}
                                color="secondary"
                                variant="outlined"
                                shape="rounded"
                            />
                        </Box>
                    </Box>
                </Paper>
            )}
        </div>
    );
}

export default SearchResult;
