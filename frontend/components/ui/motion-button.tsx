// frontend/components/ui/motion-button.tsx
'use client';

import * as React from 'react';
import { motion } from 'framer-motion';
import { Button, ButtonProps } from './button'; // Assuming your button is here

/**
 * A Higher-Order Component that wraps the base Button with motion capabilities
 * from Framer Motion, providing default animations for hover and tap states.
 */
export const MotionButton = motion(
  React.forwardRef<HTMLButtonElement, ButtonProps>(
    (props, ref) => <Button ref={ref} {...props} />
  )
);

MotionButton.displayName = 'MotionButton';

// Set default animation properties for the button.
// These can be overridden by passing props directly to an instance of MotionButton.
MotionButton.defaultProps = {
  whileHover: { scale: 1.05 },
  whileTap: { scale: 0.95 },
  transition: { type: 'spring', stiffness: 400, damping: 17 }
};
