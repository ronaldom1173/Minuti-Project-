from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from config import DB_CONFIG
from datetime import datetime
from werkzeug.security import check_password_hash
import datetime
from datetime import datetime, timedelta


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

try:
    conn = mysql.connector.connect(**DB_CONFIG)
    print("✅ Connected to MySQL Workbench Database Successfully!")
    conn.close()
except mysql.connector.Error as err:
    print(f"❌ Error: {err}")

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

# ------------------------ PRODUCTS ------------------------

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM PRODUCT ORDER BY name ASC")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/products', methods=['POST'])
def create_product():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO PRODUCT (name, description, category, base_price, active, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
    """, (
        data['name'],
        data.get('description', ''),
        data.get('category', ''),
        data['base_price'],
        int(data['active']),
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product created successfully'}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE PRODUCT
        SET name=%s, description=%s, category=%s, base_price=%s, active=%s, updated_at=NOW()
        WHERE product_id=%s
    """, (
        data['name'],
        data.get('description', ''),
        data.get('category', ''),
        data['base_price'],
        int(data['active']),
        product_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product updated successfully'})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM PRODUCT WHERE product_id = %s", (product_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Product deleted successfully'})

# ------------------------ WASTE ------------------------

@app.route('/waste', methods=['GET'])
def get_waste():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            w.waste_id,
            w.product_id,
            p.name,
            w.quantity,
            w.reason,
            w.waste_date,
            w.notes
        FROM WASTE w
        JOIN PRODUCT p ON w.product_id = p.product_id
        ORDER BY w.waste_date DESC
    """)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/waste', methods=['POST'])
def create_waste():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO WASTE (product_id, quantity, reason, waste_date, notes, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
    """, (
        data['product_id'],
        data['quantity'],
        data['reason'],
        data['waste_date'],
        data.get('notes', '')
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Waste entry created successfully'}), 201

@app.route('/waste/<int:waste_id>', methods=['PUT'])
def update_waste(waste_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE WASTE
        SET product_id=%s,
            quantity=%s,
            reason=%s,
            waste_date=%s,
            notes=%s,
            updated_at=NOW()
        WHERE waste_id=%s
    """, (
        data['product_id'],
        data['quantity'],
        data['reason'],
        data['waste_date'],
        data.get('notes', ''),
        waste_id
    ))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Waste entry updated successfully'})

@app.route('/waste/<int:waste_id>', methods=['DELETE'])
def delete_waste(waste_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM WASTE WHERE waste_id = %s", (waste_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'message': 'Waste entry deleted successfully'})



#---------------------------------------------------------------------------------------------------

@app.route('/weekly-wasteproduct', methods=['GET'])
def get_weekly_wasteProducts():
    query = "SELECT * FROM waste_summary_per_product"
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/wasteByReason', methods=['GET'])
def get_wasteByReason():
    query = "SELECT * FROM waste_by_reason"
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


@app.route('/WasteCostView', methods=['GET'])
def get_WasteCostView():
    query = "SELECT * FROM WasteCostView"
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# edited to aggregate by product
@app.route('/all-waste-cost', methods=['GET'])
def get_waste_cost():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    query = """
        SELECT 
            product_name,
            SUM(total_quantity) as total_quantity,
            base_price,
            SUM(total_cost_lost) as total_cost_lost
        FROM WasteCostView_AllTime
        WHERE waste_date BETWEEN %s AND %s
        GROUP BY product_name, base_price
        ORDER BY product_name
    """

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (start_date, end_date))
            result = cursor.fetchall()
    
    return jsonify(result)


@app.route('/all-waste-by-reason', methods=['GET'])
def get_waste_by_reason():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    query = """
        SELECT reason, SUM(total_quantity) AS total_quantity
        FROM waste_by_reason_all_time
        WHERE waste_date BETWEEN %s AND %s
        GROUP BY reason
    """

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (start_date, end_date))
            result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/all-waste-summary-per-product', methods=['GET'])
def get_waste_summary_per_product():
    
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    query = """
        SELECT product_name, SUM(total_quantity_wasted) AS total_quantity
        FROM waste_summary_per_product_all_time
        WHERE waste_date BETWEEN %s AND %s
        GROUP BY product_name
    """

    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(query, (start_date, end_date))
            result = cursor.fetchall()
    
    return jsonify(result)

@app.route('/top-wasted-products-30days')
def top_wasted_products():
    import datetime
    conn = get_db_connection() 
    thirty_days_ago = datetime.datetime.now() - datetime.timedelta(days=30)

    query = """
    SELECT 
        p.name, 
        SUM(w.quantity) as total_quantity
    FROM WASTE w
    JOIN PRODUCT p ON p.product_id = w.product_id
    WHERE w.waste_date >= %s
    GROUP BY w.product_id
    ORDER BY total_quantity DESC
    LIMIT 10;
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, (thirty_days_ago,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/overproduction-estimate-30days')
def get_overproduction_estimate():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = """
            SELECT p.name, p.category, w.waste_date, w.quantity
            FROM WASTE w
            JOIN PRODUCT p ON p.product_id = w.product_id
            WHERE w.reason = 'EXPIRED' AND w.waste_date >= NOW() - INTERVAL 30 DAY
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        days = {
            "Monday": {}, "Tuesday": {}, "Wednesday": {},
            "Thursday": {}, "Friday": {}, "Saturday": {}, "Sunday": {}
        }

        for row in rows:
            shelf_life = 3 if row["category"].lower() == "pastry" else 2
            production_date = row["waste_date"] - timedelta(days=shelf_life)
            day = production_date.strftime('%A')
            key = row["name"]
            qty = row.get("quantity", 1)

            if key in days[day]:
                days[day][key] += qty
            else:
                days[day][key] = qty

        filtered_days = {}

        for day, product_dict in days.items():
            total_qty = sum(product_dict.values())
            if total_qty >= 3:
                filtered_days[day] = [f"{name} ({qty})" for name, qty in product_dict.items()]

        return jsonify(filtered_days)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


'''@app.route('/api/sales_profit', methods=['GET'])
def get_sales_profit():
    db = get_db_connection()
    selected_date = request.args.get('date')
    if not selected_date:
        return jsonify({'error': 'Missing "date" parameter'}), 400

    query = """
        SELECT * 
        FROM daily_sales_profit 
        WHERE DATE(transaction_date) = %s
    """

    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query, (selected_date,))
        result = cursor.fetchall()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/weekly-sales', methods=['GET'])
def get_weekly_sales():
    year_week = 0
    def get_last_week_yearweek():
        last_week_date = datetime.date.today() - datetime.timedelta(days=7)
        iso_year, iso_week, _ = last_week_date.isocalendar()  # returns (year, week, weekday)
        return int(f"{iso_year}{iso_week:02d}")
    year_week = get_last_week_yearweek()
    print("Fetching report for year_week:", year_week)


    query = "SELECT * FROM weekly_sales_profit WHERE year_week = %s"
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, (year_week,))
        results = cursor.fetchall()
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
'''

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
    user = cursor.fetchone()
    
    cursor.close()
    db.close()

    if user and check_password_hash(user['password'], password):
        return jsonify({
            "message": "Login successful",
            "role": user['role'],
            "username": user['username']
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/export-waste-csv', methods=['GET'])
def export_waste_csv():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "start_date and end_date are required"}), 400

    query = """
        SELECT 
            w.waste_id,
            p.name as product_name,
            w.quantity,
            w.reason,
            w.waste_date,
            p.base_price,
            (w.quantity * p.base_price) as total_cost,
            w.notes
        FROM WASTE w
        JOIN PRODUCT p ON w.product_id = p.product_id
        WHERE w.waste_date BETWEEN %s AND %s
        ORDER BY w.waste_date DESC
    """

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(query, (start_date, end_date))
        waste_data = cursor.fetchall()
        
        # Create a string buffer for CSV data
        from io import StringIO
        import csv
        
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header row
        if waste_data:
            writer.writerow(waste_data[0].keys())
            
            # Write data rows
            for row in waste_data:
                # Format date properly
                if 'waste_date' in row and row['waste_date']:
                    if isinstance(row['waste_date'], str):
                        # If it's already a string, keep it
                        pass
                    else:
                        # If it's a datetime object, format it
                        row['waste_date'] = row['waste_date'].strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow(row.values())
        
        # Prepare response
        output = si.getvalue()
        
        # Create response with appropriate headers for CSV download
        from flask import Response
        filename = f"waste_report_{start_date}_to_{end_date}.csv"
        return Response(
            output,
            mimetype="text/csv",
            headers={"Content-Disposition": f"attachment;filename={filename}"}
        )
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
