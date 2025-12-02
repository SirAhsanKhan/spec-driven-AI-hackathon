# Data Model (Conceptual)

This document outlines the conceptual data model for the research paper, defining the structure and key informational components. It is not a database schema but a high-level outline.

## 1. Paper

- **Title**: `string` - The main title of the research paper.
- **Abstract**: `string` - A brief summary of the paper's content.
- **Introduction**: `string` - The introductory section of the paper.
- **CaseStudies**: `CaseStudy[]` - A list of case studies.
- **ComparativeAnalysis**: `string` - The section where case studies are compared.
- **Discussion**: `string` - The section for discussing universal patterns.
- **Conclusion**: `string` - The concluding section of the paper.
- **Bibliography**: `Source[]` - A list of sources cited in the paper.

## 2. CaseStudy

- **Brand**: `Brand` - The successful brand in the case study.
- **Competitor**: `Brand` - The less successful competitor brand.
- **Narrative**: `string` - The historical narrative of the two brands.
- **SuccessFactors**: `SuccessFactor[]` - The success factors identified in the case study.
- **FailurePatterns**: `FailurePattern[]` - The failure patterns identified in the case study.

## 3. Brand

- **Name**: `string` - The name of the brand.
- **History**: `string` - A summary of the brand's history.

## 4. Source

- **Author**: `string` - The author(s) of the source.
- **Title**: `string` - The title of the source.
- **Year**: `integer` - The publication year.
- **Publication**: `string` - The name of the journal, book, or website.
- **DOI_URL**: `string` - The Digital Object Identifier or URL of the source.

## 5. SuccessFactor

- **Name**: `string` - A short name for the success factor (e.g., "Adaptability").
- **Description**: `string` - A description of the success factor.

## 6. FailurePattern

- **Name**: `string` - A short name for the failure pattern (e.g., "Strategic Rigidity").
- **Description**: `string` - A description of the failure pattern.
