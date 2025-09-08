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
  Paper,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  Security as SecurityIcon,
  Warning as WarningIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

interface DetectionPageProps {
  currentIncident: number | null;
  setCurrentIncident: (id: number | null) => void;
}

interface AlertData {
  id: number;
  source: string;
  alert_type: string;
  message: string;
  severity: string;
  source_ip: string;
  destination_ip: string;
  created_at: string;
  acknowledged: boolean;
}

const DetectionPage: React.FC<DetectionPageProps> = ({ currentIncident, setCurrentIncident }) => {
  const [alerts, setAlerts] = useState<AlertData[]>([]);
  const [loading, setLoading] = useState(true);
  const [suspiciousIPs, setSuspiciousIPs] = useState<any[]>([]);

  useEffect(() => {
    fetchLiveAlerts();
    fetchSuspiciousIPs();
  }, []);

  const fetchLiveAlerts = async () => {
    try {
      const response = await fetch('/api/detection/alerts');
      if (response.ok) {
        const data = await response.json();
        setAlerts(data);
      }
    } catch (error) {
      console.error('Error fetching alerts:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSuspiciousIPs = async () => {
    try {
      const response = await fetch('/api/detection/suspicious-ips');
      if (response.ok) {
        const data = await response.json();
        setSuspiciousIPs(data.suspicious_ips || []);
      }
    } catch (error) {
      console.error('Error fetching suspicious IPs:', error);
    }
  };

  const handleConfirmAttack = async () => {
    try {
      const response = await fetch('/api/detection/confirm-attack', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          alert_ids: alerts.filter(a => !a.acknowledged).map(a => a.id),
          incident_title: 'Security Incident - Detected Attack',
          incident_description: 'Multiple security alerts triggered indicating potential attack',
          severity: 'high'
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setCurrentIncident(data.incident_id);
        alert('Attack confirmed! Moving to Containment phase.');
      }
    } catch (error) {
      console.error('Error confirming attack:', error);
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box>
      <Box className="phase-header">
        <Typography variant="h4" gutterBottom>
          <SecurityIcon sx={{ mr: 2 }} />
          Detection Phase
        </Typography>
        <Typography variant="subtitle1">
          Monitor live alerts and identify potential security threats
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Live Security Alerts
              </Typography>
              
              {alerts.length === 0 ? (
                <Alert severity="info">No active alerts detected</Alert>
              ) : (
                <TableContainer>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Source</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell>Message</TableCell>
                        <TableCell>Severity</TableCell>
                        <TableCell>Source IP</TableCell>
                        <TableCell>Status</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {alerts.map((alert) => (
                        <TableRow key={alert.id}>
                          <TableCell>{alert.source}</TableCell>
                          <TableCell>{alert.alert_type}</TableCell>
                          <TableCell>{alert.message}</TableCell>
                          <TableCell>
                            <Chip 
                              label={alert.severity} 
                              color={getSeverityColor(alert.severity) as any}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>{alert.source_ip}</TableCell>
                          <TableCell>
                            {alert.acknowledged ? (
                              <Chip label="Acknowledged" color="success" size="small" />
                            ) : (
                              <Chip label="New" color="error" size="small" />
                            )}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Suspicious IP Addresses
              </Typography>
              {suspiciousIPs.length === 0 ? (
                <Typography variant="body2" color="text.secondary">
                  No suspicious IPs detected
                </Typography>
              ) : (
                suspiciousIPs.slice(0, 5).map((ip, index) => (
                  <Box key={index} sx={{ mb: 1, p: 1, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                    <Typography variant="body2" fontWeight="bold">
                      {ip.ip}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      Risk Score: {ip.risk_score}/10 | {ip.country}
                    </Typography>
                  </Box>
                ))
              )}
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Actions
              </Typography>
              <Button
                variant="contained"
                color="error"
                fullWidth
                onClick={handleConfirmAttack}
                disabled={alerts.length === 0}
                startIcon={<WarningIcon />}
                sx={{ mb: 2 }}
              >
                Confirm Attack → Move to Containment
              </Button>
              <Button
                variant="outlined"
                fullWidth
                onClick={fetchLiveAlerts}
                startIcon={<CheckIcon />}
              >
                Refresh Alerts
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DetectionPage;
