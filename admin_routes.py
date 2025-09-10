from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
import datetime

admin_bp = Blueprint('admin', __name__)

def require_admin_session():
    """Check if user is logged in as admin in session"""
    user_data = session.get('mock_user_data')
    if not user_data or not user_data.get('is_admin', False):
        return False
    return True

# Mock data for admin functionality
MOCK_USERS = [
    {
        'id': '1',
        'email': 'admin@tradinggrow.com',
        'full_name': 'Admin User',
        'subscription_tier': 'pro',
        'is_admin': True,
        'created_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': '2',
        'email': 'demo@tradinggrow.com',
        'full_name': 'Demo User',
        'subscription_tier': 'pro',
        'is_admin': False,
        'created_at': '2024-01-15T00:00:00Z'
    },
    {
        'id': '3',
        'email': 'user1@example.com',
        'full_name': 'John Smith',
        'subscription_tier': 'medium',
        'is_admin': False,
        'created_at': '2024-02-01T00:00:00Z'
    },
    {
        'id': '4',
        'email': 'user2@example.com',
        'full_name': 'Jane Doe',
        'subscription_tier': 'free',
        'is_admin': False,
        'created_at': '2024-02-15T00:00:00Z'
    },
    {
        'id': '5',
        'email': 'user3@example.com',
        'full_name': 'Bob Wilson',
        'subscription_tier': 'free',
        'is_admin': False,
        'created_at': '2024-03-01T00:00:00Z'
    }
]

MOCK_STOCKS = [
    {
        'id': '1',
        'symbol': 'AAPL',
        'name': 'Apple Inc.',
        'sector': 'Technology',
        'price': 175.50,
        'change_percent': 2.3
    },
    {
        'id': '2',
        'symbol': 'GOOGL',
        'name': 'Alphabet Inc.',
        'sector': 'Technology',
        'price': 2850.25,
        'change_percent': -1.2
    },
    {
        'id': '3',
        'symbol': 'MSFT',
        'name': 'Microsoft Corporation',
        'sector': 'Technology',
        'price': 420.15,
        'change_percent': 1.8
    },
    {
        'id': '4',
        'symbol': 'TSLA',
        'name': 'Tesla Inc.',
        'sector': 'Consumer',
        'price': 245.80,
        'change_percent': -3.5
    }
]

MOCK_SUBSCRIPTION_REQUESTS = [
    {
        'id': '1',
        'user_id': '3',
        'user_name': 'John Smith',
        'user_email': 'user1@example.com',
        'current_tier': 'medium',
        'requested_tier': 'pro',
        'created_at': '2024-03-15T10:00:00Z'
    }
]

@admin_bp.route('/admin/login')
def admin_login():
    """Admin login page"""
    return render_template('spa.html')

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if not require_admin_session():
        return redirect('/admin/login')
    return render_template('spa.html')

@admin_bp.route('/admin/logout')
def admin_logout():
    """Admin logout endpoint"""
    session.pop('mock_user_id', None)
    session.pop('mock_user_data', None)
    session.pop('is_admin', None)
    return redirect('/admin/login')

# API Endpoints

@admin_bp.route('/admin/api/dashboard-data')
def admin_dashboard_data():
    """Get admin dashboard statistics"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'data': {
            'stats': {
                'total_users': len(MOCK_USERS),
                'pro_users': len([u for u in MOCK_USERS if u['subscription_tier'] == 'pro']),
                'medium_users': len([u for u in MOCK_USERS if u['subscription_tier'] == 'medium']),
                'free_users': len([u for u in MOCK_USERS if u['subscription_tier'] == 'free']),
                'total_screenings': 89
            },
            'screenings': [
                {
                    'id': 1,
                    'name': 'High Growth Stocks',
                    'results_count': 23,
                    'created_at': '2024-03-15T10:00:00Z'
                },
                {
                    'id': 2,
                    'name': 'Value Stocks',
                    'results_count': 18,
                    'created_at': '2024-03-14T15:30:00Z'
                }
            ]
        }
    })

@admin_bp.route('/admin/api/users')
def get_all_users():
    """Get all users for admin management"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'users': MOCK_USERS
    })

