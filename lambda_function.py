import os
import json
import shutil
import sqlite3
from datetime import datetime


def get_available_vacations_days(employee_id):
    conn = sqlite3.connect('employee_database.db')
    c = conn.cursor()

    if employee_id:
        c.execute("""
            SELECT employee_vacation_days_available
            FROM vacations
            WHERE employee_id = ?
            ORDER BY year DESC
            LIMIT 1
        """, (employee_id,))

        available_vacation_days = c.fetchone()

        if available_vacation_days:
            available_vacation_days = available_vacation_days[0]
            conn.close()
            return available_vacation_days
        else:
            conn.close()
            return f"No vacation data found for employed_id {employee_id}"
    else:
        conn.close()
        raise Exception("No employee id provided")
