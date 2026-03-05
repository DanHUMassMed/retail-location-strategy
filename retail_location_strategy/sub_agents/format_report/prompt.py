def format_report_instruction() -> str:
    return """Generate a comprehensive, professional HTML report for a location intelligence analysis.

This report should be in the style of McKinsey/BCG consulting presentations:
- Multi-slide format using full-screen scrollable sections
- Modern, clean, executive-ready design
- Data-driven visualizations
- Professional color scheme and typography

CRITICAL REQUIREMENTS:

1. STRUCTURE - Create 7 distinct slides (full-screen sections):

   SLIDE 1 - EXECUTIVE SUMMARY & TOP RECOMMENDATION
   - Large, prominent display of recommended location and score
   - Business type and target location
   - High-level market validation
   - Eye-catching hero section

   SLIDE 2 - TOP RECOMMENDATION DETAILS
   - All strengths with evidence (cards/boxes)
   - All concerns with mitigation strategies
   - Opportunity type and target customer segment

   SLIDE 3 - COMPETITION ANALYSIS
   - Competition metrics (total competitors, density, chain dominance)
   - Visual representation of key numbers (large stat boxes)
   - Average ratings, high performers count

   SLIDE 4 - MARKET CHARACTERISTICS
   - Population density, income level, infrastructure
   - Foot traffic patterns, rental costs
   - Grid/card layout for each characteristic

   SLIDE 5 - ALTERNATIVE LOCATIONS
   - Each alternative in a comparison card
   - Scores, opportunity types, strengths/concerns
   - Why each is not the top choice

   SLIDE 6 - KEY INSIGHTS & NEXT STEPS
   - Strategic insights (bullet points or cards)
   - Actionable next steps (numbered list)

   SLIDE 7 - METHODOLOGY
   - How the analysis was performed
   - Data sources and approach

2. DESIGN:
   - Use professional consulting color palette:
     * Primary: Navy blue (#1e3a8a, #3b82f6) for headers/trust
     * Success: Green (#059669, #10b981) for positive metrics
     * Warning: Amber (#d97706, #f59e0b) for concerns
     * Neutral: Grays (#6b7280, #e5e7eb) for backgrounds
   - Modern sans-serif fonts (system: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto)
   - Cards with subtle shadows and rounded corners
   - Generous white space and padding
   - Responsive grid layouts

3. TECHNICAL:
   - Self-contained: ALL CSS embedded in <style> tag
   - No external dependencies (no CDNs, no external images)
   - Each slide: min-height: 100vh; page-break-after: always;
   - Smooth scroll behavior
   - Print-friendly

4. DATA TO INCLUDE (use EXACTLY this data, do not invent):

{report_generation_result}

5. OUTPUT:
   - Generate ONLY the complete HTML code
   - Start with <!DOCTYPE html>
   - End with </html>
   - NO explanations before or after the HTML
   - NO markdown code fences

Make it visually stunning, data-rich, and executive-ready.

Current date: {current_date}
"""