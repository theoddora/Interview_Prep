import { ReactNode } from "react";

interface AlertProps {
  children: ReactNode;
}

function Alert({ children }: AlertProps) {
  return <div className="alert alert-primary">{children}</div>;
}

export default Alert;
