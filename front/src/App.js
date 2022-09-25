import Mmap from "./MyComponents/MyMap";
import { Routes, Route, Link } from "react-router-dom";
import {Button, CssBaseline} from "@mui/material";
import Choose from "./MyComponents/Choose";
import theme from "assets/theme";
import {ThemeProvider} from "@emotion/react";
import {useRef} from "react";


function App() {
    const oneTime = useRef(false)

  return (

      // <Routes
      <Routes>
        <Route path="/" element={<Choose/>} />
        <Route path="/partner" element={<Mmap oneTime={oneTime} />} />
        <Route path="/customer" element={<Mmap oneTime={oneTime}/>} />
      </Routes>
  );
}

export default App;
