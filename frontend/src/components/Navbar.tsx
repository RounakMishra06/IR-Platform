import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Tabs,
  Tab,
  Box,
  Badge,
  IconButton,
  Chip
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Security as DetectionIcon,
  Shield as ContainmentIcon,
  BugReport as EradicationIcon,
  Refresh as RecoveryIcon,
  Assignment as PostIncidentIcon,
  Notifications as NotificationsIcon
} from '@mui/icons-material';

interface NavbarProps {
  currentIncident: number | null;
  setCurrentIncident: (id: number | null) => void;
}

const Navbar: React.FC<NavbarProps> = ({ currentIncident }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const phases = [
    { label: 'Detection', path: '/detection', icon: <DetectionIcon /> },
    { label: 'Containment', path: '/containment', icon: <ContainmentIcon /> },
    { label: 'Eradication', path: '/eradication', icon: <EradicationIcon /> },
    { label: 'Recovery', path: '/recovery', icon: <RecoveryIcon /> },
    { label: 'Post-Incident', path: '/post-incident', icon: <PostIncidentIcon /> }
  ];

  const getCurrentTab = () => {
    const currentPath = location.pathname;
    const tabIndex = phases.findIndex(phase => phase.path === currentPath);
    return tabIndex >= 0 ? tabIndex : false;
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    navigate(phases[newValue].path);
  };

  return (
    <AppBar position="sticky" sx={{ zIndex: 1300 }}>
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ mr: 4 }}>
          Incident Response Platform
        </Typography>
        
        {currentIncident && (
          <Chip 
            label={`Incident #${currentIncident}`} 
            color="secondary" 
            size="small" 
            sx={{ mr: 2 }}
          />
        )}

        <Box sx={{ flexGrow: 1 }}>
          <Tabs
            value={getCurrentTab()}
            onChange={handleTabChange}
            textColor="inherit"
            indicatorColor="secondary"
            variant="scrollable"
            scrollButtons="auto"
          >
            {phases.map((phase, index) => (
              <Tab
                key={phase.path}
                icon={phase.icon}
                label={phase.label}
                iconPosition="start"
                sx={{ minWidth: 120 }}
              />
            ))}
          </Tabs>
        </Box>

        <IconButton color="inherit">
          <Badge badgeContent={3} color="error">
            <NotificationsIcon />
          </Badge>
        </IconButton>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
