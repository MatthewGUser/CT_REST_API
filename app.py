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

# Running the Flask app
if __name__ == '__main__':
    app.run(debug=True)
