import React from "react";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: "sm" | "md" | "lg";
  variant?: "default" | "outline";
  children: React.ReactNode;
}

export const Button = ({
  size = "md",
  variant = "default",
  children,
  className = "",
  ...props
}: ButtonProps) => {
  let baseClass = "px-4 py-2 rounded focus:outline-none transition-colors";

  // Adjust size
  if (size === "sm") {
    baseClass += " text-sm";
  } else if (size === "lg") {
    baseClass += " text-lg";
  } else {
    baseClass += " text-base";
  }

  // Adjust variant
  if (variant === "outline") {
    baseClass += " border border-gray-300 text-gray-700 hover:bg-gray-100";
  } else {
    baseClass += " bg-blue-500 text-white hover:bg-blue-600";
  }

  return (
    <button className={`${baseClass} ${className}`} {...props}>
      {children}
    </button>
  );
};

export default Button;
