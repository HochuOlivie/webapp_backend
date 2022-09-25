import Mmap from "./MyComponents/MyMap";
import { Routes, Route, Link } from "react-router-dom";
import {Button, CssBaseline} from "@mui/material";
import Choose from "./MyComponents/Choose";
import theme from "assets/theme";
import {ThemeProvider} from "@emotion/react";


function App() {

  return (
      // <Routes
      <Routes>
        <Route path="/" element={<Choose/>} />
        <Route path="/partner" element={<Mmap />} />
        <Route path="/customer" element={<Mmap />} />
      </Routes>
  );
}

export default App;
