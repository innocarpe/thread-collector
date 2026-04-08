"use client";

type ButtonProps = {
  children: React.ReactNode;
  kind?: "primary" | "secondary" | "ghost";
  type?: "button" | "submit";
  onClick?: () => void;
};

export function Button({ children, kind = "primary", type = "button", onClick }: ButtonProps) {
  return (
    <button className={`button ${kind}`} type={type} onClick={onClick}>
      {children}
    </button>
  );
}
