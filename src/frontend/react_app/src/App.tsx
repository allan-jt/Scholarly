import "./App.css";
import Search from "./search/Search";
import SearchResult from "./search/SearchResult";
import ResponsiveAppBar from "./menu/ResponsiveAppBar";
import { ThemeProvider, createTheme } from "@mui/material";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import CssBaseline from "@mui/material/CssBaseline";

function App() {
    const theme = createTheme({
        typography: {
            fontFamily: '"Lexend", sans-serif',
            fontWeightBold: 700,
            fontWeightRegular: 300,
        },
        palette: {
            background: {
                default: "#ffffff",
            },
            text: {
                primary: "#05171c",
            },
            primary: {
                // light: "#36beff",
                main: "#36beff",
                dark: "#239ad1",
                contrastText: "#05171c",
            },
            secondary: {
                light: "#FAFAFE",
                main: "#8a8bec",
                dark: "#3a3b9e",
                contrastText: "#05171c",
            },
        },
    });

    const darktheme = createTheme({
        typography: {
            fontFamily: '"Lexend", sans-serif',
            fontWeightBold: 700,
            fontWeightRegular: 300,
        },
        palette: {
            mode: "dark",
            background: {
                default: "#05171c",
            },
            text: {
                primary: "#ffffff",
            },
            primary: {
                light: "#ffffff",
                main: "#36beff",
                dark: "#239ad1",
                contrastText: "#05171c",
            },
            secondary: {
                light: "#FAFAFE",
                main: "#8a8bec",
                dark: "#3a3b9e",
                contrastText: "#05171c",
            },
            // error: {
            //     main: "#ff4870",
            //     dark: "#650d73",
            //     contrastText: "#05171c",
            // },
        },
    });

    return (
        <BrowserRouter>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <ResponsiveAppBar />
                <Routes>
                    <Route path="/" element={<Search />} />
                    <Route path="/search" element={<Search />} />
                    <Route path="/search_result" element={<SearchResult />} />
                    {/* <Route path="/about" element={<Search />} /> */}
                </Routes>
            </ThemeProvider>
        </BrowserRouter>
    );
}

export default App;
