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
  Stepper,
  Step,
  StepLabel,
  Paper,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import {
  Assignment as ReportIcon,
  Timeline as TimelineIcon,
  Download as DownloadIcon,
  Send as SendIcon,
  CheckCircle as CheckIcon,
  Edit as EditIcon
} from '@mui/icons-material';

interface PostIncidentPageProps {
  currentIncident: number | null;
}

const PostIncidentPage: React.FC<PostIncidentPageProps> = ({ currentIncident }) => {
  const [incidentReport, setIncidentReport] = useState<any>({});
  const [timeline, setTimeline] = useState<any[]>([]);
  const [lessons, setLessons] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [reportDialogOpen, setReportDialogOpen] = useState(false);
  const [newLesson, setNewLesson] = useState({ category: '', description: '', recommendation: '' });

  // Form fields for the report
  const [reportForm, setReportForm] = useState({
    executive_summary: '',
    root_cause: '',
    impact_assessment: '',
    response_timeline: '',
    lessons_learned: '',
    recommendations: '',
    follow_up_actions: ''
  });

  useEffect(() => {
    if (currentIncident) {
      fetchIncidentReport();
      fetchTimeline();
      fetchLessonsLearned();
    }
  }, [currentIncident]);

  const fetchIncidentReport = async () => {
    try {
      const response = await fetch(`/api/post-incident/incident-report/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setIncidentReport(data.report || {});
        setReportForm(data.report || {});
      }
    } catch (error) {
      console.error('Error fetching incident report:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTimeline = async () => {
    try {
      const response = await fetch(`/api/post-incident/timeline/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setTimeline(data.timeline || []);
      }
    } catch (error) {
      console.error('Error fetching timeline:', error);
    }
  };

  const fetchLessonsLearned = async () => {
    try {
      const response = await fetch(`/api/post-incident/lessons-learned/${currentIncident}`);
      if (response.ok) {
        const data = await response.json();
        setLessons(data.lessons || []);
      }
    } catch (error) {
      console.error('Error fetching lessons learned:', error);
    }
  };

  const handleSaveReport = async () => {
    try {
      const response = await fetch(`/api/post-incident/save-report/${currentIncident}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(reportForm),
      });
      
      if (response.ok) {
        alert('Incident report saved successfully!');
        setReportDialogOpen(false);
        fetchIncidentReport();
      }
    } catch (error) {
      console.error('Error saving report:', error);
    }
  };

  const handleGenerateReport = async () => {
    try {
      const response = await fetch(`/api/post-incident/generate-report/${currentIncident}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        a.download = `incident_${currentIncident}_report.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Error generating report:', error);
    }
  };

  const handleAddLesson = async () => {
    try {
      const response = await fetch('/api/post-incident/add-lesson', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          incident_id: currentIncident,
          ...newLesson
        }),
      });
      
      if (response.ok) {
        setNewLesson({ category: '', description: '', recommendation: '' });
        fetchLessonsLearned();
      }
    } catch (error) {
      console.error('Error adding lesson:', error);
    }
  };

  const handleCloseIncident = async () => {
    try {
      const response = await fetch(`/api/post-incident/close-incident/${currentIncident}`, {
        method: 'POST',
      });
      
      if (response.ok) {
        alert('Incident closed successfully! All phases completed.');
      }
    } catch (error) {
      console.error('Error closing incident:', error);
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
          No active incident. Please complete the Recovery phase first.
        </Alert>
      </Box>
    );
  }

  const timelineSteps = timeline.map(event => event.phase);

  return (
    <Box>
      <Box className="phase-header">
        <Typography variant="h4" gutterBottom>
          <ReportIcon sx={{ mr: 2 }} />
          Post-Incident Phase
        </Typography>
        <Typography variant="subtitle1">
          Document findings, analyze lessons learned, and create comprehensive incident reports
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Incident Timeline */}
        <Grid item xs={12}>
          <Card sx={{ mb: 3 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <TimelineIcon sx={{ mr: 1 }} />
                Incident Timeline
              </Typography>
              
              <Stepper alternativeLabel>
                {timelineSteps.map((step, index) => (
                  <Step key={index} completed={true}>
                    <StepLabel>{step}</StepLabel>
                  </Step>
                ))}
              </Stepper>
              
              <TableContainer sx={{ mt: 3 }}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Timestamp</TableCell>
                      <TableCell>Phase</TableCell>
                      <TableCell>Event</TableCell>
                      <TableCell>Actor</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {timeline.map((event, index) => (
                      <TableRow key={index}>
                        <TableCell>{new Date(event.timestamp).toLocaleString()}</TableCell>
                        <TableCell>
                          <Chip label={event.phase} size="small" />
                        </TableCell>
                        <TableCell>{event.description}</TableCell>
                        <TableCell>{event.actor}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Report Summary */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Incident Report Summary
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" gutterBottom>Executive Summary</Typography>
                <Typography variant="body2" color="text.secondary">
                  {incidentReport.executive_summary || 'No summary available yet.'}
                </Typography>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" gutterBottom>Root Cause Analysis</Typography>
                <Typography variant="body2" color="text.secondary">
                  {incidentReport.root_cause || 'Root cause analysis pending.'}
                </Typography>
              </Box>
              
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle1" gutterBottom>Impact Assessment</Typography>
                <Typography variant="body2" color="text.secondary">
                  {incidentReport.impact_assessment || 'Impact assessment not completed.'}
                </Typography>
              </Box>
              
              <Box sx={{ display: 'flex', gap: 2 }}>
                <Button
                  variant="contained"
                  onClick={() => setReportDialogOpen(true)}
                  startIcon={<EditIcon />}
                >
                  Edit Report
                </Button>
                <Button
                  variant="outlined"
                  onClick={handleGenerateReport}
                  startIcon={<DownloadIcon />}
                >
                  Download PDF
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Report Statistics */}
        <Grid item xs={12} md={4}>
          <Card sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>Incident Metrics</Typography>
              
              <Box className="stats-card">
                <Typography variant="body2" color="text.secondary">Total Duration</Typography>
                <Typography variant="h4">
                  {incidentReport.total_duration || '0h'}
                </Typography>
              </Box>
              
              <Box className="stats-card">
                <Typography variant="body2" color="text.secondary">Systems Affected</Typography>
                <Typography variant="h4">
                  {incidentReport.systems_affected || 0}
                </Typography>
              </Box>
              
              <Box className="stats-card">
                <Typography variant="body2" color="text.secondary">Severity Level</Typography>
                <Typography variant="h4" color="error.main">
                  {incidentReport.severity || 'Unknown'}
                </Typography>
              </Box>
            </CardContent>
          </Card>

          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>Complete Incident</Typography>
              <Button
                variant="contained"
                color="success"
                fullWidth
                onClick={handleCloseIncident}
                startIcon={<CheckIcon />}
              >
                Close Incident
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Lessons Learned */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Lessons Learned
              </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <TextField
                    label="Category"
                    fullWidth
                    value={newLesson.category}
                    onChange={(e) => setNewLesson({ ...newLesson, category: e.target.value })}
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12} md={8}>
                  <TextField
                    label="Description"
                    fullWidth
                    value={newLesson.description}
                    onChange={(e) => setNewLesson({ ...newLesson, description: e.target.value })}
                    sx={{ mb: 2 }}
                  />
                </Grid>
                <Grid item xs={12}>
                  <TextField
                    label="Recommendation"
                    fullWidth
                    multiline
                    rows={2}
                    value={newLesson.recommendation}
                    onChange={(e) => setNewLesson({ ...newLesson, recommendation: e.target.value })}
                    sx={{ mb: 2 }}
                  />
                  <Button
                    variant="contained"
                    onClick={handleAddLesson}
                    disabled={!newLesson.category || !newLesson.description}
                  >
                    Add Lesson
                  </Button>
                </Grid>
              </Grid>
              
              {lessons.length > 0 && (
                <Box sx={{ mt: 3 }}>
                  <Typography variant="subtitle1" gutterBottom>Recorded Lessons</Typography>
                  {lessons.map((lesson, index) => (
                    <Paper key={index} sx={{ p: 2, mb: 2 }}>
                      <Typography variant="subtitle2" gutterBottom>
                        {lesson.category}
                      </Typography>
                      <Typography variant="body2" gutterBottom>
                        {lesson.description}
                      </Typography>
                      <Typography variant="body2" color="primary">
                        <strong>Recommendation:</strong> {lesson.recommendation}
                      </Typography>
                    </Paper>
                  ))}
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Report Edit Dialog */}
      <Dialog 
        open={reportDialogOpen} 
        onClose={() => setReportDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Incident Report</DialogTitle>
        <DialogContent>
          <TextField
            label="Executive Summary"
            fullWidth
            multiline
            rows={3}
            value={reportForm.executive_summary}
            onChange={(e) => setReportForm({ ...reportForm, executive_summary: e.target.value })}
            sx={{ mb: 2, mt: 1 }}
          />
          
          <TextField
            label="Root Cause"
            fullWidth
            multiline
            rows={3}
            value={reportForm.root_cause}
            onChange={(e) => setReportForm({ ...reportForm, root_cause: e.target.value })}
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Impact Assessment"
            fullWidth
            multiline
            rows={3}
            value={reportForm.impact_assessment}
            onChange={(e) => setReportForm({ ...reportForm, impact_assessment: e.target.value })}
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Lessons Learned"
            fullWidth
            multiline
            rows={3}
            value={reportForm.lessons_learned}
            onChange={(e) => setReportForm({ ...reportForm, lessons_learned: e.target.value })}
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Recommendations"
            fullWidth
            multiline
            rows={3}
            value={reportForm.recommendations}
            onChange={(e) => setReportForm({ ...reportForm, recommendations: e.target.value })}
            sx={{ mb: 2 }}
          />
          
          <TextField
            label="Follow-up Actions"
            fullWidth
            multiline
            rows={3}
            value={reportForm.follow_up_actions}
            onChange={(e) => setReportForm({ ...reportForm, follow_up_actions: e.target.value })}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setReportDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveReport} variant="contained">Save Report</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PostIncidentPage;
