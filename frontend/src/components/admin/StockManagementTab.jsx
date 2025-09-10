import React, { useState } from 'react';

const StockManagementTab = ({ stocks, onRefresh }) => {
    const [selectedStock, setSelectedStock] = useState(null);
    const [showAddModal, setShowAddModal] = useState(false);
    const [newStock, setNewStock] = useState({
        symbol: '',
        name: '',
        sector: '',
        price: '',
        change_percent: ''
    });

    const handleAddStock = async () => {
        try {
            const response = await fetch('/admin/api/stocks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(newStock)
            });

            if (response.ok) {
                setShowAddModal(false);
                setNewStock({ symbol: '', name: '', sector: '', price: '', change_percent: '' });
                onRefresh();
                alert('Stock added successfully!');
            } else {
                alert('Failed to add stock');
            }
        } catch (error) {
            console.error('Error adding stock:', error);
            alert('Error adding stock');
        }
    };

    const handleDeleteStock = async (stockId) => {
        if (!confirm('Are you sure you want to remove this stock?')) return;

        try {
            const response = await fetch(`/admin/api/stocks/${stockId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                onRefresh();
                alert('Stock removed successfully!');
            } else {
                alert('Failed to remove stock');
            }
        } catch (error) {
            console.error('Error removing stock:', error);
            alert('Error removing stock');
        }
    };

    const handleUpdatePrice = async (stockId, newPrice) => {
        try {
            const response = await fetch(`/admin/api/stocks/${stockId}/price`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ price: newPrice })
            });

            if (response.ok) {
                onRefresh();
                alert('Stock price updated!');
            } else {
                alert('Failed to update price');
            }
        } catch (error) {
            console.error('Error updating price:', error);
            alert('Error updating price');
        }
    };

    return (
        <div className="p-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
                <h4><i className="fas fa-chart-line me-2"></i>Stock Management</h4>
                <button 
                    className="btn btn-primary"
                    onClick={() => setShowAddModal(true)}
                >
                    <i className="fas fa-plus me-2"></i>Add Stock
                </button>
            </div>

            {/* Stock Management Cards */}
            <div className="row mb-4">
                <div className="col-md-3">
                    <div className="card text-center">
                        <div className="card-body">
                            <h5 className="text-primary">{stocks.length}</h5>
                            <p className="mb-0">Total Stocks</p>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card text-center">
                        <div className="card-body">
                            <h5 className="text-success">
                                {stocks.filter(s => s.change_percent >= 0).length}
                            </h5>
                            <p className="mb-0">Gainers</p>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card text-center">
                        <div className="card-body">
                            <h5 className="text-danger">
                                {stocks.filter(s => s.change_percent < 0).length}
                            </h5>
                            <p className="mb-0">Losers</p>
                        </div>
                    </div>
                </div>
                <div className="col-md-3">
                    <div className="card text-center">
                        <div className="card-body">
                            <h5 className="text-info">
                                {[...new Set(stocks.map(s => s.sector))].length}
                            </h5>
                            <p className="mb-0">Sectors</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Stocks Table */}
            <div className="table-responsive">
                <table className="table table-hover">
                    <thead className="table-light">
                        <tr>
                            <th>Symbol</th>
                            <th>Name</th>
                            <th>Sector</th>
                            <th>Price</th>
                            <th>Change %</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        {stocks.map(stock => (
                            <tr key={stock.id || stock.symbol}>
                                <td>
                                    <strong>{stock.symbol}</strong>
                                </td>
                                <td>{stock.name}</td>
                                <td>
                                    <span className="badge bg-secondary">{stock.sector}</span>
                                </td>
                                <td>
                                    <div className="input-group input-group-sm" style={{width: '120px'}}>
                                        <span className="input-group-text">$</span>
                                        <input 
                                            type="number" 
                                            className="form-control"
                                            value={stock.price}
                                            step="0.01"
                                            onChange={(e) => {
                                                if (e.key === 'Enter') {
                                                    handleUpdatePrice(stock.id, e.target.value);
                                                }
                                            }}
                                            onBlur={(e) => {
                                                if (e.target.value !== stock.price) {
                                                    handleUpdatePrice(stock.id, e.target.value);
                                                }
                                            }}
                                        />
                                    </div>
                                </td>
                                <td>
                                    <span className={`badge ${stock.change_percent >= 0 ? 'bg-success' : 'bg-danger'}`}>
                                        {stock.change_percent >= 0 ? '+' : ''}{stock.change_percent}%
                                    </span>
                                </td>
                                <td>
                                    <div className="btn-group btn-group-sm">
                                        <button 
                                            className="btn btn-outline-info"
                                            onClick={() => setSelectedStock(stock)}
                                        >
                                            <i className="fas fa-eye"></i>
                                        </button>
                                        <button 
                                            className="btn btn-outline-danger"
                                            onClick={() => handleDeleteStock(stock.id)}
                                        >
                                            <i className="fas fa-trash"></i>
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {stocks.length === 0 && (
                <div className="text-center py-5">
                    <i className="fas fa-chart-line fa-3x text-muted mb-3"></i>
                    <h5 className="text-muted">No stocks found</h5>
                    <p className="text-muted">Add stocks to manage them here</p>
                </div>
            )}

            {/* Add Stock Modal */}
            {showAddModal && (
                <div className="modal show d-block" tabIndex="-1">
                    <div className="modal-dialog">
                        <div className="modal-content">
                            <div className="modal-header">
                                <h5 className="modal-title">Add New Stock</h5>
                                <button 
                                    type="button" 
                                    className="btn-close"
                                    onClick={() => setShowAddModal(false)}
                                ></button>
                            </div>
                            <div className="modal-body">
                                <div className="mb-3">
                                    <label className="form-label">Stock Symbol</label>
                                    <input 
                                        type="text" 
                                        className="form-control"
                                        placeholder="e.g., AAPL"
                                        value={newStock.symbol}
                                        onChange={(e) => setNewStock({...newStock, symbol: e.target.value.toUpperCase()})}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Company Name</label>
                                    <input 
                                        type="text" 
                                        className="form-control"
                                        placeholder="e.g., Apple Inc."
                                        value={newStock.name}
                                        onChange={(e) => setNewStock({...newStock, name: e.target.value})}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Sector</label>
                                    <select 
                                        className="form-select"
                                        value={newStock.sector}
                                        onChange={(e) => setNewStock({...newStock, sector: e.target.value})}
                                    >
                                        <option value="">Select Sector</option>
                                        <option value="Technology">Technology</option>
                                        <option value="Healthcare">Healthcare</option>
                                        <option value="Finance">Finance</option>
                                        <option value="Energy">Energy</option>
                                        <option value="Consumer">Consumer</option>
                                        <option value="Industrial">Industrial</option>
                                        <option value="Real Estate">Real Estate</option>
                                    </select>
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Current Price ($)</label>
                                    <input 
                                        type="number" 
                                        className="form-control"
                                        step="0.01"
                                        placeholder="0.00"
                                        value={newStock.price}
                                        onChange={(e) => setNewStock({...newStock, price: e.target.value})}
                                    />
                                </div>
                                <div className="mb-3">
                                    <label className="form-label">Change %</label>
                                    <input 
                                        type="number" 
                                        className="form-control"
                                        step="0.01"
                                        placeholder="0.00"
                                        value={newStock.change_percent}
                                        onChange={(e) => setNewStock({...newStock, change_percent: e.target.value})}
                                    />
                                </div>
                            </div>
                            <div className="modal-footer">
                                <button 
                                    type="button" 
                                    className="btn btn-secondary"
                                    onClick={() => setShowAddModal(false)}
                                >
                                    Cancel
                                </button>
                                <button 
                                    type="button" 
                                    className="btn btn-primary"
                                    onClick={handleAddStock}
                                    disabled={!newStock.symbol || !newStock.name}
                                >
                                    Add Stock
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default StockManagementTab;