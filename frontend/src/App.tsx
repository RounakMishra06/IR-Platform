import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import Navbar from './components/Navbar';
import Dashboard from './components/Dashboard';
import DetectionPage from './pages/DetectionPage';
import ContainmentPage from './pages/ContainmentPage';
import EradicationPage from './pages/EradicationPage';
import RecoveryPage from './pages/RecoveryPage';
import PostIncidentPage from './pages/PostIncidentPage';
import { NotificationProvider } from './context/NotificationContext';
import './App.css';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#0a0a0a',
      paper: '#1e1e1e',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
});

function App() {
  const [currentIncident, setCurrentIncident] = useState<number | null>(null);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <NotificationProvider>
        <Router>
          <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
            <Navbar currentIncident={currentIncident} setCurrentIncident={setCurrentIncident} />
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route 
                  path="/detection" 
                  element={<DetectionPage currentIncident={currentIncident} setCurrentIncident={setCurrentIncident} />} 
                />
                <Route 
                  path="/containment" 
                  element={<ContainmentPage currentIncident={currentIncident} />} 
                />
                <Route 
                  path="/eradication" 
                  element={<EradicationPage currentIncident={currentIncident} />} 
                />
                <Route 
                  path="/recovery" 
                  element={<RecoveryPage currentIncident={currentIncident} />} 
                />
                <Route 
                  path="/post-incident" 
                  element={<PostIncidentPage currentIncident={currentIncident} />} 
                />
              </Routes>
            </Box>
          </Box>
        </Router>
      </NotificationProvider>
    </ThemeProvider>
  );
}

export default App;
