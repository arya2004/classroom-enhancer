import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './home'
import Graphs from './graphs'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/graphs" element={<Graphs />} />

        
      </Routes>
    </BrowserRouter>
  )
}

export default App
