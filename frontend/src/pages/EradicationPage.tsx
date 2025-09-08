import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  TextField,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  CircularProgress,
  Tabs,
  Tab,
  Paper
} from '@mui/material';
import {
  BugReport as BugIcon,
  Search as SearchIcon,
  Security as SecurityIcon,
  CheckCircle as CheckIcon
} from '@mui/icons-material';

interface EradicationPageProps {
  currentIncident: number | null;
}

const EradicationPage: React.FC<EradicationPageProps> = ({ currentIncident }) => {
  const [tabValue, setTabValue] = useState(0);
  const [logAnalysis, setLogAnalysis] = useState<any>({});
  const [vulnerabilities, setVulnerabilities] = useState<any[]>([]);
  const [threatIndicators, setThreatIndicators] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [iocSearch, setIocSearch] = useState('');

  useEffect(() => {
    if (currentIncident) {
      fetchLogAnalysis();
      fetchVulnerabilities();
    }
  }, [currentIncident]);

  const fetchLogAnalysis = async () => {
    try {
      const response = await fetch(`/api/eradication/incident/${currentIncident}/analysis`);
      if (response.ok) {
        const data = await response.json();
        setLogAnalysis(data.analysis || {});
      }
    } catch (error) {
      console.error('Error fetching log analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchVulnerabilities = async () => {
    try {
      const response = await fetch(`/api/eradication/vulnerabilities/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setVulnerabilities(data.vulnerabilities || {});
      }
    } catch (error) {
      console.error('Error fetching vulnerabilities:', error);
    }
  };

  const handleSearchIOCs = async () => {
    if (!iocSearch.trim()) return;
    
    try {
      const indicators = iocSearch.split('\n').map(i => i.trim()).filter(i => i);
      const response = await fetch('/api/eradication/search-iocs', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          indicators,
          incident_id: currentIncident
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        setThreatIndicators(data.results || []);
      }
    } catch (error) {
      console.error('Error searching IOCs:', error);
    }
  };

  const handleApplyPatches = async () => {
    try {
      const unpatched = Object.values(vulnerabilities).flat()
        .filter((vuln: any) => !vuln.patched)
        .map((vuln: any) => vuln.cve_id);
      
      const response = await fetch('/api/eradication/apply-patches', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          vulnerability_ids: unpatched,
          incident_id: currentIncident
        }),
      });
      
      if (response.ok) {
        const data = await response.json();
        alert(`Applied ${data.success_count} patches successfully`);
        fetchVulnerabilities();
      }
    } catch (error) {
      console.error('Error applying patches:', error);
    }
  };

  const handleEradicationComplete = async () => {
    try {
      const response = await fetch(`/api/eradication/eradication-complete/${currentIncident}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        alert('Eradication phase completed! Moving to Recovery phase.');
      }
    } catch (error) {
      console.error('Error marking eradication complete:', error);
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
          No active incident. Please complete the Containment phase first.
        </Alert>
      </Box>
    );
  }

  return (
    <Box>
      <Box className="phase-header">
        <Typography variant="h4" gutterBottom>
          <BugIcon sx={{ mr: 2 }} />
          Eradication Phase
        </Typography>
        <Typography variant="subtitle1">
          Remove threats, patch vulnerabilities, and analyze attack vectors
        </Typography>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs value={tabValue} onChange={(e, newValue) => setTabValue(newValue)}>
          <Tab label="Log Analysis" />
          <Tab label="Threat Intelligence" />
          <Tab label="Vulnerability Management" />
        </Tabs>
      </Paper>

      {/* Log Analysis Tab */}
      {tabValue === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Incident Log Analysis
                </Typography>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Total Events</Typography>
                  <Typography variant="h4">{logAnalysis.total_events || 0}</Typography>
                </Box>
                
                <Box className="stats-card">
                  <Typography variant="body2" color="text.secondary">Malicious Events</Typography>
                  <Typography variant="h4" color="error.main">{logAnalysis.malicious_events || 0}</Typography>
                </Box>
                
                {logAnalysis.attack_vectors && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>Attack Vectors Detected:</Typography>
                    {logAnalysis.attack_vectors.map((vector: string, index: number) => (
                      <Chip key={index} label={vector} sx={{ mr: 1, mb: 1 }} />
                    ))}
                  </Box>
                )}
                
                {logAnalysis.affected_systems && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>Affected Systems:</Typography>
                    {logAnalysis.affected_systems.map((system: string, index: number) => (
                      <Chip key={index} label={system} color="warning" sx={{ mr: 1, mb: 1 }} />
                    ))}
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Analysis Actions</Typography>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={fetchLogAnalysis}
                  sx={{ mb: 2 }}
                >
                  Refresh Analysis
                </Button>
                <Button
                  variant="contained"
                  fullWidth
                  onClick={() => setTabValue(2)}
                >
                  View Vulnerabilities
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Threat Intelligence Tab */}
      {tabValue === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Search Threat Intelligence
                </Typography>
                
                <TextField
                  label="IOCs (one per line)"
                  multiline
                  rows={6}
                  fullWidth
                  value={iocSearch}
                  onChange={(e) => setIocSearch(e.target.value)}
                  placeholder="Enter IPs, domains, or hashes..."
                  sx={{ mb: 2 }}
                />
                
                <Button
                  variant="contained"
                  onClick={handleSearchIOCs}
                  startIcon={<SearchIcon />}
                  disabled={!iocSearch.trim()}
                >
                  Search IOCs
                </Button>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Threat Intelligence Results
                </Typography>
                
                {threatIndicators.length === 0 ? (
                  <Alert severity="info">No threat intelligence results yet</Alert>
                ) : (
                  threatIndicators.map((result, index) => (
                    <Box key={index} sx={{ mb: 2, p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                      <Typography variant="body1" fontWeight="bold">
                        {result.indicator}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Threat Score: {result.threat_score}/10
                      </Typography>
                      <Box sx={{ mt: 1 }}>
                        {result.malicious ? (
                          <Chip label="Malicious" color="error" size="small" />
                        ) : (
                          <Chip label="Clean" color="success" size="small" />
                        )}
                      </Box>
                    </Box>
                  ))
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Vulnerability Management Tab */}
      {tabValue === 2 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Vulnerability Status
                </Typography>
                
                {Object.keys(vulnerabilities).length === 0 ? (
                  <Alert severity="info">Loading vulnerability data...</Alert>
                ) : (
                  Object.entries(vulnerabilities).map(([severity, vulns]: [string, any]) => (
                    <Box key={severity} sx={{ mb: 3 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        {severity.toUpperCase()} Severity ({vulns.length})
                      </Typography>
                      {vulns.map((vuln: any, index: number) => (
                        <Box key={index} sx={{ mb: 1, p: 2, border: '1px solid', borderColor: 'divider', borderRadius: 1 }}>
                          <Typography variant="body2" fontWeight="bold">
                            {vuln.cve_id} - Score: {vuln.score}
                          </Typography>
                          <Typography variant="body2">
                            {vuln.description}
                          </Typography>
                          <Box sx={{ mt: 1 }}>
                            {vuln.patched ? (
                              <Chip label="Patched" color="success" size="small" />
                            ) : (
                              <Chip label="Unpatched" color="error" size="small" />
                            )}
                          </Box>
                        </Box>
                      ))}
                    </Box>
                  ))
                )}
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>Patch Management</Typography>
                <Button
                  variant="contained"
                  color="warning"
                  fullWidth
                  onClick={handleApplyPatches}
                  sx={{ mb: 2 }}
                >
                  Apply All Available Patches
                </Button>
                <Button
                  variant="outlined"
                  fullWidth
                  onClick={fetchVulnerabilities}
                >
                  Refresh Vulnerabilities
                </Button>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>Complete Eradication</Typography>
                <Button
                  variant="contained"
                  color="success"
                  fullWidth
                  onClick={handleEradicationComplete}
                  startIcon={<CheckIcon />}
                >
                  Eradication Complete → Move to Recovery
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Box>
  );
};

export default EradicationPage;
