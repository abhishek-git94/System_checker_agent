# features/medicine_reminder.py
import json
import os
from datetime import datetime, time
from dataclasses import dataclass, asdict
from typing import List, Optional

DATA_FILE = "medicine_data.json"

@dataclass
class Medicine:
    name: str
    dosage: str
    frequency: str
    times: List[str]
    start_date: str
    end_date: Optional[str]
    notes: str
    created_at: str

def load_medicines() -> List[Medicine]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return [Medicine(**m) for m in data]
    except:
        return []

def save_medicines(medicines: List[Medicine]):
    with open(DATA_FILE, "w") as f:
        json.dump([asdict(m) for m in medicines], f, indent=2)

def add_medicine(name: str, dosage: str, frequency: str, times: List[str], 
                 start_date: str, end_date: str = None, notes: str = "") -> str:
    medicines = load_medicines()
    medicine = Medicine(
        name=name,
        dosage=dosage,
        frequency=frequency,
        times=times,
        start_date=start_date,
        end_date=end_date,
        notes=notes,
        created_at=datetime.now().isoformat()
    )
    medicines.append(medicine)
    save_medicines(medicines)
    return f"Medicine '{name}' added successfully!"

def remove_medicine(name: str) -> str:
    medicines = load_medicines()
    original_count = len(medicines)
    medicines = [m for m in medicines if m.name.lower() != name.lower()]
    if len(medicines) == original_count:
        return f"Medicine '{name}' not found."
    save_medicines(medicines)
    return f"Medicine '{name}' removed."

def get_all_medicines() -> List[Medicine]:
    return load_medicines()

def get_todays_schedule() -> str:
    medicines = load_medicines()
    if not medicines:
        return "No medicines scheduled for today."
    
    result = "💊 **Today's Medicine Schedule:**\n\n"
    for med in medicines:
        result += f"**{med.name}** - {med.dosage}\n"
        result += f"   Time: {', '.join(med.times)}\n"
        result += f"   Frequency: {med.frequency}\n"
        if med.notes:
            result += f"   Note: {med.notes}\n"
        result += "\n"
    return result

def format_medicine_list() -> str:
    medicines = get_all_medicines()
    if not medicines:
        return "No medicines added yet."
    
    result = "💊 **Your Medicines:**\n\n"
    for i, med in enumerate(medicines, 1):
        result += f"{i}. **{med.name}**\n"
        result += f"   Dosage: {med.dosage}\n"
        result += f"   Time: {', '.join(med.times)}\n\n"
    return result