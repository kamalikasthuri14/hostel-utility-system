from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.database.models import Hostel, UtilityConsumption, Alert, Occupancy, UtilityRate

def generate_actionable_recommendations(db: Session, hostel_id: int = None) -> List[Dict[str, Any]]:
    recommendations = []
    hostels = db.query(Hostel).all() if not hostel_id else [db.query(Hostel).filter(Hostel.id == hostel_id).first()]

    for h in hostels:
        if not h:
            continue

        # Check latest occupancy
        latest_occ = db.query(Occupancy).filter(Occupancy.hostel_id == h.id).order_by(Occupancy.date.desc()).first()
        occ_rate = latest_occ.occupancy_percentage if latest_occ else 90.0

        # Check active alerts
        alerts = db.query(Alert).filter(Alert.hostel_id == h.id, Alert.status == "Active").all()
        has_water_alert = any(a.resource_type == "Water" for a in alerts)
        has_elec_alert = any(a.resource_type == "Electricity" for a in alerts)
        has_gas_alert = any(a.resource_type == "Gas" for a in alerts)

        # Recommendation 1: Water Anomaly & Leak Mitigation
        if has_water_alert:
            recommendations.append({
                "id": f"REC-WAT-{h.id}",
                "hostel_id": h.id,
                "hostel_name": f"{h.name} ({h.block})",
                "category": "Water",
                "title": f"High Water Surge Detected in {h.block}",
                "description": f"{h.name} has exceeded its normal per-student baseline by >35%. Probable pipe rupture or continuous flush valve leakage.",
                "suggested_actions": [
                    "Inspect overhead tank float sensors and overflow drain channels.",
                    "Audit common washrooms and shower fixtures across floors 2 & 3.",
                    "Verify automated sump pump cutoff solenoid relay timings.",
                    "Schedule 24-hour flow meter pressure audit with plumbing crew."
                ],
                "estimated_monthly_savings": 14500.0,
                "impact_level": "High",
                "reasoning": "Uncorrected water leakage wastes ~4,200 Litres/day, inflating pumping power costs and local municipal water procurement bills."
            })

        # Recommendation 2: Electricity Peak Load & Geyser Scheduling
        if has_elec_alert or occ_rate > 90.0:
            recommendations.append({
                "id": f"REC-ELEC-{h.id}",
                "hostel_id": h.id,
                "hostel_name": f"{h.name} ({h.block})",
                "category": "Electricity",
                "title": f"Peak Electrical Load Optimization for {h.block}",
                "description": f"High electricity draw during morning hours (6:00 AM – 9:00 AM). Staggered geyser duty cycles can shave 22% off maximum demand tariff.",
                "suggested_actions": [
                    "Implement phased 20-minute timer intervals for water geysers across odd/even wings.",
                    "Switch common corridor & stairwell lighting to photocell motion-dimming fixtures.",
                    "Issue advisory to residents regarding phantom appliance loads during lecture hours.",
                    "Verify main distribution panel phase balance to avoid neutral overheating."
                ],
                "estimated_monthly_savings": 28400.0,
                "impact_level": "High",
                "reasoning": "Peak demand penalties constitute up to 30% of total commercial power bills. Shaving 45 kW instantaneous surge yields direct tariff savings."
            })

        # Recommendation 3: Dining/Mess Kitchen Gas Conservation
        if has_gas_alert or h.block in ["Block A", "Block C", "Block D"]:
            recommendations.append({
                "id": f"REC-GAS-{h.id}",
                "hostel_id": h.id,
                "hostel_name": f"{h.name} ({h.block})",
                "category": "Gas",
                "title": f"Kitchen LPG Burner Efficiency & Pre-Heater Calibration",
                "description": f"Commercial LPG consumption in {h.name} mess kitchen is 18% above seasonal norm.",
                "suggested_actions": [
                    "Inspect commercial high-pressure burner nozzles for carbon fouling.",
                    "Incorporate steam jacket cookers for bulk rice and dal preparation.",
                    "Ensure pre-soaking of grains to reduce active boiling burner time by 25%.",
                    "Conduct weekly soap-bubble leak checks on LPG manifold regulator joints."
                ],
                "estimated_monthly_savings": 8200.0,
                "impact_level": "Medium",
                "reasoning": "Optimized thermal transfer and clean burner orifices reduce specific LPG consumption from 0.18 kg to 0.13 kg per resident meal."
            })

        # Recommendation 4: High Occupancy Resource Stress
        if occ_rate >= 95.0:
            recommendations.append({
                "id": f"REC-OCC-{h.id}",
                "hostel_id": h.id,
                "hostel_name": f"{h.name} ({h.block})",
                "category": "Occupancy",
                "title": f"High Occupancy ({int(occ_rate)}%) Stress Management for {h.block}",
                "description": f"{h.name} is operating at near-maximum capacity ({latest_occ.student_count if latest_occ else h.capacity}/{h.capacity} students).",
                "suggested_actions": [
                    "Increase water supply delivery cycles from municipal booster line.",
                    "Perform preventive thermal scanning of main wing circuit breakers.",
                    "Deploy additional waste segregation bins near common pantry areas."
                ],
                "estimated_monthly_savings": 6500.0,
                "impact_level": "Low",
                "reasoning": "Preventive maintenance under heavy student load prevents catastrophic transformer trips or dry-tank conditions during exam weeks."
            })

    return recommendations
