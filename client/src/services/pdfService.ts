import { shortenReportId } from "@/herlpers";

// Interface for PDF generation
export interface PDFReportData {
  report_id: string;
  patient_demographics: any;
  test_date: string;
  raw_data: any;
  predicted_values: any;
  percent_predicted: any;
  quality_metrics: any;
  interpretation: any;
  triage: any; // Changed from triage_assessment to triage
  report_content: any;
  quality_assessment: any;
  generated_by: string;
  generated_at: string;
  processing_metadata: any;
}

// Interface for PDF generation options
export interface PDFGenerationOptions {
  enabledSections?: string[];
}

/**
 * Generate a professional PDF report from the report data
 * @param reportData - The complete report data
 * @param options - Optional generation options including enabled sections
 * @returns Promise with the PDF blob
 */
export async function generatePDFReport(
  reportData: PDFReportData, 
  options: PDFGenerationOptions = {}
): Promise<Blob> {
  console.log("[pdfService] Generating PDF for report:", reportData.report_id);
  
  try {
    // Create the PDF content using jsPDF
    const { jsPDF } = await import('jspdf');
    const doc = new jsPDF();
    
    // Set document properties
    doc.setProperties({
      title: `PFT Report - ${shortenReportId(reportData.report_id)}`,
      subject: 'Pulmonary Function Test Report',
      author: reportData.generated_by,
      creator: 'AutoPFTReport System'
    });

    let yPosition = 20;
    const pageWidth = doc.internal.pageSize.getWidth();
    const margin = 20;
    const contentWidth = pageWidth - (margin * 2);

    // Add Korle Bu Teaching Hospital logo
    try {
      const logoModule = await import('@/assets/images/korle-bu.png');
      const logoUrl = logoModule.default;
      
      // Convert image to base64
      const response = await fetch(logoUrl);
      const blob = await response.blob();
      const logoBase64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result as string);
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
      
      const logoWidth = 60;
      const logoHeight = 30;
      const logoX = (pageWidth - logoWidth) / 2;
      
      doc.addImage(logoBase64, 'PNG', logoX, yPosition, logoWidth, logoHeight);
      yPosition += logoHeight + 15; // Add space after logo
    } catch (error) {
      console.warn("[pdfService] Could not load logo:", error);
      // Continue without logo if it fails to load
    }

    // Helper function to add text with word wrapping
    const addWrappedText = (text: string, y: number, fontSize: number = 12, isBold: boolean = false) => {
      doc.setFontSize(fontSize);
      if (isBold) doc.setFont('helvetica', 'bold');
      else doc.setFont('helvetica', 'normal');
      
      const lines = doc.splitTextToSize(text, contentWidth);
      doc.text(lines, margin, y);
      return y + (lines.length * fontSize * 0.4);
    };

    // Helper function to add section header
    const addSectionHeader = (title: string, y: number) => {
      doc.setFontSize(10);
      doc.setFont('helvetica', 'bold');
      doc.setTextColor(0, 100, 0); // Green color
      doc.text(title, margin, y);
      doc.setTextColor(0, 0, 0); // Reset to black
      return y + 8;
    };

    // Helper function to add table
    const addTable = (headers: string[], data: any[][], startY: number) => {
      const colWidth = contentWidth / headers.length;
      let currentY = startY;

      // Add headers
      doc.setFontSize(10);
      doc.setFont('helvetica', 'bold');
      headers.forEach((header, index) => {
        doc.text(header, margin + (index * colWidth), currentY);
      });
      currentY += 6;

      // Add data rows
      doc.setFont('helvetica', 'normal');
      data.forEach(row => {
        row.forEach((cell, index) => {
          const cellText = cell?.toString() || '-';
          const lines = doc.splitTextToSize(cellText, colWidth - 2);
          doc.text(lines, margin + (index * colWidth), currentY);
        });
        currentY += 6;
      });

      return currentY + 5;
    };

    // Helper function to check if we need a new page
    const checkNewPage = (y: number, requiredSpace: number = 20) => {
      const pageHeight = doc.internal.pageSize.getHeight();
      if (y + requiredSpace > pageHeight - margin) {
        doc.addPage();
        return 20;
      }
      return y;
    };

    // Helper function to check if a section should be included
    const shouldIncludeSection = (sectionId: string): boolean => {
      if (!options.enabledSections || options.enabledSections.length === 0) {
        return true; // Include all sections if none specified
      }
      return options.enabledSections.includes(sectionId);
    };

    // 1. Reporting Date (like in the image)
    yPosition += 10;
    doc.setFontSize(10);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(128, 128, 128); // Gray color
    doc.text('REPORTING DATE', margin, yPosition);
    doc.setTextColor(0, 0, 0); // Reset to black
    
    // Add the date text on the same line
    const dateText = new Date().toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric'
    });
    doc.setFontSize(12);
    doc.setFont('helvetica', 'normal');
    doc.text(dateText, margin + 60, yPosition); // Position date to the right of "REPORTING DATE"
    yPosition += 15; 

    // 2. Referral Details
    yPosition = checkNewPage(yPosition);
    yPosition = addSectionHeader('REFERRAL DETAILS', yPosition);
    const referralDemographics = reportData.patient_demographics;
    const referralTable = [
      ['NAME', referralDemographics?.patient_id ? `Patient ${referralDemographics.patient_id}` : ''],
      ['REFERRAL HOSPITAL', ''],
      ['INDICATION FOR PFT', 'Routine pulmonary function assessment'],
      ['REFERRING PHYSICIAN', '-']
    ];
    
    // Create table with faint borders and smaller text
    const colWidth = contentWidth / 2;
    const rowHeight = 6;
    let currentY = yPosition;
    
    // Draw table borders
    doc.setDrawColor(200, 200, 200); // Faint gray color for borders
    doc.setLineWidth(0.3);
    
    // Draw outer border
    doc.rect(margin, currentY - 5, contentWidth, (referralTable.length * rowHeight) + 10);
    
    // Draw vertical line between columns
    doc.line(margin + colWidth, currentY - 5, margin + colWidth, currentY + (referralTable.length * rowHeight) + 5);
    
    // Draw horizontal lines between rows
    referralTable.forEach((row, index) => {
      if (index > 0) {
        doc.line(margin, currentY + (index * rowHeight) - 5, margin + contentWidth, currentY + (index * rowHeight) - 5);
      }
    });
    
    // Add table content with smaller text
    referralTable.forEach((row, index) => {
      const rowY = currentY + (index * rowHeight);
      
      // Left column (bold, smaller font)
      doc.setFontSize(10);
      doc.setFont('helvetica', 'bold');
      doc.text(row[0] || '', margin + 5, rowY);
      
      // Right column (normal, smaller font)
      doc.setFont('helvetica', 'normal');
      doc.text(row[1] || '', margin + colWidth + 5, rowY);
    });
    
    // Reset line width and color
    doc.setLineWidth(1);
    doc.setDrawColor(0, 0, 0);
    
    yPosition = currentY + (referralTable.length * rowHeight) + 20;

    // // 3. Test Results
    // yPosition = checkNewPage(yPosition);
    // yPosition = addSectionHeader('TEST RESULTS', yPosition);
    // yPosition = addWrappedText('Tests are technically acceptable.', yPosition, 12);
    // yPosition = addWrappedText('Please, see the attachment for spirometric measures, flow volume loops, and volume time graphs', yPosition, 10);
    // yPosition += 10;

    // // 4. Comments
    // yPosition = checkNewPage(yPosition);
    // yPosition = addSectionHeader('COMMENTS', yPosition);
    // const commentsRawData = reportData.raw_data;
    // const commentsInterpretation = reportData.interpretation;
    
    // // Dynamic comments based on actual data
    // const comments = [];
    
    // // Flow-volume loop comment
    // comments.push('DISPLAY (find attached): The flow-volume loop shows no in-coving.');
    
    // // FEV1/FVC ratio comment
    // if (commentsRawData?.fev1 && commentsRawData?.fvc) {
    //   const fev1FvcRatio = (parseFloat(commentsRawData.fev1) / parseFloat(commentsRawData.fvc) * 100).toFixed(1);
    //   comments.push(`FEV1/FVC ratio (${fev1FvcRatio}%) is within normal limits.`);
    // } else {
    //   comments.push('FEV1/FVC ratio is within normal limits.');
    // }
    
    // // FVC and FEV1 comments
    // if (commentsRawData?.fvc) {
    //   comments.push(`FVC (${commentsRawData.fvc} L) is within normal limits.`);
    // } else {
    //   comments.push('FVC is within normal limits.');
    // }
    
    // if (commentsRawData?.fev1) {
    //   comments.push(`FEV1 (${commentsRawData.fev1} L) is within normal limits.`);
    // } else {
    //   comments.push('FEV1 is within normal limits.');
    // }
    
    // // FEF25-75 comment
    // if (commentsRawData?.fef2575) {
    //   comments.push(`FEF25-75% (${commentsRawData.fef2575} L/s) is within normal limits.`);
    // } else {
    //   comments.push('FEF25-75% is within normal limits.');
    // }
    
    // comments.forEach(comment => {
    //   yPosition = addWrappedText(`• ${comment}`, yPosition, 10);
    // });
    // yPosition += 10;

    // // 5. Conclusions (like in the image)
    // yPosition = checkNewPage(yPosition);
    // yPosition = addSectionHeader('CONCLUSIONS', yPosition);
    
    // // Dynamic conclusions based on actual data
    // const conclusions = [];
    
    // // Main conclusion based on interpretation pattern
    // if (commentsInterpretation?.pattern) {
    //   const pattern = commentsInterpretation.pattern.toUpperCase();
    //   conclusions.push(`THE RESULTS ARE SUGGESTIVE OF A ${pattern} SPIROMETRY`);
    // } else {
    //   conclusions.push('THE RESULTS ARE SUGGESTIVE OF A NORMAL SPIROMETRY');
    // }
    
    // // Obstruction and restriction assessment
    // const hasObstruction = commentsInterpretation?.obstruction || false;
    // const hasRestriction = commentsInterpretation?.restriction || false;
    
    // if (!hasObstruction && !hasRestriction) {
    //   conclusions.push('There is no airway obstruction or pulmonary restriction based on spirometry.');
    // } else {
    //   if (hasObstruction) {
    //     conclusions.push('There is evidence of airway obstruction based on spirometry.');
    //   }
    //   if (hasRestriction) {
    //     conclusions.push('There is evidence of pulmonary restriction based on spirometry.');
    //   }
    // }
    
    // // Predicted values if available
    // const percentPredicted = reportData.percent_predicted;
    // if (percentPredicted?.fev1 && percentPredicted?.fvc) {
    //   conclusions.push(`The client has ${percentPredicted.fev1}% of the predicted pre-bronchodilator FEV1 and ${percentPredicted.fvc}% of the predicted pre-bronchodilator FVC.`);
    // } else {
    //   conclusions.push('Predicted values are not available for comparison.');
    // }
    
    // conclusions.forEach(conclusion => {
    //   yPosition = addWrappedText(`• ${conclusion}`, yPosition, 10);
    // });
    // yPosition += 10;

    // 6. Additional Report Data (from actual report)
    yPosition = checkNewPage(yPosition);
    yPosition = addSectionHeader('DETAILED REPORT DATA', yPosition);
    
    // Patient Demographics
    yPosition = addWrappedText('Patient Demographics:', yPosition, 12);
    const demographics = reportData.patient_demographics;
    if (demographics) {
      yPosition = addWrappedText(`Patient ID: ${demographics.patient_id || 'N/A'}`, yPosition, 10);
      yPosition = addWrappedText(`Age: ${demographics.age || 'N/A'}`, yPosition, 10);
      yPosition = addWrappedText(`Gender: ${demographics.gender || 'N/A'}`, yPosition, 10);
      yPosition = addWrappedText(`Height: ${demographics.height || 'N/A'} cm`, yPosition, 10);
      yPosition = addWrappedText(`Weight: ${demographics.weight || 'N/A'} kg`, yPosition, 10);
      yPosition = addWrappedText(`Ethnicity: ${demographics.ethnicity || 'N/A'}`, yPosition, 10);
      yPosition = addWrappedText(`Smoking Status: ${demographics.smoking_status || 'N/A'}`, yPosition, 10);
    }
    yPosition += 10;

    // Raw Data & Predicted Values
    yPosition = addWrappedText('Raw Data & Predicted Values:', yPosition, 12);
    const detailedRawData = reportData.raw_data;
    if (detailedRawData) {
      const tableHeaders = ['Parameter', 'Measured', 'Predicted', '% Predicted'];
      const tableData = [
        ['FVC', detailedRawData.fvc || 'N/A', 'N/A', 'N/A'],
        ['FEV₁', detailedRawData.fev1 || 'N/A', 'N/A', 'N/A'],
        ['PEF', detailedRawData.pef || 'N/A', 'N/A', 'N/A'],
        ['FEF₂₅–₇₅', detailedRawData.fef2575 || 'N/A', 'N/A', 'N/A']
      ];
      yPosition = addTable(tableHeaders, tableData, yPosition);
    }
    yPosition += 10;

    // 7. Triage Assessment
    if (shouldIncludeSection('triage_assessment')) {
      yPosition = checkNewPage(yPosition);
      yPosition = addSectionHeader('TRIAGE ASSESSMENT', yPosition);
      const triage = reportData.triage;
      if (triage) {
        yPosition = addWrappedText(`Level: ${triage.level || 'N/A'}`, yPosition, 10);
        yPosition = addWrappedText(`Reasons: ${triage.reasons?.join(', ') || 'N/A'}`, yPosition, 10);
        yPosition = addWrappedText(`Recommended Follow-up: ${triage.recommended_followup || 'N/A'}`, yPosition, 10);
        yPosition = addWrappedText(`Specialist Referral: ${triage.specialist_referral ? 'Yes' : 'No'}`, yPosition, 10);
        if (triage.specialist_type) {
          yPosition = addWrappedText(`Specialist Type: ${triage.specialist_type}`, yPosition, 10);
        }
        yPosition = addWrappedText(`Urgency Score: ${triage.urgency_score || 'N/A'}/10`, yPosition, 10);
        yPosition = addWrappedText(`Immediate Actions: ${triage.immediate_actions?.join(', ') || 'None'}`, yPosition, 10);
        if (triage.monitoring_requirements?.length > 0) {
          yPosition = addWrappedText(`Monitoring Requirements: ${triage.monitoring_requirements.join(', ')}`, yPosition, 10);
        }
        if (triage.follow_up_instructions?.length > 0) {
          yPosition = addWrappedText(`Follow-up Instructions: ${triage.follow_up_instructions.join(', ')}`, yPosition, 10);
        }
      }
      yPosition += 10;
    }

    // 8. Report Content
    if (shouldIncludeSection('clinical_summary')) {
      yPosition = checkNewPage(yPosition);
      yPosition = addSectionHeader('CLINICAL SUMMARY', yPosition);
      const reportContent = reportData.report_content;
      if (reportContent?.clinical_summary) {
        yPosition = addWrappedText(reportContent.clinical_summary, yPosition, 10);
        yPosition += 5;
      }
    }

    if (shouldIncludeSection('detailed_interpretation')) {
      yPosition = checkNewPage(yPosition);
      yPosition = addSectionHeader('DETAILED INTERPRETATION', yPosition);
      const reportContent = reportData.report_content;
      if (reportContent?.detailed_interpretation) {
        yPosition = addWrappedText(reportContent.detailed_interpretation, yPosition, 10);
        yPosition += 5;
      }
    }

    if (shouldIncludeSection('recommendations')) {
      yPosition = checkNewPage(yPosition);
      yPosition = addSectionHeader('RECOMMENDATIONS', yPosition);
      const reportContent = reportData.report_content;
      if (reportContent?.recommendations_text) {
        yPosition = addWrappedText(reportContent.recommendations_text, yPosition, 10);
        yPosition += 5;
      }
    }

    // 9. Quality Assessment
    if (shouldIncludeSection('quality_assessment')) {
      yPosition = checkNewPage(yPosition);
      yPosition = addSectionHeader('QUALITY ASSESSMENT', yPosition);
      const qualityAssessment = reportData.quality_assessment;
      if (qualityAssessment) {
        yPosition = addWrappedText(`Overall Quality: ${qualityAssessment.overall_quality || 'N/A'}/10`, yPosition, 10);
        yPosition = addWrappedText(`Completeness: ${qualityAssessment.completeness || 'N/A'}/10`, yPosition, 10);
        yPosition = addWrappedText(`Clarity: ${qualityAssessment.clarity || 'N/A'}/10`, yPosition, 10);
        yPosition = addWrappedText(`Medical Accuracy: ${qualityAssessment.medical_accuracy || 'N/A'}/10`, yPosition, 10);
        yPosition = addWrappedText(`Approval Status: ${qualityAssessment.approval_status || 'N/A'}`, yPosition, 10);
      }
    }

    // 10. Processing Metadata
    if (shouldIncludeSection('processing_metadata')) {
      yPosition = checkNewPage(yPosition);
      yPosition = addSectionHeader('PROCESSING METADATA', yPosition);
      const metadata = reportData.processing_metadata;
      if (metadata) {
        yPosition = addWrappedText(`Processing Time: ≈${(metadata.processing_time / 60).toFixed(1)} minutes`, yPosition, 10);
        yPosition = addWrappedText(`Agents Used: ${metadata.agents_used?.join(', ') || 'N/A'}`, yPosition, 10);
      }
    }

    // Generate PDF blob
    const pdfBlob = doc.output('blob');
    console.log("[pdfService] PDF generated successfully");
    
    return pdfBlob;
    
  } catch (error) {
    console.error("[pdfService] Error generating PDF:", error);
    throw new Error('Failed to generate PDF report');
  }
}

/**
 * Download the PDF report
 * @param reportData - The report data
 * @param options - Optional generation options including enabled sections
 * @param filename - Optional custom filename
 */
export async function downloadPDFReport(
  reportData: PDFReportData, 
  options: PDFGenerationOptions = {},
  filename?: string
): Promise<void> {
  try {
    const pdfBlob = await generatePDFReport(reportData, options);
    const defaultFilename = `PFT_Report_${shortenReportId(reportData.report_id)}_${new Date().toISOString().split('T')[0]}.pdf`;
    const finalFilename = filename || defaultFilename;
    
    // Create download link
    const url = URL.createObjectURL(pdfBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = finalFilename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    
    console.log("[pdfService] PDF downloaded successfully:", finalFilename);
  } catch (error) {
    console.error("[pdfService] Error downloading PDF:", error);
    throw error;
  }
} 