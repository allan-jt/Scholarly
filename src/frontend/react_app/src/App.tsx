import { useState, useEffect } from "react";
import "./App.css";
import Search from "./search/Search";
import SearchResult from "./search/SearchResult";
import ResponsiveAppBar from "./menu/ResponsiveAppBar";
import { ThemeProvider, createTheme } from "@mui/material";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import CssBaseline from "@mui/material/CssBaseline";

function App() {
    const [darkMode, setDarkMode] = useState(() => {
        const savedTheme = localStorage.getItem("theme");
        return savedTheme === "dark";
    });

    const toggleTheme = () => {
        setDarkMode((prev) => {
            const newMode = !prev;
            localStorage.setItem("theme", newMode ? "dark" : "light");
            return newMode;
        });
    };

    const theme = createTheme({
        typography: {
            fontFamily: '"Lexend", sans-serif',
            fontWeightBold: 700,
            fontWeightRegular: 300,
        },
        palette: {
            mode: darkMode ? "dark" : "light",
            ...(darkMode
                ? {
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
                  }
                : {
                      background: {
                          default: "#ffffff",
                      },
                      text: {
                          primary: "#05171c",
                      },
                      primary: {
                          main: "#36beff",
                          dark: "#239ad1",
                          contrastText: "#05171c",
                      },
                      secondary: {
                          main: "#8a8bec",
                          dark: "#3a3b9e",
                          contrastText: "#05171c",
                      },
                  }),
        },
    });

    useEffect(() => {
        const savedTheme = localStorage.getItem("theme");
        if (savedTheme) {
            setDarkMode(savedTheme === "dark");
        }
    }, []);

    return (
        <BrowserRouter>
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <ResponsiveAppBar
                    toggleTheme={toggleTheme}
                    darkMode={darkMode}
                />
                <Routes>
                    <Route path="/" element={<Search />} />
                    <Route path="/search" element={<Search />} />
                    <Route path="/search_result" element={<SearchResult />} />
                </Routes>
            </ThemeProvider>
        </BrowserRouter>
    );
}

export default App;
