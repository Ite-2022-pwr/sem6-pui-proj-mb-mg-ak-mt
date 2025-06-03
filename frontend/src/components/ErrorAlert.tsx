import { AlertCircle } from "lucide-react";

interface ErrorAlertProps {
  status?: number;
  message: string;
}

function ErrorAlert({ status, message }: ErrorAlertProps) {
  return (
    <div className="flex items-start gap-2 bg-red-100 border border-red-300 text-red-800 px-4 py-3 rounded-md mb-4">
      <AlertCircle className="mt-1" size={20} />
      <div>
        {status && <p className="font-bold">Error {status}</p>}
        <p>{message}</p>
      </div>
    </div>
  );
}

export default ErrorAlert;
