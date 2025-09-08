import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  CircularProgress,
  Switch,
  FormControlLabel,
  LinearProgress,
  Tabs,
  Tab,
  Paper
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  PlayArrow as PlayIcon,
  Stop as StopIcon,
  CheckCircle as CheckIcon,
  Warning as WarningIcon
} from '@mui/icons-material';

interface RecoveryPageProps {
  currentIncident: number | null;
}

const RecoveryPage: React.FC<RecoveryPageProps> = ({ currentIncident }) => {
  const [tabValue, setTabValue] = useState(0);
  const [systemHealth, setSystemHealth] = useState<any>({});
  const [recoveryStatus, setRecoveryStatus] = useState<any>({});
  const [performanceMetrics, setPerformanceMetrics] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [autoRecoveryEnabled, setAutoRecoveryEnabled] = useState(false);

  useEffect(() => {
    if (currentIncident) {
      fetchSystemHealth();
      fetchRecoveryStatus();
      fetchPerformanceMetrics();
    }
  }, [currentIncident]);

  const fetchSystemHealth = async () => {
    try {
      const response = await fetch(`/api/recovery/system-health/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setSystemHealth(data.health || {});
      }
    } catch (error) {
      console.error('Error fetching system health:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchRecoveryStatus = async () => {
    try {
      const response = await fetch(`/api/recovery/recovery-status/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setRecoveryStatus(data.status || {});
      }
    } catch (error) {
      console.error('Error fetching recovery status:', error);
    }
  };

  const fetchPerformanceMetrics = async () => {
    try {
      const response = await fetch(`/api/recovery/performance-metrics/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setPerformanceMetrics(data.metrics || {});
      }
    } catch (error) {
      console.error('Error fetching performance metrics:', error);
    }
  };

  const handleStartRecovery = async () => {
    try {
      const response = await fetch(`/api/recovery/start-recovery/${currentIncident}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`Recovery initiated for ${data.services_started} services`);
        fetchRecoveryStatus();
        fetchSystemHealth();
      }
    } catch (error) {
      console.error('Error starting recovery:', error);
    }
  };

  const handleStopService = async (serviceName: string) => {
    try {
      const response = await fetch('/api/recovery/control-service', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service_name: serviceName,
          action: 'stop',
          incident_id: currentIncident
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`Service ${serviceName} ${data.success ? 'stopped' : 'failed to stop'}`);
        fetchSystemHealth();
      }
    } catch (error) {
      console.error('Error stopping service:', error);
    }
  };

  const handleStartService = async (serviceName: string) => {
    try {
      const response = await fetch('/api/recovery/control-service', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          service_name: serviceName,
          action: 'start',
          incident_id: currentIncident
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`Service ${serviceName} ${data.success ? 'started' : 'failed to start'}`);
        fetchSystemHealth();
      }
    } catch (error) {
      console.error('Error starting service:', error);
    }
  };

  const handleRecoveryComplete = async () => {
    try {
      const response = await fetch(`/api/recovery/recovery-complete/${currentIncident}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        alert('Recovery phase completed! Moving to Post-Incident phase.');
      }
    } catch (error) {
      console.error('Error marking recovery complete:', error);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (!currentIncident) {
    return (
      <Box>
        <Alert severity="warning">
          No active incident. Please complete the Eradication phase first.
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box className="phase-header">
        <Typography variant="h4" gutterBottom>
          <RefreshIcon sx={{ mr: 2 }} />
          Recovery Phase
        </Typography>
        <Typography variant="subtitle1">
          Restore services, monitor system health, and ensure full operational recovery
        </Typography>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="System Health" />
          <Tab label="Recovery Controls" />
          <Tab label="Performance Metrics" />
        </Tabs>
      </Paper>

      {/* System Health Tab */}
      {tabValue === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  System Health Status
                </Typography>
                
                {systemHealth.services && (
                  <TableContainer>
                    <Table>
                      <TableHead>
                        <TableRow>
                          <TableCell>Service</TableCell>
                          <TableCell>Status</TableCell>
                          <TableCell>Health</TableCell>
                          <TableCell>Actions</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {systemHealth.services.map((service: any, index: number) => (
                          <TableRow key={index}>
                            <TableCell>{service.name}</TableCell>
                            <TableCell>
                              <Chip
                                label={service.status}
                                color={service.status === 'running' ? 'success' : 'error'}
                                size="small"
                              />
                            </TableCell>
                            <TableCell>
                              <Box sx={{ width: '100px' }}>
                                <LinearProgress 
                                  variant="determinate" 
                                  value={service.health_score} 
                                  color={service.health_score > 80 ? 'success' : 'warning'}
                                />
                                <Typography variant="body2">{service.health_score}%</Typography>
                              </Box>
                            </TableCell>
                            <TableCell>
                              {service.status === 'running' ? (
                                <Button
                                  size="small"
                                  color="error"
                                  startIcon={<StopIcon />}
                                  onClick={() => handleStopService(service.name)}
                                >
                                  Stop
                                </Button>
                              ) : (
                                <Button
                                  size="small"
                                  color="success"
                                  startIcon={<PlayIcon />}
                                  onClick={() => handleStartService(service.name)}
                                >
                                  Start
                                </Button>
                              )}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </TableContainer>
                )}
                
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  <Box className="stats-card">
                    <Typography variant="body2" color="text.secondary">Overall Health</Typography>
                    <Typography variant="h4" color="success.main">
                      {systemHealth.overall_health || 0}%
                    </Typography>
                  </Box>
                  
                  <Box className="stats-card">
                    <Typography variant="body2" color="text.secondary">Services Running</Typography>
                    <Typography variant="h4">
                      {systemHealth.running_services || 0}/{systemHealth.total_services || 0}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Health Monitoring</Typography>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={fetchSystemHealth}
                  startIcon={<RefreshIcon />}
                  sx={{ mb: 2 }}
                >
                  Refresh Health Status
                </Button>
                
                <FormControlLabel
                  control={
                    <Switch
                      checked={autoRecoveryEnabled}
                      onChange={(e) => setAutoRecoveryEnabled(e.target.checked)}
                    />
                  }
                  label="Auto-Recovery Mode"
                />
              </CardContent>
            </Card>

            {systemHealth.alerts && systemHealth.alerts.length > 0 && (
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>Health Alerts</Typography>
                  {systemHealth.alerts.map((alert: any, index: number) => (
                    <Alert key={index} severity={alert.severity} sx={{ mb: 1 }}>
                      {alert.message}
                    </Alert>
                  ))}
                </CardContent>
              </Card>
            )}
          </Grid>
        </Grid>
      )}

      {/* Recovery Controls Tab */}
      {tabValue === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Recovery Progress
                </Typography>
                
                {recoveryStatus.phases && (
                  recoveryStatus.phases.map((phase: any, index: number) => (
                    <Box key={index} sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        {phase.name}
                      </Typography>
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Box sx={{ width: '100%', mr: 1 }}>
                          <LinearProgress variant="determinate" value={phase.progress} />
                        </Box>
                        <Box sx={{ minWidth: 35 }}>
                          <Typography variant="body2" color="text.secondary">
                            {phase.progress}%
                          </Typography>
                        </Box>
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {phase.description}
                      </Typography>
                    </Box>
                  ))
                )}
                
                <Box sx={{ mt: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>Recovery Actions</Typography>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleStartRecovery}
                    startIcon={<PlayIcon />}
                    sx={{ mr: 2 }}
                  >
                    Start Automated Recovery
                  </Button>
                  <Button
                    variant="outlined"
                    onClick={fetchRecoveryStatus}
                  >
                    Refresh Status
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Recovery Summary</Typography>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Recovery Progress</Typography>
                  <Typography variant="h4">
                    {recoveryStatus.overall_progress || 0}%
                  </Typography>
                </Box>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Estimated Time</Typography>
                  <Typography variant="h6">
                    {recoveryStatus.estimated_time || 'Unknown'}
                  </Typography>
                </Box>
                
                {recoveryStatus.overall_progress === 100 && (
                  <Button
                    variant="contained"
                    color="success"
                    fullWidth
                    onClick={handleRecoveryComplete}
                    startIcon={<CheckIcon />}
                    sx={{ mt: 2 }}
                  >
                    Recovery Complete → Move to Post-Incident
                  </Button>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Performance Metrics Tab */}
      {tabValue === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  System Performance
                </Typography>
                
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2">CPU Usage</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={performanceMetrics.cpu_usage || 0} 
                    color={performanceMetrics.cpu_usage > 80 ? 'error' : 'primary'}
                  />
                  <Typography variant="body2">{performanceMetrics.cpu_usage || 0}%</Typography>
                </Box>
                
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2">Memory Usage</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={performanceMetrics.memory_usage || 0} 
                    color={performanceMetrics.memory_usage > 80 ? 'error' : 'primary'}
                  />
                  <Typography variant="body2">{performanceMetrics.memory_usage || 0}%</Typography>
                </Box>
                
                <Box sx={{ mb: 3 }}>
                  <Typography variant="subtitle2">Disk Usage</Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={performanceMetrics.disk_usage || 0} 
                    color={performanceMetrics.disk_usage > 90 ? 'error' : 'primary'}
                  />
                  <Typography variant="body2">{performanceMetrics.disk_usage || 0}%</Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Network & Response Times
                </Typography>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Average Response Time</Typography>
                  <Typography variant="h4">
                    {performanceMetrics.response_time || 0}ms
                  </Typography>
                </Box>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Network Throughput</Typography>
                  <Typography variant="h4">
                    {performanceMetrics.network_throughput || 0} Mbps
                  </Typography>
                </Box>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Active Connections</Typography>
                  <Typography variant="h4">
                    {performanceMetrics.active_connections || 0}
                  </Typography>
                </Box>
                
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={fetchPerformanceMetrics}
                  startIcon={<RefreshIcon />}
                  sx={{ mt: 2 }}
                >
                  Refresh Metrics
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default RecoveryPage;
