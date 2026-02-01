/**
 * OEE Card Component
 * Displays OEE metrics with color-coding
 */

import React from 'react';

interface OEECardProps {
  label: string;
  value: number;
  showPercentage?: boolean;
  large?: boolean;
}

const OEECard: React.FC<OEECardProps> = ({
  label,
  value,
  showPercentage = true,
  large = false,
}) => {
  const getColor = (val: number) => {
    if (val >= 85) return 'text-green-600';
    if (val >= 70) return 'text-orange-600';
    return 'text-red-600';
  };

  return (
    <div className="kpi-card">
      <div className="kpi-label">{label}</div>
      <div className={`kpi-value ${getColor(value)} ${large ? 'text-5xl' : ''}`}>
        {value.toFixed(1)}{showPercentage && '%'}
      </div>
    </div>
  );
};

export default OEECard;
