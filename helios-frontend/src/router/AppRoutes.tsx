import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from '../pages/LoginPage';
import { PlannerPage } from '../pages/PlannerPage';
import { ChallengePage } from '../pages/ChallengePage';
import { AIWorkshopPage } from '../pages/AIWorkshopPage';
import { TreeHolePage } from '../pages/TreeHolePage';
import { useAppStore } from '../store/useAppStore';

const AppRoutes: React.FC = () => {
  const { activeView } = useAppStore();
  
  // 根据activeView渲染对应的页面
  const renderActivePage = () => {
    switch (activeView) {
      case 'planner':
        return <PlannerPage />;
      case 'challenge':
        return <ChallengePage />;
      case 'ai':
        return <AIWorkshopPage />;
      case 'treehole':
        return <TreeHolePage />;
      default:
        return <PlannerPage />;
    }
  };

  return (
    <Routes>
      <Route path="/" element={renderActivePage()} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
};

export default AppRoutes; 