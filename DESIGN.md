# POCUS Portal - Design System

## Overview
This document outlines the design improvements made to create a professional, medical/academic aesthetic for the University of Manitoba POCUS Portal.

## Design Philosophy
The design focuses on:
- **Professionalism**: Clean, clinical aesthetic appropriate for medical education
- **Clarity**: High contrast, readable typography, generous whitespace
- **Hierarchy**: Clear visual organization guiding users through learning pathways
- **Accessibility**: Color choices and typography meet WCAG standards

## Color Palette

### Primary Colors (Medical Blue)
- **Primary**: `#0B4F6C` - Deep medical blue for headers and primary actions
- **Primary Light**: `#1B5E7E` - Lighter variant for hover states
- **Primary Dark**: `#053B4F` - Darker variant for emphasis

### Secondary Colors (Medical Teal)
- **Secondary**: `#2A9D8F` - Clean teal for accents and progress
- **Secondary Light**: `#40B5A5` - Lighter variant
- **Secondary Dark**: `#1E7A6F` - Darker variant

### Accent Colors
- **Accent**: `#E76F51` - Coral for important actions
- **Success**: `#52B788` - Muted green for completions and progress

### Neutral Colors
- **Background Main**: `#F8F9FA` - Light gray for page background
- **Card Background**: `#FFFFFF` - White for content cards
- **Sidebar**: `#1A2332` - Dark navy for navigation
- **Navbar**: `#0B1929` - Darker navy for top navigation

## Typography

### Fonts
- **Headings**: Inter (600 weight) - Modern, professional sans-serif
- **Body**: Source Sans Pro (400 weight) - Highly readable for medical content

### Font Sizes
- H1: 2.25rem (36px)
- H2: 1.875rem (30px)
- H3: 1.5rem (24px)
- Body: 1rem (16px)
- Small: 0.875rem (14px)

### Line Heights
- Headings: 1.3
- Body: 1.6
- Improved readability for long-form medical content

## Components

### Dashboard Cards
- Clean white cards with subtle shadows
- Icon-based visual hierarchy
- Gradient accent bars on hover
- Smooth transitions and hover effects
- Replaced bright Bootstrap colors with professional gradients

### Progress Tracking
- **Progress Bars**: Rounded, with gradient fills
- **Competency Badges**: Color-coded skill levels
  - Novice: Amber
  - Intermediate: Blue
  - Advanced: Green
  - Expert: Purple

### Navigation
- Dark sidebar with teal accent colors
- Clear section headings (Core, Education)
- Icon-based navigation for quick recognition
- Active state indicators

### Forms & Inputs
- Increased padding for better touch targets
- Teal focus states (medical secondary color)
- Clear labels with proper hierarchy

## Spacing & Layout
- Increased whitespace throughout
- 8px base unit for spacing consistency
- Generous padding in cards (1.5rem)
- Consistent border radius (8px standard, 12px for cards)

## Shadows
- **Small**: Subtle depth for cards
- **Medium**: Interactive elements on hover
- **Large**: Elevated states for emphasis

## Responsive Design
- Mobile-first approach
- Breakpoints at 768px for tablet/mobile
- Flexible grid system maintained
- Stack cards vertically on mobile

## Implementation Files
- `/static/css/custom-medical.css` - Main custom stylesheet
- `/templates/base.html` - Updated base template with new structure
- `/templates/home.html` - Redesigned dashboard with new card components

## Future Enhancements
- Learning pathway visualization with step indicators
- Milestone badges and achievements
- Interactive ultrasound image annotations
- Video player integration with custom controls
- Certificate generation system