@admin_bp.route('/admin/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # Find and update user in mock data
    for user in MOCK_USERS:
        if user['id'] == user_id:
            user.update({
                'email': data.get('email', user['email']),
                'full_name': data.get('full_name', user['full_name']),
                'subscription_tier': data.get('subscription_tier', user['subscription_tier']),
                'is_admin': data.get('is_admin', user['is_admin'])
            })
            return jsonify({'success': True, 'message': 'User updated successfully'})
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/admin/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global MOCK_USERS
    MOCK_USERS = [u for u in MOCK_USERS if u['id'] != user_id]
    
    return jsonify({'success': True, 'message': 'User deleted successfully'})

@admin_bp.route('/admin/api/users/<user_id>/subscription', methods=['PUT'])
def update_user_subscription(user_id):
    """Update user subscription tier"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_tier = data.get('subscription_tier')
    
    # Find and update user subscription
    for user in MOCK_USERS:
        if user['id'] == user_id:
            user['subscription_tier'] = new_tier
            return jsonify({'success': True, 'message': f'Subscription updated to {new_tier}'})
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/admin/api/subscription-requests')
def get_subscription_requests():
    """Get all pending subscription requests"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'requests': MOCK_SUBSCRIPTION_REQUESTS
    })

@admin_bp.route('/admin/api/subscription-requests/<request_id>/<action>', methods=['POST'])
def handle_subscription_request(request_id, action):
    """Approve or reject subscription request"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global MOCK_SUBSCRIPTION_REQUESTS
    
    # Find the request
    request_obj = None
    for req in MOCK_SUBSCRIPTION_REQUESTS:
        if req['id'] == request_id:
            request_obj = req
            break
    
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404
    
    if action == 'approve':
        # Update user subscription
        for user in MOCK_USERS:
            if user['id'] == request_obj['user_id']:
                user['subscription_tier'] = request_obj['requested_tier']
                break
        
        # Remove request
        MOCK_SUBSCRIPTION_REQUESTS = [r for r in MOCK_SUBSCRIPTION_REQUESTS if r['id'] != request_id]
        
        return jsonify({
            'success': True, 
            'message': f"Subscription upgraded to {request_obj['requested_tier']}"
        })
    
    elif action == 'reject':
        # Remove request
        MOCK_SUBSCRIPTION_REQUESTS = [r for r in MOCK_SUBSCRIPTION_REQUESTS if r['id'] != request_id]
        
        return jsonify({
            'success': True,
            'message': 'Subscription request rejected'
        })
    
    return jsonify({'error': 'Invalid action'}), 400

@admin_bp.route('/admin/api/bulk-upgrade', methods=['POST'])
def bulk_upgrade_users():
    """Bulk upgrade users from one tier to another"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    from_tier = data.get('from_tier')
    to_tier = data.get('to_tier')
    
    updated_count = 0
    for user in MOCK_USERS:
        if user['subscription_tier'] == from_tier and not user.get('is_admin', False):
            user['subscription_tier'] = to_tier
            updated_count += 1
    
    return jsonify({
        'success': True,
        'message': f'Upgraded {updated_count} users from {from_tier} to {to_tier}',
        'updated_count': updated_count
    })

@admin_bp.route('/admin/api/stocks', methods=['GET'])
def get_all_stocks():
    """Get all stocks for management"""
    return jsonify({
        'success': True,
        'stocks': MOCK_STOCKS
    })

@admin_bp.route('/admin/api/stocks', methods=['POST'])
def add_stock():
    """Add a new stock"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    new_stock = {
        'id': str(len(MOCK_STOCKS) + 1),
        'symbol': data.get('symbol', '').upper(),
        'name': data.get('name', ''),
        'sector': data.get('sector', ''),
        'price': float(data.get('price', 0)),
        'change_percent': float(data.get('change_percent', 0))
    }
    
    MOCK_STOCKS.append(new_stock)
    
    return jsonify({
        'success': True,
        'message': 'Stock added successfully',
        'stock': new_stock
    })

@admin_bp.route('/admin/api/stocks/<stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    """Delete a stock"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global MOCK_STOCKS
    MOCK_STOCKS = [s for s in MOCK_STOCKS if s['id'] != stock_id]
    
    return jsonify({
        'success': True,
        'message': 'Stock removed successfully'
    })

@admin_bp.route('/admin/api/stocks/<stock_id>/price', methods=['PUT'])
def update_stock_price(stock_id):
    """Update stock price"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_price = float(data.get('price', 0))
    
    for stock in MOCK_STOCKS:
        if stock['id'] == stock_id:
            old_price = stock['price']
            stock['price'] = new_price
            # Calculate change percentage
            if old_price > 0:
                stock['change_percent'] = ((new_price - old_price) / old_price) * 100
            return jsonify({'success': True, 'message': 'Stock price updated'})
    
    return jsonify({'error': 'Stock not found'}), 404