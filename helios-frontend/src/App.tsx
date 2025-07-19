import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { MainLayout } from './components/layout/MainLayout';
import { LoginPage } from './pages/LoginPage';
import AppRoutes from './router/AppRoutes';
import { useAppStore } from './store/useAppStore';

function App() {
  const { user } = useAppStore();

  if (!user) {
    return <LoginPage />;
  }

  return (
    <Router>
      <MainLayout>
        <AnimatePresence mode="wait">
          <AppRoutes />
        </AnimatePresence>
      </MainLayout>
    </Router>
  );
}

export default App; 