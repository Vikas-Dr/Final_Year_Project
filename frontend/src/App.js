import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminPage from "./pages/AdminPage";
import AIChatAgentWidget from "./components/AIChatAgentWidget";
import AuthPage from "./pages/AuthPage";
import DashboardPage from "./pages/DashboardPage";
import HomePage from "./pages/HomePage";
import InterviewEvaluationPage from "./pages/InterviewEvaluationPage";
import InterviewPage from "./pages/InterviewPage";
import ReportsPage from "./pages/ReportsPage";
import ResumeAnalysisPage from "./pages/ResumeAnalysisPage";
import VerificationPage from "./pages/VerificationPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ai-assistant" element={<AIChatAgentWidget />} />
        <Route path="/auth/:role" element={<AuthPage />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={["candidate", "recruiter"]}>
              <DashboardPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/verification"
          element={
            <ProtectedRoute allowedRoles={["candidate"]}>
              <VerificationPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/resume-analysis"
          element={
            <ProtectedRoute allowedRoles={["candidate", "recruiter"]}>
              <ResumeAnalysisPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/interview"
          element={
            <ProtectedRoute allowedRoles={["candidate", "recruiter"]}>
              <InterviewPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/interview-evaluation"
          element={
            <ProtectedRoute allowedRoles={["recruiter"]}>
              <InterviewEvaluationPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/reports"
          element={
            <ProtectedRoute allowedRoles={["candidate", "recruiter"]}>
              <ReportsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/admin"
          element={
            <ProtectedRoute allowedRoles={["recruiter"]}>
              <AdminPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  );
}
