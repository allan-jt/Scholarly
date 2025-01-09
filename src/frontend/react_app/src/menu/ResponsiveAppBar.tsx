import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import FormControlLabel from "@mui/material/FormControlLabel";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import { School as SchoolIcon } from "@mui/icons-material";
import { MaterialUISwitch } from "./MaterialUISwitch";

const pages = ["About", "Search"];
const links = ["/", "/"];

interface ResponsiveAppBarProps {
    toggleTheme: () => void;
    darkMode: boolean;
}

function ResponsiveAppBar({ toggleTheme, darkMode }: ResponsiveAppBarProps) {
    const [anchorElNav, setAnchorElNav] = React.useState<null | HTMLElement>(
        null
    );

    const handleOpenNavMenu = (event: React.MouseEvent<HTMLElement>) => {
        setAnchorElNav(event.currentTarget);
    };

    const handleCloseNavMenu = () => {
        setAnchorElNav(null);
    };

    return (
        <AppBar position="fixed" color="inherit">
            <Container style={{ maxWidth: "none", height: "70px" }}>
                <Toolbar disableGutters>
                    <SchoolIcon
                        color="primary"
                        sx={{ display: { xs: "none", md: "flex" }, mr: 1 }}
                    />
                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        className="gradient-text"
                        href="/"
                        sx={{
                            mr: 2,
                            display: { xs: "none", md: "flex" },
                            fontWeight: 700,
                            textDecoration: "none",
                        }}
                    >
                        Scholarly
                    </Typography>

                    <Box
                        sx={{
                            flexGrow: 1,
                            display: { xs: "flex", md: "none" },
                        }}
                    >
                        <IconButton
                            size="large"
                            aria-controls="menu-appbar"
                            aria-haspopup="true"
                            onClick={handleOpenNavMenu}
                            color="primary"
                        >
                            <MenuIcon />
                        </IconButton>
                        <Menu
                            id="menu-appbar"
                            anchorEl={anchorElNav}
                            anchorOrigin={{
                                vertical: "bottom",
                                horizontal: "left",
                            }}
                            keepMounted
                            transformOrigin={{
                                vertical: "top",
                                horizontal: "left",
                            }}
                            open={Boolean(anchorElNav)}
                            onClose={handleCloseNavMenu}
                            sx={{ display: { xs: "block", md: "none" } }}
                        >
                            {pages.map((page, index) => (
                                <MenuItem
                                    key={page}
                                    onClick={handleCloseNavMenu}
                                >
                                    <Typography
                                        color="primary"
                                        sx={{
                                            textAlign: "center",
                                            textDecoration: "none",
                                        }}
                                        component="a"
                                        href={links[index]}
                                    >
                                        {page}
                                    </Typography>
                                </MenuItem>
                            ))}
                        </Menu>
                    </Box>
                    <SchoolIcon
                        color="primary"
                        sx={{ display: { xs: "flex", md: "none" }, mr: 1 }}
                    />
                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        className="gradient-text"
                        href="/"
                        sx={{
                            mr: 2,
                            display: { xs: "flex", md: "none" },
                            flexGrow: 1,
                            fontWeight: 700,
                            textDecoration: "none",
                        }}
                    >
                        Scholarly
                    </Typography>
                    <Box
                        sx={{
                            flexGrow: 1,
                            display: { xs: "none", md: "flex" },
                        }}
                    >
                        {pages.map((page, index) => (
                            <Button
                                key={page}
                                onClick={handleCloseNavMenu}
                                color="secondary"
                                sx={{ my: 2, display: "block" }}
                                component="a"
                                href={links[index]}
                            >
                                {page}
                            </Button>
                        ))}
                    </Box>
                    <Box sx={{ flexGrow: 0 }}>
                        <FormControlLabel
                            label=""
                            sx={{ m: 0 }}
                            control={
                                <MaterialUISwitch
                                    checked={darkMode}
                                    onChange={toggleTheme}
                                />
                            }
                        />
                    </Box>
                </Toolbar>
            </Container>
        </AppBar>
    );
}

export default ResponsiveAppBar;
