import { useState, useEffect } from 'react';

// Define the report sections that can be included/excluded
export interface ReportSection {
  id: string;
  label: string;
  description: string;
  defaultEnabled: boolean;
}

export const REPORT_SECTIONS: ReportSection[] = [
  {
    id: 'report_header',
    label: 'Report Header',
    description: 'Report ID, generation date, and author information',
    defaultEnabled: true
  },
  {
    id: 'patient_demographics',
    label: 'Patient Demographics',
    description: 'Patient ID, age, gender, height, weight, ethnicity, smoking status',
    defaultEnabled: true
  },
  {
    id: 'test_information',
    label: 'Test Information',
    description: 'Test date, workflow version, and agents used',
    defaultEnabled: true
  },
  {
    id: 'pft_results',
    label: 'PFT Results',
    description: 'Raw data, predicted values, and percent predicted measurements',
    defaultEnabled: true
  },
  {
    id: 'quality_metrics',
    label: 'Quality Metrics',
    description: 'Data completeness, measurement quality, and quality issues',
    defaultEnabled: true
  },
  {
    id: 'interpretation',
    label: 'Interpretation',
    description: 'Pattern, severity, obstruction, restriction, and clinical significance',
    defaultEnabled: true
  },
  {
    id: 'triage_assessment',
    label: 'Triage Assessment',
    description: 'Urgency level, reasons, follow-up recommendations, and immediate actions',
    defaultEnabled: true
  },
  {
    id: 'clinical_summary',
    label: 'Clinical Summary',
    description: 'Concise clinical summary for healthcare providers',
    defaultEnabled: true
  },
  {
    id: 'detailed_interpretation',
    label: 'Detailed Interpretation',
    description: 'Comprehensive analysis and interpretation of results',
    defaultEnabled: true
  },
  {
    id: 'recommendations',
    label: 'Recommendations',
    description: 'Actionable clinical recommendations and next steps',
    defaultEnabled: true
  },
  {
    id: 'quality_assessment',
    label: 'Quality Assessment',
    description: 'Report quality scores and approval status',
    defaultEnabled: true
  },
  {
    id: 'processing_metadata',
    label: 'Processing Metadata',
    description: 'Processing time, agents used, and technical details',
    defaultEnabled: false
  }
];

export interface ReportSettings {
  enabledSections: string[];
  lastUpdated: string;
}

const STORAGE_KEY = 'pft_report_settings';

export function useReportSettings() {
  const [settings, setSettings] = useState<ReportSettings>(() => {
    // Load settings from localStorage on initialization
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Validate that all required sections are present
        const validSections = REPORT_SECTIONS.map(section => section.id);
        const validEnabledSections = parsed.enabledSections?.filter((id: string) => 
          validSections.includes(id)
        ) || [];
        
        return {
          enabledSections: validEnabledSections.length > 0 ? validEnabledSections : 
            REPORT_SECTIONS.filter(s => s.defaultEnabled).map(s => s.id),
          lastUpdated: parsed.lastUpdated || new Date().toISOString()
        };
      }
    } catch (error) {
      console.error('[useReportSettings] Error loading settings:', error);
    }
    
    // Return default settings
    return {
      enabledSections: REPORT_SECTIONS.filter(s => s.defaultEnabled).map(s => s.id),
      lastUpdated: new Date().toISOString()
    };
  });

  // Save settings to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    } catch (error) {
      console.error('[useReportSettings] Error saving settings:', error);
    }
  }, [settings]);

  const toggleSection = (sectionId: string) => {
    setSettings(prev => {
      const isEnabled = prev.enabledSections.includes(sectionId);
      const newEnabledSections = isEnabled
        ? prev.enabledSections.filter(id => id !== sectionId)
        : [...prev.enabledSections, sectionId];
      
      return {
        enabledSections: newEnabledSections,
        lastUpdated: new Date().toISOString()
      };
    });
  };

  const isSectionEnabled = (sectionId: string): boolean => {
    return settings.enabledSections.includes(sectionId);
  };

  const resetToDefaults = () => {
    setSettings({
      enabledSections: REPORT_SECTIONS.filter(s => s.defaultEnabled).map(s => s.id),
      lastUpdated: new Date().toISOString()
    });
  };

  const enableAllSections = () => {
    setSettings({
      enabledSections: REPORT_SECTIONS.map(s => s.id),
      lastUpdated: new Date().toISOString()
    });
  };

  const disableAllSections = () => {
    setSettings({
      enabledSections: [],
      lastUpdated: new Date().toISOString()
    });
  };

  return {
    settings,
    toggleSection,
    isSectionEnabled,
    resetToDefaults,
    enableAllSections,
    disableAllSections,
    sections: REPORT_SECTIONS
  };
} 