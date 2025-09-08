import React from 'react';
import {
  Grid,
  Paper,
  Typography,
  Box,
  Card,
  CardContent,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  Security as SecurityIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

const Dashboard: React.FC = () => {
  const stats = {
    activeIncidents: 3,
    totalIncidents: 47,
    avgResolutionTime: 4.2,
    threatLevel: 'Medium'
  };

  const recentIncidents = [
    { id: 1, title: 'Suspicious Network Activity', phase: 'Containment', severity: 'High' },
    { id: 2, title: 'Malware Detection', phase: 'Eradication', severity: 'Critical' },
    { id: 3, title: 'Failed Login Attempts', phase: 'Detection', severity: 'Medium' }
  ];

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'Critical': return 'error';
      case 'High': return 'warning';
      case 'Medium': return 'info';
      case 'Low': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Incident Response Dashboard
      </Typography>
      
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <WarningIcon color="error" sx={{ mr: 1 }} />
                <Typography variant="h6">Active Incidents</Typography>
              </Box>
              <Typography variant="h3" color="error.main">
                {stats.activeIncidents}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <SecurityIcon color="primary" sx={{ mr: 1 }} />
                <Typography variant="h6">Total Incidents</Typography>
              </Box>
              <Typography variant="h3" color="primary.main">
                {stats.totalIncidents}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <TrendingUpIcon color="success" sx={{ mr: 1 }} />
                <Typography variant="h6">Avg Resolution</Typography>
              </Box>
              <Typography variant="h3" color="success.main">
                {stats.avgResolutionTime}h
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <CheckIcon color="info" sx={{ mr: 1 }} />
                <Typography variant="h6">Threat Level</Typography>
              </Box>
              <Chip
                label={stats.threatLevel}
                color="warning"
                size="medium"
                sx={{ mt: 1 }}
              />
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              System Health Overview
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Security Services
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={95} 
                color="success" 
                sx={{ height: 8, borderRadius: 4, mb: 1 }}
              />
            </Box>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Network Monitoring
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={87} 
                color="warning" 
                sx={{ height: 8, borderRadius: 4, mb: 1 }}
              />
            </Box>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                Threat Intelligence
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={92} 
                color="success" 
                sx={{ height: 8, borderRadius: 4 }}
              />
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Incidents
            </Typography>
            {recentIncidents.map((incident) => (
              <Box key={incident.id} sx={{ mb: 2, p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                <Typography variant="subtitle2" gutterBottom>
                  #{incident.id} - {incident.title}
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    {incident.phase}
                  </Typography>
                  <Chip 
                    label={incident.severity} 
                    color={getSeverityColor(incident.severity) as any}
                    size="small"
                  />
                </Box>
              </Box>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
