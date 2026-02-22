# Gestion des Équipements - Equipment Management Module

A comprehensive Odoo 17 custom module for managing IT equipment lifecycle, including equipment tracking, employee assignment, warranty management, and return workflows.

## Overview

This module provides a complete solution for equipment management in Odoo 17 with an intuitive kanban interface, advanced warranty tracking, and streamlined equipment assignment/return processes.

## Features

### Core Equipment Management
- **Equipment Registry**: Manage all IT equipment with details including name, serial number, type, purchase date, and warranty expiration
- **Status Tracking**: Track equipment status with four states:
  - **Disponible** (Available) - Green badge
  - **Assigné** (Assigned) - Blue badge
  - **En réparation** (In Repair) - Orange badge
  - **Retiré** (Retired) - Red badge

### Visual Interface (Kanban View)
- **Equipment Cards** with equipment images (fallback to gradient placeholder)
- **Status Badges** with dynamic icons based on equipment state
- **Warranty Indicators** at the bottom of each card showing:
  - **Garantie OK** (Green) - Warranty valid
  - **Expire bientôt** (Yellow) - Expiring within 10 days with days remaining
  - **Garantie expirée** (Red) - Warranty expired
  - **Non renseignée** (Gray) - No warranty date set
- **Clickable Cards** - Click any card to view full equipment details

### Warranty Management
- Automatic warranty status computation based on expiration date
- Displays days remaining for expiring warranties (shown when ≤10 days left)
- Color-coded warranty status for quick identification
- Computed fields stored in database for performance

### Employee Assignment
- Link equipment to employees
- Assignment workflows with dedicated wizards
- Equipment return process with wizard modal
- Assignment history tracking

### Equipment Organization
- Group equipment by status in kanban view
- Equipment types management
- Department classification
- Tree view for list display
- Form view for detailed editing
- Search functionality

## Technical Architecture

### Models
1. **gestion.equipement** - Main equipment model with warranty computation
2. **gestion.equipement.type** - Equipment type classification
3. **gestion.employee** - Employee records
4. **gestion.department** - Department organization
5. **gestion.assignment.history** - Track all equipment assignments
6. **equipment.assignment.wizard** - Transient model for assignment workflow
7. **equipment.return.wizard** - Transient model for return workflow

### Views
- **Kanban View (Default)** - Visual card-based interface grouped by status
  - Image section (220px height with object-fit:cover)
  - Equipment details (name, type, serial number)
  - Status badge with dynamic icons and colors
  - Employee assignment display (when applicable)
  - Warranty status bar with light backgrounds and proper spacing
- **Tree View** - List view of all equipment with status badges
- **Form View** - Detailed equipment editing interface
- **Search View** - Filter and search capabilities

### Styling & Design
- **Light color scheme** with pastel backgrounds:
  - Available: Light green (#e8f5e9)
  - Assigned: Light blue (#e3f2fd)
  - Repair: Light orange (#fff3e0)
  - Retired: Light red (#ffebee)
- **Spacing**: 12px gaps between cards in status groups
- **Border Radius**: 6-8px rounded corners for modern appearance
- **Shadow Effects**: Subtle box shadows for depth

### Security
- Two user groups: User and Manager
- Admin user included in both security groups
- Access control via ir.model.access.csv

## Installation & Setup

1. Place module in Odoo custom addons folder
2. Update module list in Odoo
3. Install "gestion_equipements" module
4. Module will create:
   - Equipment models and database tables
   - Kanban, tree, form, and search views
   - Security groups and access rules
   - Menu items in Operations section

## Usage

### Adding Equipment
1. Navigate to **Operations > Equipments**
2. Click **Create**
3. Fill in equipment details:
   - Equipment name (required)
   - Serial number (required)
   - Equipment type (required)
   - Purchase date
   - Warranty expiration date
   - Status (default: Available)
   - Upload image (optional)
4. Save

### Assigning Equipment
1. Open any equipment in Kanban view
2. Click the card to open form
3. Use **Assign/Transfer** button to open assignment wizard
4. Select employee and confirm
5. Equipment status automatically changes to "Assigné"

### Returning Equipment
1. Open assigned equipment
2. Click **Return** button (visible only when status is "Assigné")
3. Confirm return in wizard modal
4. Equipment status automatically changes to "Disponible"

### Tracking Warranty
- Warranty status displays automatically on each kanban card
- Color indicators show at a glance:
  - Green = Valid warranty
  - Yellow = Expiring soon (shows days remaining)
  - Red = Warranty expired
  - Gray = No warranty date set
- Days remaining shown only when ≤10 days to expiration

### Managing Equipment Types
1. Navigate to **Operations > Configuration > Equipment Types**
2. Create and manage equipment type categories

### Managing Departments
1. Navigate to **Operations > Configuration > Departments**
2. Create and organize departments

## Database Schema

### gestion_equipement
- nom (Char) - Equipment name
- numero_serie (Char) - Serial number
- type_id (Many2one) - Reference to equipment type
- date_achat (Date) - Purchase date
- date_expiration_garantie (Date) - Warranty expiration
- statut (Selection) - Equipment status
- employee_id (Many2one) - Assigned employee
- image (Image) - Equipment photo
- garantie_status (Computed) - Warranty status (valid/expiring_soon/expired/none)
- garantie_days_left (Computed) - Days remaining until expiration

## XML Compliance

Module is fully compliant with Odoo 17 strict XML validation:
- No `<data>` wrapper tags (Odoo 17 requirement)
- Proper Qweb template syntax for all conditions
- Valid kanban template structure
- All view definitions follow Odoo 17 schema

## Key Implementation Details

### Warranty Computation
```python
@api.depends("date_expiration_garantie")
def _compute_garantie_status(self):
    today = date.today()
    for record in self:
        if not record.date_expiration_garantie:
            record.garantie_status = "none"
            record.garantie_days_left = 0
        else:
            days_left = (record.date_expiration_garantie - today).days
            record.garantie_days_left = days_left
            if days_left < 0:
                record.garantie_status = "expired"
            elif days_left < 30:
                record.garantie_status = "expiring_soon"
            else:
                record.garantie_status = "valid"
```

### Kanban Card Structure
- Clickable link wrapper for navigation
- Image section with 220px fixed height
- Equipment details section with warranty and status
- Color-coded warranty bar at bottom
- Responsive design with flexbox layout

## Future Enhancements

Potential improvements for future versions:
- Equipment maintenance schedules
- Cost tracking and depreciation
- Multi-location support
- Equipment condition ratings
- Audit trail for equipment movements
- Email notifications for warranty expiration
- Equipment export functionality
- Dashboard with KPIs

## Support & Maintenance

For issues or feature requests, refer to the module's git repository or contact the development team.

---

**Last Updated**: 22nd February 2026  
**Odoo Version**: 17  
**Module Status**: Production Ready
**devlopper**: Fatima Ezzahra BOULOUIZ
