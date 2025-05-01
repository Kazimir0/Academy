from dash import html

def orders_layout(order_groups):
    return html.Div(
        className="container mt-5",
        children=[
            html.H1("Comenzile Mele", className="text-center mb-4"),
            html.Div(
                className="row g-4",
                children=[
                    html.Div(
                        className="col-md-6",
                        children=[
                            html.Div(
                                className="card h-100",
                                children=[
                                    html.Div(
                                        className="card-body",
                                        children=[
                                            html.H5(f"Comanda #{order['order_id']}", className="card-title"),
                                            html.P(f"Data: {order['order_date']}", className="card-text text-muted"),
                                            html.P(order["product_name"], className="card-text"),  # Display product details
                                            html.P(
                                                f"Total: {order['total_price']} RON",
                                                className="card-text fw-bold mt-3"
                                            ),
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                    for order in order_groups
                ]
            )
        ]
    )
