"use client";
import { motion } from "framer-motion";
import { ReactNode } from "react";

interface ScrollRevealProps {
  children: ReactNode;
  width?: "fit-content" | "100%";
  delay?: number;
  className?: string;
  overflowHidden?: boolean;
}

export const ScrollReveal = ({ 
  children, 
  width = "100%", 
  delay = 0,
  className = "",
  overflowHidden = true
}: ScrollRevealProps) => {
  return (
    <div style={{ position: "relative", width, overflow: overflowHidden ? "hidden" : "visible" }} className={className}>
      <motion.div
        variants={{
          hidden: { opacity: 0, y: 75 },
          visible: { opacity: 1, y: 0 },
        }}
        initial="hidden"
        whileInView="visible"
        transition={{ duration: 0.5, delay: delay }}
        viewport={{ once: true }}
        className={className}
      >
        {children}
      </motion.div>
    </div>
  );
};
