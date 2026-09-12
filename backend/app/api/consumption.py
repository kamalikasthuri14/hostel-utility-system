import io
import csv
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Response
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import UtilityConsumption, Occupancy, Hostel, User
from app.schemas.schemas import ConsumptionCreate, ConsumptionUpdate, ConsumptionResponse
from app.services.auth_service import get_current_user, require_role
from app.ml.prediction import get_utility_rate

router = APIRouter(prefix="/api/consumption", tags=["Utility Consumption"])

@router.get("", response_model=List[ConsumptionResponse])
def get_consumption_records(
    hostel_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = Query(100, le=1000),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(
        UtilityConsumption,
        Hostel.name.label("hostel_name"),
        Hostel.block.label("hostel_block"),
        Occupancy.student_count
    ).join(
        Hostel, UtilityConsumption.hostel_id == Hostel.id
    ).outerjoin(
        Occupancy, (UtilityConsumption.hostel_id == Occupancy.hostel_id) & (UtilityConsumption.date == Occupancy.date)
    )

    if current_user.role == "warden" and current_user.assigned_hostel_id:
        query = query.filter(UtilityConsumption.hostel_id == current_user.assigned_hostel_id)
    elif hostel_id:
        query = query.filter(UtilityConsumption.hostel_id == hostel_id)

    if start_date:
        query = query.filter(UtilityConsumption.date >= start_date)
    if end_date:
        query = query.filter(UtilityConsumption.date <= end_date)

    records = query.order_by(UtilityConsumption.date.desc(), UtilityConsumption.hostel_id.asc()).offset(offset).limit(limit).all()

    results = []
    for r in records:
        cons = r.UtilityConsumption
        students = r.student_count or 250
        results.append(ConsumptionResponse(
            id=cons.id,
            hostel_id=cons.hostel_id,
            hostel_name=r.hostel_name,
            hostel_block=r.hostel_block,
            date=cons.date,
            student_count=students,
            water_litres=cons.water_litres,
            electricity_kwh=cons.electricity_kwh,
            gas_kg=cons.gas_kg,
            water_cost=cons.water_cost,
            electricity_cost=cons.electricity_cost,
            gas_cost=cons.gas_cost,
            total_cost=cons.total_cost,
            water_per_student=round(cons.water_litres / max(students, 1), 1),
            electricity_per_student=round(cons.electricity_kwh / max(students, 1), 2),
            gas_per_student=round(cons.gas_kg / max(students, 1), 3)
        ))
    return results

@router.post("", response_model=ConsumptionResponse)
def create_consumption_record(payload: ConsumptionCreate, current_user: User = Depends(require_role("admin", "warden")), db: Session = Depends(get_db)):
    hostel = db.query(Hostel).filter(Hostel.id == payload.hostel_id).first()
    if not hostel:
        raise HTTPException(status_code=404, detail="Hostel not found")

    w_rate = get_utility_rate(db, "Water")
    e_rate = get_utility_rate(db, "Electricity")
    g_rate = get_utility_rate(db, "Gas")

    w_cost = round(payload.water_litres * w_rate, 2)
    e_cost = round(payload.electricity_kwh * e_rate, 2)
    g_cost = round(payload.gas_kg * g_rate, 2)
    tot_cost = round(w_cost + e_cost + g_cost, 2)

    rec = UtilityConsumption(
        hostel_id=payload.hostel_id,
        date=payload.date,
        water_litres=payload.water_litres,
        electricity_kwh=payload.electricity_kwh,
        gas_kg=payload.gas_kg,
        water_cost=w_cost,
        electricity_cost=e_cost,
        gas_cost=g_cost,
        total_cost=tot_cost
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    occ = db.query(Occupancy).filter(Occupancy.hostel_id == payload.hostel_id, Occupancy.date == payload.date).first()
    students = occ.student_count if occ else hostel.current_occupancy

    return ConsumptionResponse(
        id=rec.id,
        hostel_id=rec.hostel_id,
        hostel_name=hostel.name,
        hostel_block=hostel.block,
        date=rec.date,
        student_count=students,
        water_litres=rec.water_litres,
        electricity_kwh=rec.electricity_kwh,
        gas_kg=rec.gas_kg,
        water_cost=rec.water_cost,
        electricity_cost=rec.electricity_cost,
        gas_cost=rec.gas_cost,
        total_cost=rec.total_cost,
        water_per_student=round(rec.water_litres / max(students, 1), 1),
        electricity_per_student=round(rec.electricity_kwh / max(students, 1), 2),
        gas_per_student=round(rec.gas_kg / max(students, 1), 3)
    )

@router.put("/{id}", response_model=ConsumptionResponse)
def update_consumption_record(id: int, payload: ConsumptionUpdate, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    rec = db.query(UtilityConsumption).filter(UtilityConsumption.id == id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")

    w_rate = get_utility_rate(db, "Water")
    e_rate = get_utility_rate(db, "Electricity")
    g_rate = get_utility_rate(db, "Gas")

    if payload.water_litres is not None:
        rec.water_litres = payload.water_litres
        rec.water_cost = round(rec.water_litres * w_rate, 2)

    if payload.electricity_kwh is not None:
        rec.electricity_kwh = payload.electricity_kwh
        rec.electricity_cost = round(rec.electricity_kwh * e_rate, 2)

    if payload.gas_kg is not None:
        rec.gas_kg = payload.gas_kg
        rec.gas_cost = round(rec.gas_kg * g_rate, 2)

    rec.total_cost = round(rec.water_cost + rec.electricity_cost + rec.gas_cost, 2)
    db.commit()
    db.refresh(rec)

    hostel = db.query(Hostel).filter(Hostel.id == rec.hostel_id).first()
    occ = db.query(Occupancy).filter(Occupancy.hostel_id == rec.hostel_id, Occupancy.date == rec.date).first()
    students = occ.student_count if occ else (hostel.current_occupancy if hostel else 250)

    return ConsumptionResponse(
        id=rec.id,
        hostel_id=rec.hostel_id,
        hostel_name=hostel.name if hostel else "Block",
        hostel_block=hostel.block if hostel else "",
        date=rec.date,
        student_count=students,
        water_litres=rec.water_litres,
        electricity_kwh=rec.electricity_kwh,
        gas_kg=rec.gas_kg,
        water_cost=rec.water_cost,
        electricity_cost=rec.electricity_cost,
        gas_cost=rec.gas_cost,
        total_cost=rec.total_cost,
        water_per_student=round(rec.water_litres / max(students, 1), 1),
        electricity_per_student=round(rec.electricity_kwh / max(students, 1), 2),
        gas_per_student=round(rec.gas_kg / max(students, 1), 3)
    )

@router.delete("/{id}")
def delete_consumption_record(id: int, current_user: User = Depends(require_role("admin")), db: Session = Depends(get_db)):
    rec = db.query(UtilityConsumption).filter(UtilityConsumption.id == id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(rec)
    db.commit()
    return {"status": "success", "message": "Consumption record deleted successfully"}

@router.post("/upload-csv")
async def upload_consumption_csv(
    file: UploadFile = File(...),
    current_user: User = Depends(require_role("admin", "warden")),
    db: Session = Depends(get_db)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only .csv files are supported")

    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    reader = csv.DictReader(io.StringIO(text))
    hostels_by_block = {h.block.lower(): h.id for h in db.query(Hostel).all()}
    hostels_by_name = {h.name.lower(): h.id for h in db.query(Hostel).all()}

    w_rate = get_utility_rate(db, "Water")
    e_rate = get_utility_rate(db, "Electricity")
    g_rate = get_utility_rate(db, "Gas")

    inserted_count = 0
    errors = []

    for idx, row in enumerate(reader, start=2):
        try:
            raw_hostel = (row.get("hostel") or row.get("block") or row.get("hostel_id") or "").strip()
            if not raw_hostel:
                errors.append(f"Row {idx}: Missing hostel identifier")
                continue

            hostel_id = None
            if raw_hostel.isdigit():
                hostel_id = int(raw_hostel)
            elif raw_hostel.lower() in hostels_by_block:
                hostel_id = hostels_by_block[raw_hostel.lower()]
            elif raw_hostel.lower() in hostels_by_name:
                hostel_id = hostels_by_name[raw_hostel.lower()]

            if not hostel_id:
                errors.append(f"Row {idx}: Hostel '{raw_hostel}' not recognized")
                continue

            raw_date = row.get("date", "").strip()
            rec_date = datetime.strptime(raw_date, "%Y-%m-%d").date()

            water = float(row.get("water_litres") or row.get("water") or 0)
            elec = float(row.get("electricity_kwh") or row.get("electricity") or 0)
            gas = float(row.get("gas_kg") or row.get("gas") or 0)

            if water < 0 or elec < 0 or gas < 0:
                errors.append(f"Row {idx}: Negative consumption values not allowed")
                continue

            w_cost = round(water * w_rate, 2)
            e_cost = round(elec * e_rate, 2)
            g_cost = round(gas * g_rate, 2)
            tot_cost = round(w_cost + e_cost + g_cost, 2)

            rec = UtilityConsumption(
                hostel_id=hostel_id,
                date=rec_date,
                water_litres=water,
                electricity_kwh=elec,
                gas_kg=gas,
                water_cost=w_cost,
                electricity_cost=e_cost,
                gas_cost=g_cost,
                total_cost=tot_cost
            )
            db.add(rec)
            inserted_count += 1
        except Exception as e:
            errors.append(f"Row {idx}: {str(e)}")

    db.commit()

    return {
        "status": "success",
        "inserted_records": inserted_count,
        "errors": errors[:10],
        "total_errors": len(errors)
    }

@router.get("/export-csv")
def export_consumption_csv(
    hostel_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(
        UtilityConsumption,
        Hostel.name.label("hostel_name"),
        Hostel.block.label("hostel_block")
    ).join(Hostel, UtilityConsumption.hostel_id == Hostel.id)

    if current_user.role == "warden" and current_user.assigned_hostel_id:
        query = query.filter(UtilityConsumption.hostel_id == current_user.assigned_hostel_id)
    elif hostel_id:
        query = query.filter(UtilityConsumption.hostel_id == hostel_id)

    records = query.order_by(UtilityConsumption.date.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Record_ID", "Hostel_Name", "Block", "Date",
        "Water_Litres", "Electricity_kWh", "Gas_kg",
        "Water_Cost_INR", "Electricity_Cost_INR", "Gas_Cost_INR", "Total_Cost_INR"
    ])

    for r in records:
        c = r.UtilityConsumption
        writer.writerow([
            c.id, r.hostel_name, r.hostel_block, str(c.date),
            c.water_litres, c.electricity_kwh, c.gas_kg,
            c.water_cost, c.electricity_cost, c.gas_cost, c.total_cost
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=hostel_utility_consumption.csv"}
    )
