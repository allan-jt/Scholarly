import { Card, CardContent, Typography, Link } from "@mui/material";

export interface Article {
    id: string;
    pdf: string;
    title: string;
    author: Author[] | Author;
    summary: Summary[];
    abstract: string;
    published: string;
    updated: string;
}

export interface Author {
    name: string;
}

export interface Summary {
    header: string;
    summary: string;
}

const SearchResultTable: React.FC<Article> = ({
    id,
    pdf,
    title,
    author,
    summary,
    abstract,
    published,
    updated,
}) => {
    // Normalize authors to always be an array
    const authorList = Array.isArray(author) ? author : [author];
    const summaries = Array.isArray(summary) ? summary : [summary];

    return (
        <>
            {/* Article Card */}
            <Card
                elevation={2}
                sx={{
                    padding: "10px",
                    marginBottom: {
                        xs: "2px",
                        sm: "2px",
                        md: "20px",
                        lg: "20px",
                    },
                    width: { xs: "100%", sm: "100%", md: "50%", lg: "50%" },
                    height: "320px",
                    borderRadius: "15px",
                }}
            >
                <CardContent>
                    {id && (
                        <Link
                            color="secondary"
                            underline="hover"
                            variant="body2"
                            fontWeight={500}
                            href={id}
                        >
                            arXiv:
                            {id.split("/").pop()}
                        </Link>
                    )}
                    {title && (
                        <Typography
                            sx={{
                                lineHeight: 1.2,
                                fontWeight: 500,
                                marginBottom: "0.8rem",
                            }}
                        >
                            {title}
                        </Typography>
                    )}

                    {authorList.length > 0 && (
                        <div>
                            <p
                                style={{
                                    fontSize: "14px",
                                    marginTop: "10px",
                                    marginBottom: 0,
                                    fontWeight: 500,
                                }}
                            >
                                Authors
                            </p>
                            <Typography
                                className="search-result-author"
                                fontSize="14px"
                                sx={{
                                    lineHeight: 1.1,
                                }}
                            >
                                {authorList.map((item) => item.name).join(", ")}
                            </Typography>
                        </div>
                    )}
                    {abstract && (
                        <div>
                            <p
                                style={{
                                    fontSize: "14px",
                                    marginTop: "10px",
                                    marginBottom: 0,
                                    fontWeight: 500,
                                }}
                            >
                                Abstract
                            </p>
                            <Typography
                                fontSize="14px"
                                className="search-result-abstract"
                            >
                                {abstract}
                            </Typography>
                        </div>
                    )}
                    {published && updated && (
                        <div>
                            <p
                                style={{
                                    fontSize: "14px",
                                    marginTop: "10px",
                                    marginBottom: 0,
                                    fontWeight: 500,
                                }}
                            >
                                Date Submitted
                            </p>
                            <Typography fontSize="14px">
                                {published.split("T")[0]} (Last Updated:{" "}
                                {updated.split("T")[0]})
                            </Typography>
                        </div>
                    )}
                </CardContent>
            </Card>

            {/* Summary Card */}
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
                        {summaries.map((item, index) => (
                            <div key={index}>
                                <p>
                                    <b>{item.header}</b>
                                </p>
                                <p style={{ margin: "0" }}>{item.summary}</p>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>
        </>
    );
};

export default SearchResultTable;
