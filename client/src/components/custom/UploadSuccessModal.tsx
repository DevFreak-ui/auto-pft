import { useEffect } from "react";
import { CheckCircle } from "lucide-react";
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogOverlay,
} from "@/components/ui/alert-dialog";

interface UploadSuccessModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export function UploadSuccessModal({ isOpen, onClose }: UploadSuccessModalProps) {
  // Auto-close the modal after 5 seconds
  useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        onClose();
      }, 5000);

      return () => clearTimeout(timer);
    }
  }, [isOpen, onClose]);

  // Don't render if not open
  if (!isOpen) return null;

  return (
    <AlertDialog open={isOpen} onOpenChange={onClose}>
      <AlertDialogOverlay className="bg-black/80" />
      <AlertDialogContent className="sm:max-w-md">
        <AlertDialogHeader>
          <div className="flex items-center justify-center mb-4">
            <CheckCircle className="h-12 w-12 text-green-500" />
          </div>
          <AlertDialogTitle className="text-center">Upload Successful!</AlertDialogTitle>
          <AlertDialogDescription className="text-center">
            Your file has been uploaded successfully. Report generation will start soon.
          </AlertDialogDescription>
        </AlertDialogHeader>
      </AlertDialogContent>
    </AlertDialog>
  );
} 