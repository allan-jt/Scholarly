import { Card, CardContent, Typography, Link } from "@mui/material";

export interface Article {
    id: string;
    title: string;
    author: Author[] | Author;
    summary: string;
    published: string;
    updated: string;
}

export interface Author {
    name: string;
}

const SearchResultTable: React.FC<Article> = ({
    id,
    title,
    summary,
    author,
    published,
    updated,
}) => {
    // Normalize authors to always be an array
    const authorList = Array.isArray(author) ? author : [author];

    return (
        <Card elevation={1} sx={{ padding: "10px", marginBottom: "10px" }}>
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
                            fontSize="14px"
                            sx={{
                                lineHeight: 1.1,
                            }}
                        >
                            {authorList.map(
                                (item, index) =>
                                    `${item.name}${
                                        index + 1 === authorList.length
                                            ? ""
                                            : ", "
                                    }`
                            )}
                        </Typography>
                    </div>
                )}
                {summary && (
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
                            {summary}
                        </Typography>
                    </div>
                )}
                {published && (
                    <div>
                        <p
                            style={{
                                fontSize: "14px",
                                marginTop: "10px",
                                marginBottom: 0,
                                fontWeight: 500,
                            }}
                        >
                            Date Published
                        </p>
                        <Typography fontSize="14px">
                            {published.split("T")[0]} (Last Updated:{" "}
                            {updated.split("T")[0]})
                        </Typography>
                    </div>
                )}
            </CardContent>
        </Card>
    );
};

export default SearchResultTable;
