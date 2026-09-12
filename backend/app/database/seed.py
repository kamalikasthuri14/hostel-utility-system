import random
import datetime
from datetime import date, timedelta
import numpy as np
from sqlalchemy.orm import Session

from app.database.connection import engine, SessionLocal, Base
from app.database.models import (
    User, Hostel, Occupancy, UtilityConsumption,
    Alert, Prediction, Maintenance, UtilityRate
)
from app.services.auth_service import get_password_hash
from app.ml.prediction import train_and_save_all_models
from app.ml.anomaly_detection import run_anomaly_detection

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        print('Seeding Utility Rates...')
        rates = [
            UtilityRate(resource_type='Electricity', rate=8.50, unit='kWh'),
            UtilityRate(resource_type='Water', rate=0.04, unit='Litres'),
            UtilityRate(resource_type='Gas', rate=85.00, unit='kg')
        ]
        db.add_all(rates)
        db.commit()

        print('Seeding 8 Hostel Blocks (2,450+ students)...')
        hostel_data = [
            {'name': 'Himalaya Boys Hostel', 'block': 'Block A', 'capacity': 320, 'occupancy': 304, 'location': 'North Campus - Wing A', 'status': 'Active'},
            {'name': 'Nilgiri Boys Hostel', 'block': 'Block B', 'capacity': 300, 'occupancy': 285, 'location': 'North Campus - Wing B', 'status': 'Active'},
            {'name': 'Aravali Girls Hostel', 'block': 'Block C', 'capacity': 350, 'occupancy': 330, 'location': 'South Campus - Wing A', 'status': 'Active'},
            {'name': 'Vindhya Girls Hostel', 'block': 'Block D', 'capacity': 280, 'occupancy': 260, 'location': 'South Campus - Wing B', 'status': 'Active'},
            {'name': 'Shivalik PG & Scholars Hostel', 'block': 'Block E', 'capacity': 300, 'occupancy': 290, 'location': 'East Campus - Research Enclave', 'status': 'Active'},
            {'name': 'Everest International Hostel', 'block': 'Block F', 'capacity': 320, 'occupancy': 310, 'location': 'West Campus - Global Wing', 'status': 'Active'},
            {'name': 'Sahyadri Freshmen Hostel', 'block': 'Block G', 'capacity': 340, 'occupancy': 320, 'location': 'Central Campus - Quad 1', 'status': 'Active'},
            {'name': 'Kailash Senior Residency', 'block': 'Block H', 'capacity': 360, 'occupancy': 351, 'location': 'Central Campus - Quad 2', 'status': 'Active'},
        ]

        hostels = []
        for h in hostel_data:
            obj = Hostel(
                name=h['name'],
                block=h['block'],
                capacity=h['capacity'],
                current_occupancy=h['occupancy'],
                location=h['location'],
                status=h['status']
            )
            db.add(obj)
            hostels.append(obj)
        db.commit()

        for h in hostels:
            db.refresh(h)

        print('Seeding Demo Users...')
        users = [
            User(
                name='Prof. Sharma (Dean / Administrator)',
                email='admin@hostel.edu',
                password_hash=get_password_hash('Admin@123'),
                role='admin',
                assigned_hostel_id=None
            ),
            User(
                name='Dr. Rajiv Mehta (Warden Block A)',
                email='warden.blocka@hostel.edu',
                password_hash=get_password_hash('Warden@123'),
                role='warden',
                assigned_hostel_id=hostels[0].id
            ),
            User(
                name='Dr. Sunita Rao (Warden Block C)',
                email='warden.blockc@hostel.edu',
                password_hash=get_password_hash('Warden@123'),
                role='warden',
                assigned_hostel_id=hostels[2].id
            ),
            User(
                name='Vikram Singh (Chief Maintenance Supervisor)',
                email='maintenance@hostel.edu',
                password_hash=get_password_hash('Maint@123'),
                role='maintenance',
                assigned_hostel_id=None
            )
        ]
        db.add_all(users)
        db.commit()

        print('Generating 180 Days of Daily Occupancy & Utility Records...')
        start_date = date.today() - timedelta(days=180)
        
        elec_rate = 8.50
        water_rate = 0.04
        gas_rate = 85.00

        all_occupancies = []
        all_consumptions = []

        for day_offset in range(181):
            curr_date = start_date + timedelta(days=day_offset)
            dow = curr_date.weekday()
            is_weekend = dow in [5, 6]
            is_mid_sem_exam = (45 <= day_offset <= 55) or (135 <= day_offset <= 145)
            is_vacation = (75 <= day_offset <= 85)

            for h in hostels:
                base_students = h.current_occupancy
                if is_vacation:
                    students = int(base_students * random.uniform(0.35, 0.50))
                elif is_weekend:
                    students = int(base_students * random.uniform(0.82, 0.92))
                elif is_mid_sem_exam:
                    students = int(base_students * random.uniform(0.96, 1.00))
                else:
                    students = int(base_students * random.uniform(0.92, 0.98))

                occ_pct = round((students / h.capacity) * 100, 2)

                occ_record = Occupancy(
                    hostel_id=h.id,
                    date=curr_date,
                    student_count=students,
                    occupancy_percentage=occ_pct
                )
                all_occupancies.append(occ_record)

                season_factor = 1.15 if (curr_date.month in [5, 6, 7, 12, 1]) else 1.00
                weekend_elec_factor = 1.18 if is_weekend else 1.00

                base_water_per_student = random.uniform(92.0, 108.0)
                base_elec_per_student = random.uniform(3.9, 4.8) * season_factor * weekend_elec_factor
                base_gas_per_student = random.uniform(0.12, 0.15)

                water_vol = students * base_water_per_student
                elec_kwh = students * base_elec_per_student
                gas_wt = students * base_gas_per_student

                # Inject Anomaly 1: Block C Water leak in last 3 days
                if h.block == 'Block C' and day_offset >= 178:
                    water_vol *= 1.72

                # Inject Anomaly 2: Block A Electricity surge
                if h.block == 'Block A' and 176 <= day_offset <= 179:
                    elec_kwh *= 1.48

                # Inject Anomaly 3: Block D Gas surge
                if h.block == 'Block D' and 174 <= day_offset <= 176:
                    gas_wt *= 1.62

                water_vol = round(water_vol + random.uniform(-40, 40), 1)
                elec_kwh = round(elec_kwh + random.uniform(-10, 10), 1)
                gas_wt = round(gas_wt + random.uniform(-1, 1), 2)

                w_cost = round(water_vol * water_rate, 2)
                e_cost = round(elec_kwh * elec_rate, 2)
                g_cost = round(gas_wt * gas_rate, 2)
                tot_cost = round(w_cost + e_cost + g_cost, 2)

                cons_record = UtilityConsumption(
                    hostel_id=h.id,
                    date=curr_date,
                    water_litres=water_vol,
                    electricity_kwh=elec_kwh,
                    gas_kg=gas_wt,
                    water_cost=w_cost,
                    electricity_cost=e_cost,
                    gas_cost=g_cost,
                    total_cost=tot_cost
                )
                all_consumptions.append(cons_record)

        db.bulk_save_objects(all_occupancies)
        db.bulk_save_objects(all_consumptions)
        db.commit()

        print('Seeding Initial Maintenance Issues...')
        maintenance_tickets = [
            Maintenance(
                hostel_id=hostels[2].id,
                resource_type='Water',
                issue_type='Overhead Pipeline Rupture',
                description='Sudden water flow surge of +72% detected by Isolation Forest. Water pressure drop reported on 3rd floor washrooms.',
                priority='Critical',
                assigned_to='Vikram Singh',
                status='In Progress',
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=1),
                notes='Plumber on site isolating valve line 3B.'
            ),
            Maintenance(
                hostel_id=hostels[0].id,
                resource_type='Electricity',
                issue_type='Geyser Thermostat Stuck',
                description='Wing 2 central solar-electric hybrid geysers drawing continuous 45 kW during non-peak hours.',
                priority='High',
                assigned_to='Vikram Singh',
                status='Assigned',
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=2),
                notes='Replacement thermostat requisitioned from inventory.'
            ),
            Maintenance(
                hostel_id=hostels[3].id,
                resource_type='Gas',
                issue_type='LPG Regulator Pressure Drift',
                description='Commercial kitchen LPG manifold showing high flow rate anomaly. Suspected burner seal leakage.',
                priority='Medium',
                assigned_to='Vikram Singh',
                status='Resolved',
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=5),
                resolved_at=datetime.datetime.utcnow() - datetime.timedelta(days=4),
                notes='Replaced faulty regulator gasket and recalibrated pressure gauge.'
            ),
            Maintenance(
                hostel_id=hostels[1].id,
                resource_type='Water',
                issue_type='Sump Pump Motor Vibration',
                description='Underground booster pump drawing 20% extra current during filling cycle.',
                priority='Low',
                assigned_to='Vikram Singh',
                status='Open',
                created_at=datetime.datetime.utcnow() - datetime.timedelta(days=3),
                notes='Scheduled for routine lubrication and bearing check.'
            )
        ]
        db.add_all(maintenance_tickets)
        db.commit()

        print('Training Machine Learning Models (Random Forest & Linear Regression)...')
        train_res = train_and_save_all_models(db)
        print(f'ML Training Status: {train_res}')

        print('Running Anomaly Detection Pipeline to generate live alerts...')
        run_anomaly_detection(db)

        print('Seed completed successfully! Total hostels: 8, Students: 2,450, Records: 1,448+')

    except Exception as e:
        db.rollback()
        print(f'Error during seeding: {e}')
        raise e
    finally:
        db.close()

if __name__ == '__main__':
    seed_database()
