import React from 'react';

/**
 * Componente que renderiza "Forma 1" del manual de marca de Hospitalar.
 * Es un elemento gráfico en forma de paso (step) con bordes redondeados.
 */

interface BrandShapeProps {
  className?: string;
  color?: string;
  // Permite rotaciones predefinidas fácilmente
  orientation?: 'up-right' | 'right-down' | 'down-left' | 'left-up';
}

export function BrandShape({ 
  className = "", 
  color = "currentColor",
}: BrandShapeProps) {
  return (
    <svg 
      viewBox="0 0 100 100" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path 
        d="M20 90 L20 60 Q20 40 40 40 L60 40 Q80 40 80 20 L80 10" 
        stroke={color} 
        strokeWidth="20" 
        strokeLinecap="round" 
        strokeLinejoin="round"
      />
    </svg>
  );
}
