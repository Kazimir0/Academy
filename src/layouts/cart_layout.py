from dash import html, dcc

cart_layout = html.Div(
    className="container mt-5",
    children=[
        dcc.Store(id="cart-items-store", storage_type="local"),  # Ensure this store is included
        html.H1("Coșul de Cumpărături", className="text-center mb-4"),
        html.Div(id="cart-items", className="row g-4"),  # Placeholder for cart items
        html.Div(
            className="d-flex justify-content-between align-items-center",
            children=[
                html.Div(id="cart-total", className="h5"),
                html.Button("Finalizează comanda", id="finalize-order-button", className="btn btn-success")
            ]
        ),
        dcc.Store(id="checkout-success", storage_type="local"),  # Add this store to track checkout success
        html.Div(id="cart-feedback", className="mt-3"),  # Placeholder for success message
        html.Div(id="checkout-feedback", className="mt-3"),  # Placeholder for checkout feedback
    ]
)
