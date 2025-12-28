import React, { useState, useEffect } from 'react';
import { Button } from '../components/Button';
import { Card } from '../components/Card';

const AnalyticsDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview'); // overview, reports, widgets
  const [analyticsData, setAnalyticsData] = useState({
    summary: {
      total_courses_enrolled: 5,
      average_completion_rate: 75.5,
      average_performance: 82.3,
      average_engagement: 68.7,
      total_learning_hours: 42
    },
    course_progress: [
      { course_id: 1, course_title: 'Advanced React', completion_rate: 95, performance: 88 },
      { course_id: 2, course_title: 'Python for Data Science', completion_rate: 78, performance: 92 },
      { course_id: 3, course_title: 'UI/UX Design', completion_rate: 65, performance: 75 },
      { course_id: 4, course_title: 'Machine Learning', completion_rate: 45, performance: 80 },
      { course_id: 5, course_title: 'Cloud Computing', completion_rate: 30, performance: 70 }
    ],
    recent_activities: [
      { id: 1, event_type: 'video_complete', content_type: 'lesson', timestamp: '2023-06-15T10:30:00Z', metadata: { lesson_title: 'React Hooks Deep Dive' } },
      { id: 2, event_type: 'quiz_complete', content_type: 'quiz', timestamp: '2023-06-14T15:45:00Z', metadata: { quiz_title: 'JavaScript Fundamentals Quiz', score: 85 } },
      { id: 3, event_type: 'discussion_post', content_type: 'discussion', timestamp: '2023-06-14T09:15:00Z', metadata: { discussion_title: 'Best practices for state management' } },
      { id: 4, event_type: 'page_view', content_type: 'course', timestamp: '2023-06-13T11:20:00Z', metadata: { course_title: 'Advanced React' } },
      { id: 5, event_type: 'resource_download', content_type: 'resource', timestamp: '2023-06-13T08:30:00Z', metadata: { resource_title: 'React Cheat Sheet' } }
    ]
  });
  const [reports, setReports] = useState([
    {
      id: 1,
      title: 'Monthly Engagement Report',
      description: 'User engagement metrics for May 2023',
      report_type: 'user_engagement',
      generated_at: '2023-06-01T10:00:00Z',
      is_published: true
    },
    {
      id: 2,
      title: 'Course Performance Analysis',
      description: 'Performance metrics across all courses',
      report_type: 'course_performance',
      generated_at: '2023-05-28T14:30:00Z',
      is_published: true
    },
    {
      id: 3,
      title: 'Learning Progress Report',
      description: 'Individual progress tracking',
      report_type: 'learning_progress',
      generated_at: '2023-05-25T09:15:00Z',
      is_published: false
    }
  ]);
  const [widgets, setWidgets] = useState([
    {
      id: 1,
      title: 'Completion Rate',
      widget_type: 'metric_card',
      data: { value: 75.5, change: 5.2, unit: '%' }
    },
    {
      id: 2,
      title: 'Performance Score',
      widget_type: 'metric_card',
      data: { value: 82.3, change: -2.1, unit: 'pts' }
    },
    {
      id: 3,
      title: 'Learning Hours',
      widget_type: 'metric_card',
      data: { value: 42, change: 8.5, unit: 'hrs' }
    },
    {
      id: 4,
      title: 'Engagement Trend',
      widget_type: 'line_chart',
      data: [65, 68, 72, 70, 75, 78, 82]
    }
  ]);
  const [newReport, setNewReport] = useState({
    title: '',
    description: '',
    report_type: 'user_engagement'
  });

  const handleCreateReport = () => {
    if (newReport.title.trim()) {
      const report = {
        id: reports.length + 1,
        ...newReport,
        generated_at: new Date().toISOString(),
        is_published: false
      };
      setReports([report, ...reports]);
      setNewReport({
        title: '',
        description: '',
        report_type: 'user_engagement'
      });
      alert('Report created successfully!');
    }
  };

  const handlePublishReport = (id) => {
    setReports(prev => 
      prev.map(report => 
        report.id === id ? { ...report, is_published: !report.is_published } : report
      )
    );
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-6">Analytics Dashboard</h2>
      
      <div className="flex space-x-4 mb-6 border-b border-gray-200 dark:border-gray-700">
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'overview'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'reports'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('reports')}
        >
          Reports
        </button>
        <button
          className={`px-4 py-2 font-medium text-sm rounded-t-lg ${
            activeTab === 'widgets'
              ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50 dark:bg-gray-700 dark:text-blue-400'
              : 'text-gray-600 hover:text-gray-800 dark:text-gray-400 dark:hover:text-gray-300'
          }`}
          onClick={() => setActiveTab('widgets')}
        >
          Dashboard Widgets
        </button>
      </div>
      
      <div className="mt-4">
        {activeTab === 'overview' && (
          <div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card className="text-center p-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Courses Enrolled</h3>
                <p className="text-3xl font-bold text-blue-600 dark:text-blue-400">{analyticsData.summary.total_courses_enrolled}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Total courses</p>
              </Card>
              
              <Card className="text-center p-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Completion Rate</h3>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">{analyticsData.summary.average_completion_rate}%</p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Avg. progress</p>
              </Card>
              
              <Card className="text-center p-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Performance</h3>
                <p className="text-3xl font-bold text-purple-600 dark:text-purple-400">{analyticsData.summary.average_performance}</p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Score (0-100)</p>
              </Card>
              
              <Card className="text-center p-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-2">Learning Time</h3>
                <p className="text-3xl font-bold text-orange-600 dark:text-orange-400">{analyticsData.summary.total_learning_hours}h</p>
                <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">Total hours</p>
              </Card>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card className="p-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Course Progress</h3>
                <div className="space-y-4">
                  {analyticsData.course_progress.map((course) => (
                    <div key={course.course_id}>
                      <div className="flex justify-between mb-1">
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{course.course_title}</span>
                        <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{course.completion_rate}%</span>
                      </div>
                      <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
                        <div 
                          className="bg-blue-600 h-2.5 rounded-full" 
                          style={{ width: `${course.completion_rate}%` }}
                        ></div>
                      </div>
                      <div className="flex justify-between mt-1">
                        <span className="text-xs text-gray-500 dark:text-gray-400">Performance: {course.performance}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
              
              <Card className="p-6">
                <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  {analyticsData.recent_activities.map((activity) => (
                    <div key={activity.id} className="flex items-start">
                      <div className="bg-blue-100 dark:bg-blue-900 rounded-full p-2 mr-3">
                        <svg className="w-4 h-4 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                        </svg>
                      </div>
                      <div className="flex-1">
                        <p className="text-sm text-gray-800 dark:text-white">
                          <span className="font-medium capitalize">{activity.event_type.replace('_', ' ')}</span> in {activity.metadata[`${activity.content_type}_title`] || activity.content_type}
                        </p>
                        <p className="text-xs text-gray-500 dark:text-gray-400">
                          {new Date(activity.timestamp).toLocaleString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
            
            <Card className="p-6">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Engagement Trend</h3>
              <div className="h-64 flex items-end space-x-2">
                {[65, 68, 72, 70, 75, 78, 82].map((value, index) => (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div 
                      className="w-full bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
                      style={{ height: `${value}%` }}
                    ></div>
                    <span className="text-xs text-gray-500 dark:text-gray-400 mt-1">W{index + 1}</span>
                  </div>
                ))}
              </div>
            </Card>
          </div>
        )}
        
        {activeTab === 'reports' && (
          <div>
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Create New Report</h3>
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Report Title
                    </label>
                    <input
                      type="text"
                      value={newReport.title}
                      onChange={(e) => setNewReport({...newReport, title: e.target.value})}
                      placeholder="Enter report title"
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                      Report Type
                    </label>
                    <select
                      value={newReport.report_type}
                      onChange={(e) => setNewReport({...newReport, report_type: e.target.value})}
                      className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                    >
                      <option value="user_engagement">User Engagement</option>
                      <option value="course_performance">Course Performance</option>
                      <option value="learning_progress">Learning Progress</option>
                      <option value="revenue">Revenue</option>
                      <option value="instructor">Instructor Analytics</option>
                      <option value="system_usage">System Usage</option>
                    </select>
                  </div>
                </div>
                
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Description
                  </label>
                  <textarea
                    value={newReport.description}
                    onChange={(e) => setNewReport({...newReport, description: e.target.value})}
                    placeholder="Describe the report..."
                    rows="2"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-600 text-gray-900 dark:text-white"
                  />
                </div>
                
                <Button variant="primary" onClick={handleCreateReport}>
                  Create Report
                </Button>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Your Reports</h3>
              <div className="space-y-4">
                {reports.map((report) => (
                  <div 
                    key={report.id} 
                    className="p-4 rounded-lg border border-gray-200 dark:border-gray-600 bg-white dark:bg-gray-700"
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-800 dark:text-white">{report.title}</h4>
                        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">{report.description}</p>
                        <div className="flex items-center mt-2">
                          <span className="text-xs bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 px-2 py-1 rounded mr-2">
                            {report.report_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                          </span>
                          <span className="text-xs text-gray-500 dark:text-gray-400">
                            Created: {new Date(report.generated_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                      <div className="flex space-x-2">
                        <Button 
                          variant={report.is_published ? "secondary" : "primary"} 
                          size="sm"
                          onClick={() => handlePublishReport(report.id)}
                        >
                          {report.is_published ? 'Unpublish' : 'Publish'}
                        </Button>
                        <Button variant="secondary" size="sm">View</Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {activeTab === 'widgets' && (
          <div>
            <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-4">Dashboard Widgets</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {widgets.map((widget) => (
                <Card key={widget.id} className="p-6">
                  <h4 className="font-medium text-gray-800 dark:text-white mb-2">{widget.title}</h4>
                  
                  {widget.widget_type === 'metric_card' && (
                    <div>
                      <p className="text-3xl font-bold text-gray-800 dark:text-white">
                        {widget.data.value}{widget.data.unit}
                      </p>
                      <p className={`text-sm mt-1 ${widget.data.change >= 0 ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                        {widget.data.change >= 0 ? '↑' : '↓'} {Math.abs(widget.data.change)} from last period
                      </p>
                    </div>
                  )}
                  
                  {widget.widget_type === 'line_chart' && (
                    <div className="h-32 flex items-end space-x-1">
                      {widget.data.map((value, index) => (
                        <div 
                          key={index} 
                          className="flex-1 bg-blue-500 rounded-t hover:bg-blue-600 transition-colors"
                          style={{ height: `${value}%` }}
                        ></div>
                      ))}
                    </div>
                  )}
                  
                  <Button variant="secondary" size="sm" className="mt-4">
                    Configure
                  </Button>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AnalyticsDashboard;