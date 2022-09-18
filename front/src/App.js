import './App.css';
import Mmap from "./Components/MyMap";
import { Routes, Route, Link } from "react-router-dom";
import {Button} from "@mui/material";



function App() {

  return (
      // <Routes
      <Routes>
        <Route path="/partner" element={<Mmap />} />
        <Route path="/customer" element={<Button variant="text">Text</Button>} />s
      </Routes>

  );
}

export default App;
