/**
 * Main App Component
 * Router and layout setup
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

// Pages
import WorkOrderDashboard from './pages/execution/WorkOrderDashboard';
import WorkOrderExecution from './pages/execution/WorkOrderExecution';
import ProductionOEE from './pages/dashboards/ProductionOEE';

// Components
import FloatingAIAssistant from './components/shared/FloatingAIAssistant';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 30000,
    },
  },
});

const Navigation: React.FC = () => {
  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <h1 className="text-2xl font-bold">MES Execution</h1>
            <div className="flex space-x-4">
              <Link
                to="/"
                className="px-4 py-2 rounded hover:bg-blue-700 transition-colors"
              >
                Work Orders
              </Link>
              <Link
                to="/dashboards/oee"
                className="px-4 py-2 rounded hover:bg-blue-700 transition-colors"
              >
                OEE Dashboard
              </Link>
            </div>
          </div>
          <div className="text-sm">
            Phase 2: Execution & Tracking
          </div>
        </div>
      </div>
    </nav>
  );
};

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Navigation />
          
          <main className="container mx-auto">
            <Routes>
              <Route path="/" element={<WorkOrderDashboard />} />
              <Route path="/execution/work-orders" element={<WorkOrderDashboard />} />
              <Route path="/execution/work-orders/:id" element={<WorkOrderExecution />} />
              <Route path="/dashboards/oee" element={<ProductionOEE />} />
              
              {/* Fallback route */}
              <Route path="*" element={
                <div className="p-6 text-center">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Page Not Found</h2>
                  <p className="text-gray-600">The requested page does not exist.</p>
                  <Link to="/" className="text-blue-600 hover:underline mt-4 inline-block">
                    Go to Work Orders Dashboard
                  </Link>
                </div>
              } />
            </Routes>
          </main>

          {/* Floating AI Assistant */}
          <FloatingAIAssistant />
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
