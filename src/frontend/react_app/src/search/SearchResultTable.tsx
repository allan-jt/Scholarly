import { CardContent, Typography, Link, Box } from "@mui/material";

export interface Article {
    id: string;
    pdf: string;
    title: string;
    author: Author[] | Author;
    abstract: string;
    published: string;
    updated?: string;
}

export interface Author {
    name: string;
}

const SearchResultTable: React.FC<Article> = ({
    id,
    title,
    author,
    abstract,
    published,
    updated,
}) => {
    const authorList = Array.isArray(author) ? author : [author];
    const formatDate = (date: string) => date.split("T")[0];

    const sectionHeadingStyle = {
        fontSize: "14px",
        marginTop: "10px",
        marginBottom: 0,
        fontWeight: 500,
    };

    return (
        <CardContent>
            {id && (
                <Link
                    color="secondary"
                    underline="hover"
                    variant="body2"
                    fontWeight={500}
                    href={id}
                >
                    arXiv: {id.split("/").pop()}
                </Link>
            )}

            <Box sx={{ overflow: "auto", maxHeight: "255px" }}>
                {title && (
                    <Typography
                        className="search-result-title"
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
                    <Box>
                        <Typography component="p" sx={sectionHeadingStyle}>
                            Authors
                        </Typography>
                        <Typography
                            className="search-result-author"
                            fontSize="14px"
                            sx={{ lineHeight: 1.1 }}
                        >
                            {authorList.map((item) => item.name).join(", ")}
                        </Typography>
                    </Box>
                )}

                {abstract && (
                    <Box>
                        <Typography component="p" sx={sectionHeadingStyle}>
                            Abstract
                        </Typography>
                        <Typography
                            fontSize="14px"
                            className="search-result-abstract"
                        >
                            {abstract}
                        </Typography>
                    </Box>
                )}

                {published && (
                    <Box>
                        <Typography component="p" sx={sectionHeadingStyle}>
                            Date Submitted
                        </Typography>
                        <Typography fontSize="14px">
                            {formatDate(published)}
                            {updated &&
                                ` (Last Updated: ${formatDate(updated)})`}
                        </Typography>
                    </Box>
                )}
            </Box>
        </CardContent>
    );
};

export default SearchResultTable;
