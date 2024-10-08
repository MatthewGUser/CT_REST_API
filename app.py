from flask import Flask, request, jsonify
from models import get_db_connection
import mysql.connector

app = Flask(__name__)

# 1. Add a Member
@app.route('/members', methods=['POST'])
def add_member():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Members (name, email) VALUES (%s, %s)', (name, email))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Member added successfully!'}), 201
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Email already exists!'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. Get a Member by ID
@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM Members WHERE id = %s', (id,))
        member = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if member:
            return jsonify(member), 200
        else:
            return jsonify({'error': 'Member not found!'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. Update a Member
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Prepare update statement based on which fields are provided
        updates = []
        values = []
        
        if name:
            updates.append("name = %s")
            values.append(name)
        if email:
            updates.append("email = %s")
            values.append(email)
        
        if updates:
            values.append(id)  # Add ID for the WHERE clause
            cursor.execute(f'UPDATE Members SET {", ".join(updates)} WHERE id = %s', tuple(values))
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({'message': 'Member updated successfully!'}), 200
        else:
            return jsonify({'error': 'No data provided for update!'}), 400
            
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Email already exists!'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. Delete a Member
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Members WHERE id = %s', (id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            return jsonify({'error': 'Member not found!'}), 404
        
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Member deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# 1. Add a Workout Session
@app.route('/workouts', methods=['POST'])
def add_workout():
    try:
        data = request.get_json()
        member_id = data['member_id']
        session_date = data['session_date']
        duration = data['duration']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO WorkoutSessions (member_id, session_date, duration) VALUES (%s, %s, %s)', 
                       (member_id, session_date, duration))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Workout session scheduled successfully!'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. Get a Workout Session by ID
@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM WorkoutSessions WHERE id = %s', (id,))
        workout = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if workout:
            return jsonify(workout), 200
        else:
            return jsonify({'error': 'Workout session not found!'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. Get All Workout Sessions for a Specific Member
@app.route('/members/<int:member_id>/workouts', methods=['GET'])
def get_workouts_for_member(member_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM WorkoutSessions WHERE member_id = %s', (member_id,))
        workouts = cursor.fetchall()
        cursor.close()
        conn.close()

        if workouts:
            return jsonify(workouts), 200
        else:
            return jsonify({'message': 'No workout sessions found for this member.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 4. Update a Workout Session
@app.route('/workouts/<int:id>', methods=['PUT'])
def update_workout(id):
    try:
        data = request.get_json()
        session_date = data['session_date']
        duration = data['duration']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE WorkoutSessions SET session_date = %s, duration = %s WHERE id = %s',
                       (session_date, duration, id))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'message': 'Workout session updated successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 5. Delete a Workout Session
@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM WorkoutSessions WHERE id = %s', (id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Workout session not found!'}), 404

        cursor.close()
        conn.close()

        return jsonify({'message': 'Workout session deleted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
