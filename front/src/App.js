import CustomerMap from "./MyComponents/CustomerMap";
import { Routes, Route, Link } from "react-router-dom";
import {Button, CssBaseline} from "@mui/material";
import Choose from "./MyComponents/Choose";
import theme from "assets/theme";
import {ThemeProvider} from "@emotion/react";
import {useRef} from "react";
import PartnerMap from "./MyComponents/PartnerMap";


function App() {
    const oneTime = useRef(false)

  return (

      // <Routes
      <Routes>
        <Route path="/" element={<Choose />} />
        <Route path="/partner" element={<PartnerMap />} />
        <Route path="/customer" element={<CustomerMap />} />
      </Routes>
  );
}

export default App;
