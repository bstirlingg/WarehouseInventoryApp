# Light Logistics Inventory Management

A Python application for managing warehouse inventory. Users can:

- Add new sections and items  
- Modify existing item quantities  
- Move inventory between sections  
- View an overview of all sections and their items in one place  

---

## Features

- **Welcome Screen**  
  - Provides an initial entry point for the user  

- **Single Main Window**  
  - Displays a table of existing sections and items  
  - Offers buttons to **Manage Inventory** (add/update items) and **Move Inventory** between sections  

- **Dialogs**  
  - **Manage Inventory**: Add new items or update existing quantities (including optional expiry dates)  
  - **Move Inventory**: Transfer stock between sections, including partial quantities  

- **Error Handling**  
  - Notifies the user of invalid operations (e.g., incorrect quantity)  

---

## User Journey Flow

**Below is a visual interpretation of the expected User journey flow for this application:**  

```mermaid
flowchart TB
    A(["Application Start"]) --> B(["Create WarehouseApp (Hidden)"])
    B --> C(["Display WelcomeScreen (Toplevel)"])
    C -->|User clicks 'Enter'| D(["WelcomeScreen Destroyed"])
    D --> E(["Main Window (WarehouseApp) Deiconified"])
    E --> F(["Inventory Overview (Sections/Items Table)"])
    E --> G(["User clicks 'Manage Inventory'"])
    G --> H(["ManageInventoryModal Opens"])
    H -->|Submit/Cancel| E
    E --> I(["User clicks 'Move Inventory'"])
    I --> J(["MoveInventoryModal Opens"])
    J -->|Submit/Cancel| E
```

---
## System Architecture 

**Below is a visual interpretation of the expected System Architecture for this application:**  

```mermaid
flowchart LR
    subgraph main_py["main.py"]
        A[WarehouseApp]
        B[InventoryOverviewFrame]
        C[ManageInventoryModal]
        D[MoveInventoryModal]
        E[WelcomeScreen]
    end

    subgraph inventorymgmt["InventoryManagement.py"]
        IM[InventoryManager]
    end

    subgraph sections_py["Sections.py"]
        Sec[InventorySection]
    end

    subgraph regularitems_py["RegularItems.py"]
        RegItem[RegularItem]
        PerItem[PerishableItem]
    end

    subgraph baseitem_py["BaseInventoryItem.py"]
        BaseItem[InventoryItem]
    end

    %% Relationships in main.py
    E -->|Closes to reveal| A
    A --> IM
    B --> IM
    C --> IM
    D --> IM

    %% InventoryManager uses Section logic
    IM --> Sec

    %% Sections use item classes
    Sec --> RegItem
    Sec --> PerItem

    %% Both RegularItem & PerishableItem inherit from InventoryItem
    RegItem --> BaseItem
    PerItem --> BaseItem
```

---

## Requirements

1. **Python 3.8+** (3.10+ recommended)  
2. **Dependencies**:  
   - [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)  
   - [Pillow (PIL)](https://pypi.org/project/Pillow/)

Install them via:
```bash
pip install customtkinter Pillow