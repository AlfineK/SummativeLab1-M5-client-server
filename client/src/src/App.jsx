import { useState, useEffect } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5555";
const emptyForm = {
  product_name: "",
  barcode: "",
  brands: "",
  categories: "",
  quantity: 1,
  price: 0,
};

function App() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(emptyForm);
  const [editingId, setEditingId] = useState(null);
  const [status, setStatus] = useState(null);

  function showMessage(text, isError = false) {
    setStatus({ text, isError });
  }

  function handleInputChange(event) {
    const { name, value } = event.target;
    setForm((prevForm) => ({ ...prevForm, [name]: value }));
  }

  function resetForm() {
    setForm(emptyForm);
    setEditingId(null);
  }

  function loadInventory() {
    fetch(`${API_URL}/inventory`)
      .then((res) => res.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setItems(data);
        } else {
          showMessage(data.error || "Could not load inventory.", true);
        }
      });
  }

  function handleLookUp() {
    const barcode = form.barcode.trim();
    const name = form.product_name.trim();

    if (!barcode && !name) {
      showMessage("Enter a barcode or product name first", true);
      return;
    }
    const query = `barcode=${encodeURIComponent(barcode)}&name=${encodeURIComponent(name)}`;
    fetch(`${API_URL}/external/lookup?${query}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          showMessage(data.error, true);
          return;
        }
        const product = data.product || {};
        setForm((prev) => ({
          ...prev,
          product_name: prev.product_name.trim() || product.product_name || "",
          barcode: prev.barcode.trim() || product.code || "",
          brands:product.brands  || prev.brands ||"",
          categories: product.categories ||prev.categories ||"" ,
        }));
        showMessage(
          `Found "${product.product_name || "product"}" from OpenFoodFacts.`,
        );
      });
  }

  function handleSubmit(event) {
    event.preventDefault();
    const payload = {
      barcode: form.barcode.trim(),
      product_name: form.product_name.trim(),
      quantity: Number(form.quantity || 0),
      price: Number(form.price || 0),
      brands: form.brands.trim(),
      categories: form.categories.trim(),
    };
    const isEditing = editingId !== null;
    const url = isEditing
      ? `${API_URL}/inventory/${editingId}`
      : `${API_URL}/inventory`;
    const method = isEditing ? "PATCH" : "POST";

    fetch(url, {
      method: method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          showMessage(data.error, true);
          return;
        }
        showMessage(
          isEditing ? `Updated Item #${editingId}` : `Added Item #${data.id}`,
        );
        resetForm();
        loadInventory();
      });
  }

  function handleStartEdit(item) {
    setEditingId(item.id);
    setForm({
      barcode: item.barcode || "",
      product_name: item.product_name || "",
      quantity: item.quantity,
      price: item.price,
      brands: item.brands || "",
      categories: item.categories || "",
    });
    showMessage(`Editing Item #${item.id}`);
  }

  function handleDelete(id) {
    fetch(`${API_URL}/inventory/${id}`, {
      method: "DELETE",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.error) {
          showMessage(data.error, true);
          return;
        }
        if (editingId === id) {
          resetForm();
        }
        showMessage(data.message || `Deleted item #${id}`);
        loadInventory();
      });
  }

  useEffect(() => {
    loadInventory();
  }, []);

  return (
    <main className="portal-shell">
      <header className="top-bar">
        <div>
          <h1>Retail Inventory Admin Portal</h1>
          <p>Manage stock,pricing,and openFoodFacts product lookups</p>
        </div>
        <span className="count-pill">
          {items.length} {items.length === 1 ? "Item" : "Items" }in stock
        </span>
      </header>
      {status && (
        <div className={`banner ${status.isError ? "err" : "ok"}`}>
          {status.text}
        </div>
      )}
      <section className="card">
        <h2>
          {editingId !== null
            ? `Edit Product #${editingId}`
            : "Add a New Product"}
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="lookup-row">
            <input
              type="text"
              name="barcode"
              placeholder="Barcode (e.g., 3017620422003)"
              value={form.barcode}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="product_name"
              placeholder="Product Name"
              value={form.product_name}
              onChange={handleInputChange}
            />
            <button type="button" className="btn-slate" onClick={handleLookUp}>
              Lookup Product
            </button>
          </div>

          <div className="field-grid">
            <input
              type="number"
              name="quantity"
              min="0"
              placeholder="Quantity"
              value={form.quantity}
              onChange={handleInputChange}
            />
            <input
              type="number"
              name="price"
              min="0"
              step="0.01"
              placeholder="Price"
              value={form.price}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="brands"
              placeholder="Brand"
              value={form.brands}
              onChange={handleInputChange}
            />
            <input
              type="text"
              name="categories"
              placeholder="Category"
              value={form.categories}
              onChange={handleInputChange}
            />
          </div>

          <div className="btn-group">
            <button type="button" className="btn-slate" onClick={resetForm}>
              Clear Form
            </button>
          </div>
        </form>
      </section>
      <section className="card">
        <h2>Current Inventory</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Product Name</th>
                <th>Barcode</th>
                <th>Brand</th>
                <th>Category</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan="8">No products in inventory yet.</td>
                </tr>
              ) : (
                items.map((item) => (
                  <tr key={item.id}>
                    <td>#{item.id}</td>
                    <td>
                      <strong>{item.product_name}</strong>
                    </td>
                    <td>
                      {item.barcode ? (
                        <span className="code-tag">{item.barcode}</span>
                      ) : (
                        "-"
                      )}
                    </td>
                    <td>{item.brands}</td>
                    <td>{item.categories}</td>
                    <td>{item.quantity}</td>
                    <td>${Number(item.price).toFixed(2)}</td>
                    <td>
                      <div className="btn-group">
                        <button
                          type="button"
                          className="btn-teal"
                          onClick={() => handleStartEdit(item)}
                        >
                          Edit
                        </button>
                        <button
                          type="button"
                          className="btn-rose"
                          onClick={() => handleDelete(item.id)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
export default App;
