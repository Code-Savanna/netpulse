import React from 'react';

interface TailwindTestProps {
  className?: string;
}

const TailwindTest: React.FC<TailwindTestProps> = ({ className = '' }) => {
  return (
    <div className={`p-4 bg-blue-100 border border-blue-300 rounded-lg ${className}`}>
      <h3 className="text-lg font-semibold text-blue-800 mb-2">
        Tailwind CSS Test Component
      </h3>
      <p className="text-blue-600">
        This component verifies that Tailwind CSS is working correctly.
      </p>
      <div className="mt-3 flex space-x-2">
        <span className="px-3 py-1 bg-blue-500 text-white rounded-full text-sm">
          Styled
        </span>
        <span className="px-3 py-1 bg-green-500 text-white rounded-full text-sm">
          Working
        </span>
      </div>
    </div>
  );
};

export default TailwindTest;