import './App.css';
import Mmap from "./MyComponents/MyMap";
import { Routes, Route, Link } from "react-router-dom";
import {Button} from "@mui/material";
import Choose from "./MyComponents/Choose";



function App() {

  return (
      // <Routes
      <Routes>
        <Route path="/" element={<Choose/>} />
        <Route path="/partner" element={<Mmap />} />
        <Route path="/customer" element={<Button variant="text">Text</Button>} />
      </Routes>

  );
}

export default App;
