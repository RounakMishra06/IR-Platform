import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Shield as ShieldIcon,
  Block as BlockIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

interface ContainmentPageProps {
  currentIncident: number | null;
}

const ContainmentPage: React.FC<ContainmentPageProps> = ({ currentIncident }) => {
  const [attackerIPs, setAttackerIPs] = useState<string[]>([]);
  const [blockedIPs, setBlockedIPs] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [containmentStatus, setContainmentStatus] = useState<any>({});
  const [blockDialogOpen, setBlockDialogOpen] = useState(false);
  const [selectedIPs, setSelectedIPs] = useState<string[]>([]);
  const [blockReason, setBlockReason] = useState('');

  useEffect(() => {
    if (currentIncident) {
      fetchAttackerIPs();
      fetchContainmentStatus();
    }
  }, [currentIncident]);

  const fetchAttackerIPs = async () => {
    try {
      const response = await fetch(`/api/containment/incident/${currentIncident}/attacker-ips`);
      if (response.ok) {
        const data = await response.json();
        setAttackerIPs(data.attacker_ips || []);
      }
    } catch (error) {
      console.error('Error fetching attacker IPs:', error);
    }
  };

  const fetchContainmentStatus = async () => {
    try {
      const response = await fetch(`/api/containment/status/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setContainmentStatus(data);
        setBlockedIPs(data.blocked_ips || []);
      }
    } catch (error) {
      console.error('Error fetching containment status:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleBlockIPs = async () => {
    try {
      const response = await fetch('/api/containment/block-ips', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ip_addresses: selectedIPs,
          reason: blockReason,
          incident_id: currentIncident
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setBlockedIPs([...blockedIPs, ...data.blocked_ips]);
        setSelectedIPs([]);
        setBlockDialogOpen(false);
        setBlockReason('');
        fetchContainmentStatus();
        alert(`Successfully blocked ${data.blocked_ips.length} IP addresses`);
      }
    } catch (error) {
      console.error('Error blocking IPs:', error);
    }
  };

  const handleContainmentComplete = async () => {
    try {
      const response = await fetch(`/api/containment/containment-complete/${currentIncident}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        alert('Containment phase completed! Moving to Eradication phase.');
      }
    } catch (error) {
      console.error('Error marking containment complete:', error);
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
          No active incident. Please confirm an attack in the Detection phase first.
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box className="phase-header">
        <Typography variant="h4" gutterBottom>
          <ShieldIcon sx={{ mr: 2 }} />
          Containment Phase
        </Typography>
        <Typography variant="subtitle1">
          Block malicious IPs and contain the attack
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Attacker IP Addresses
              </Typography>
              
              {attackerIPs.length === 0 ? (
                <Alert severity="info">No attacker IPs identified</Alert>
              ) : (
                <Box>
                  {attackerIPs.map((ip, index) => (
                    <Box key={index} sx={{ mb: 1, p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                      <Typography variant="body1" fontWeight="bold">{ip}</Typography>
                      <Box sx={{ mt: 1 }}>
                        {blockedIPs.includes(ip) ? (
                          <Chip label="Blocked" color="success" size="small" />
                        ) : (
                          <Chip label="Active Threat" color="error" size="small" />
                        )}
                      </Box>
                    </Box>
                  ))}
                  
                  <Button
                    variant="contained"
                    color="error"
                    onClick={() => {
                      setSelectedIPs(attackerIPs.filter(ip => !blockedIPs.includes(ip)));
                      setBlockDialogOpen(true);
                    }}
                    disabled={attackerIPs.every(ip => blockedIPs.includes(ip))}
                    startIcon={<BlockIcon />}
                    sx={{ mt: 2 }}
                  >
                    Block All Unblocked IPs
                  </Button>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Containment Status
              </Typography>
              
              <Box className="stats-card">
                <Typography variant="body2" color="text.secondary">Blocked IPs</Typography>
                <Typography variant="h4" color="success.main">
                  {containmentStatus.blocked_ips_count || 0}
                </Typography>
              </Box>
              
              <Box className="stats-card">
                <Typography variant="body2" color="text.secondary">Active Connections</Typography>
                <Typography variant="h4" color="primary.main">
                  {containmentStatus.active_connections || 0}
                </Typography>
              </Box>
              
              <Box className="stats-card">
                <Typography variant="body2" color="text.secondary">Blocked Connections</Typography>
                <Typography variant="h4" color="error.main">
                  {containmentStatus.blocked_connections || 0}
                </Typography>
              </Box>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Actions
              </Typography>
              
              <Button
                variant="contained"
                color="success"
                fullWidth
                onClick={handleContainmentComplete}
                startIcon={<CheckIcon />}
                sx={{ mb: 2 }}
                disabled={blockedIPs.length === 0}
              >
                Containment Complete → Move to Eradication
              </Button>
              
              <Button
                variant="outlined"
                fullWidth
                onClick={fetchContainmentStatus}
              >
                Refresh Status
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Block IPs Dialog */}
      <Dialog open={blockDialogOpen} onClose={() => setBlockDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Block IP Addresses</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            IPs to block: {selectedIPs.join(', ')}
          </Typography>
          <TextField
            label="Reason for blocking"
            multiline
            rows={3}
            fullWidth
            value={blockReason}
            onChange={(e) => setBlockReason(e.target.value)}
            placeholder="e.g., Malicious activity detected, Attack confirmed"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setBlockDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleBlockIPs} 
            variant="contained" 
            color="error"
            disabled={!blockReason.trim()}
          >
            Block IPs
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ContainmentPage;
