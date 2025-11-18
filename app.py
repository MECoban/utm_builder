from flask import Flask, render_template, request, jsonify
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Database dosya yolu
DATABASE = 'utm_links.db'

def get_db_connection():
    """Veritabanı bağlantısı oluştur"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Veritabanını başlat ve gerekirse güncelle"""
    conn = get_db_connection()
    
    # Tabloyu oluştur (yoksa)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS utm_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_url TEXT NOT NULL,
            utm_source TEXT NOT NULL,
            utm_medium TEXT NOT NULL,
            utm_campaign TEXT NOT NULL,
            utm_term TEXT,
            utm_content TEXT,
            utm_url TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # launch_group sütununu ekle (yoksa)
    try:
        conn.execute('ALTER TABLE utm_links ADD COLUMN launch_group TEXT')
        print("✅ launch_group sütunu eklendi!")
    except sqlite3.OperationalError:
        # Sütun zaten varsa hata vermesin
        pass
    
    conn.commit()
    conn.close()
    print("✅ Veritabanı hazır!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/links')
def links():
    """Kaydedilen linkleri göster"""
    return render_template('links.html')

@app.route('/api/links', methods=['GET'])
def get_links():
    """Tüm linkleri getir"""
    try:
        conn = get_db_connection()
        links = conn.execute(
            'SELECT * FROM utm_links ORDER BY created_at DESC'
        ).fetchall()
        conn.close()
        
        return jsonify([dict(link) for link in links])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/launch-groups', methods=['GET'])
def get_launch_groups():
    """Tüm lansman gruplarını getir"""
    try:
        conn = get_db_connection()
        groups = conn.execute('''
            SELECT DISTINCT launch_group, COUNT(*) as link_count,
                   MIN(created_at) as first_link,
                   MAX(created_at) as last_link
            FROM utm_links 
            WHERE launch_group IS NOT NULL AND launch_group != ''
            GROUP BY launch_group
            ORDER BY last_link DESC
        ''').fetchall()
        conn.close()
        
        return jsonify([dict(group) for group in groups])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/links/<int:link_id>', methods=['DELETE'])
def delete_link(link_id):
    """Link sil"""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM utm_links WHERE id = ?', (link_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/build', methods=['POST'])
def build_utm():
    try:
        data = request.get_json()
        
        base_url = data.get('base_url', '').strip()
        utm_source = data.get('utm_source', '').strip()
        utm_medium = data.get('utm_medium', '').strip()
        utm_campaign = data.get('utm_campaign', '').strip()
        utm_term = data.get('utm_term', '').strip()
        utm_content = data.get('utm_content', '').strip()
        description = data.get('description', '').strip()
        launch_group = data.get('launch_group', '').strip()
        
        # Zorunlu alanları kontrol et
        if not base_url:
            return jsonify({'error': 'Base URL gereklidir'}), 400
        if not utm_source:
            return jsonify({'error': 'UTM Source gereklidir'}), 400
        if not utm_medium:
            return jsonify({'error': 'UTM Medium gereklidir'}), 400
        if not utm_campaign:
            return jsonify({'error': 'UTM Campaign gereklidir'}), 400
        
        # URL'i parse et
        parsed_url = urlparse(base_url)
        
        # Mevcut query parametrelerini al
        query_params = parse_qs(parsed_url.query)
        
        # UTM parametrelerini ekle
        utm_params = {
            'utm_source': utm_source,
            'utm_medium': utm_medium,
            'utm_campaign': utm_campaign
        }
        
        if utm_term:
            utm_params['utm_term'] = utm_term
        if utm_content:
            utm_params['utm_content'] = utm_content
        
        # Mevcut parametrelerle birleştir
        for key, value in utm_params.items():
            query_params[key] = [value]
        
        # Query string'i yeniden oluştur
        new_query = urlencode(query_params, doseq=True)
        
        # Yeni URL'i oluştur
        new_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment
        ))
        
        # Veritabanına kaydet
        conn = get_db_connection()
        cursor = conn.execute('''
            INSERT INTO utm_links 
            (base_url, utm_source, utm_medium, utm_campaign, utm_term, utm_content, utm_url, description, launch_group)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (base_url, utm_source, utm_medium, utm_campaign, utm_term, utm_content, new_url, description, launch_group))
        conn.commit()
        link_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'utm_url': new_url,
            'link_id': link_id,
            'message': 'Link başarıyla kaydedildi!'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
