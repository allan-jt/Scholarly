import { useSearchParams } from "react-router-dom";
import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import { Paper, Typography, Backdrop, CircularProgress } from "@mui/material";
import Pagination from "@mui/material/Pagination";
import SearchDropDown from "./SearchDropDown";
import SearchResultTable, { Article } from "./SearchResultTable";
import { sortByOptions, orderByOptions } from "./SearchMenuItems";
import ErrorDisplay from "./ErrorDisplay";
// import testData from "./test_data.json";

const ITEMS_PER_PAGE = 3;

function SearchResult() {
    const api = import.meta.env.VITE_BACKEND_URL;
    const [searchParams, setSearchParams] = useSearchParams();
    const [data, setData] = useState<Article[]>([]);
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

    const fetchData = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const start = (pageNum - 1) * ITEMS_PER_PAGE + 1;
            const queryParams = new URLSearchParams(searchParams.toString());
            queryParams.set("start", start.toString());
            // queryParams.set("max_results", ITEMS_PER_PAGE.toString());
            queryParams.set("sort_by", sort_by);
            queryParams.set("sort_order", sort_order);
            const endpoint = searchParams.has("all")
                ? "/query"
                : "/query/advanced";
            const response = await axios.get(
                `${api}${endpoint}?${queryParams.toString()}`
            );
            const result = response.data.arxiv || {};
            // console.log(`${api}${endpoint}?${queryParams.toString()}`);
            // const response = testData;
            // const result = response.arxiv;
            const totalResults = result.length;
            setResultCount(totalResults);
            Array.isArray(result) ? setData(result) : setData([result]);
        } catch (e) {
            setError(
                e instanceof Error ? e.message : "An unknown error occurred."
            );
        } finally {
            setLoading(false);
        }
    }, [api, searchParams, pageNum]);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

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
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        p: 0,
                        width: { xs: "auto", sm: "auto", md: "auto" },
                        maxHeight: "90%",
                        margin: {
                            xs: "2% 3% 3% 3%",
                            sm: "2% 3% 3% 3%",
                            md: "2% 0 3% 3%",
                            lg: "2% 3% 2% 3%",
                        },
                        borderRadius: "10px",
                    }}
                >
                    <div
                        style={{
                            display: "flex",
                            flexDirection: "row",
                            alignSelf: "flex-start",
                            marginBottom: "2%",
                            width: "-webkit-fill-available",
                            justifyContent: "space-between",
                            alignItems: "center",
                        }}
                    >
                        <ResultStats />
                        <div style={{ width: "300px" }}>
                            <SearchDropDown
                                id="sort_by_search-result"
                                label="Sort By"
                                value={sort_by}
                                options={sortByOptions}
                                onChange={(value) =>
                                    handleDropdownChange("sort_by", value)
                                }
                                selectSize="small"
                            />
                            <SearchDropDown
                                id="order_by_search-result"
                                label="Order By"
                                value={sort_order}
                                options={orderByOptions}
                                onChange={(value) =>
                                    handleDropdownChange("sort_order", value)
                                }
                                selectSize="small"
                            />
                        </div>
                    </div>
                    {data.length === 0 ? (
                        <Typography variant="body1" sx={{ padding: 2 }}>
                            No results found.
                        </Typography>
                    ) : (
                        data.map((item, index) => (
                            <Paper
                                elevation={0}
                                sx={{
                                    display: "flex",
                                    flexDirection: {
                                        xs: "column",
                                        sm: "column",
                                        md: "row",
                                        lg: "row",
                                    },
                                    width: "100%",
                                }}
                                key={index}
                            >
                                <SearchResultTable
                                    key={item.id || index}
                                    id={item.id || ""}
                                    pdf={item.pdf || ""}
                                    title={item.title || "Untitled"}
                                    author={item.author || []}
                                    abstract={
                                        item.abstract || "No abstract available"
                                    }
                                    published={item.published || ""}
                                    updated={item.updated || ""}
                                    summary={
                                        item.summary || "No summary available"
                                    }
                                />
                            </Paper>
                        ))
                    )}
                    <Pagination
                        sx={{ margin: "2%" }}
                        count={Math.ceil(resultCount / ITEMS_PER_PAGE)}
                        page={pageNum}
                        onChange={handlePageChange}
                        color="secondary"
                        variant="outlined"
                        shape="rounded"
                    />
                </Paper>
            )}
        </div>
    );
}

export default SearchResult;
