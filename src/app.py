import dash,json, os
from dash import html, dcc, callback_context
from layout import app_layout
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from products import add_product, delete_comment_from_db, fetch_comments_by_product_id, fetch_product_by_id, fetch_products,delete_product, save_comment_to_db, save_image_to_db,update_product
from db_connection import get_connection
from layouts.home_layout import home_layout
from layouts.product_list_layout import product_list_layout
from layouts.add_product_layout import product_add_layout
from layouts.edit_product_layout import edit_product_layout
from layouts.cart_layout import cart_layout
from layouts.navbar import navbar
from datetime import datetime
import pytz
from PIL import Image
from flask import Flask, send_from_directory

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,# Allow callbacks for dynamically loaded components
    prevent_initial_callbacks=True, 
    external_stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css"
    ]
)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@server.route('/static/uploads/<filename>')
def serve_image(filename):
    image_path = os.path.join('/app/static/uploads', filename)
    if os.path.isfile(image_path):
        return send_from_directory('/app/static/uploads', filename)
    else:
        return "Image not found", 404
    
@server.route('/<path:path>')
def catch_all(path):
    # Redirect all unknown routes to the Dash app
    return app.index()
    
## Main layout of the app
app.layout = app_layout

@app.callback(
    [
        Output("page-content", "children"),
        Output("current-product-data", "data"),
        Output("edit-error-message", "children"),
        Output("edit-error-message", "style"),
        Output("edit-success-message", "children"),
        Output("edit-success-message", "style")
    ],
    [
        Input("url", "pathname"),
        Input("save-edit-button", "n_clicks")
    ],
    [
        State("edit-product-name", "value"),
        State("edit-product-price", "value"),
        State("edit-product-description", "value"),
        State("edit-upload-image", "contents"),
        State("current-product-data", "data")
    ],
    prevent_initial_call=True
)
def handle_page_and_save_changes(pathname, save_clicks, name, price, description, image_content, product_data):
    ctx = callback_context

    # Redirect based on URL changes 
    if ctx.triggered and "url" in ctx.triggered[0]["prop_id"]:
        if pathname == "/":
            return home_layout, None, None, {"display": "none"}, None, {"display": "none"}

        elif pathname == "/add-product":
            return product_add_layout, None, None, {"display": "none"}, None, {"display": "none"}

        elif pathname == "/products":
            return product_list_layout, None, None, {"display": "none"}, None, {"display": "none"}

        elif pathname == "/cart":
            return cart_layout, None, None, {"display": "none"}, None, {"display": "none"}

        elif pathname.startswith("/product/"):
            product_id = pathname.split("/")[-1]
            product_data = fetch_product_by_id(product_id)
            if product_data:
                product_details = html.Div(
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col-md-4",
                                    children=[
                                        html.Img(
                                            src=f"/static/uploads/{os.path.basename(product_data['image_url'])}",
                                            className="img-fluid",
                                            style={"maxHeight": "300px", "objectFit": "contain"}
                                        )
                                    ]
                                ),
                                html.Div(
                                    className="col-md-8",
                                    children=[
                                        html.H3(product_data["name"], className="text-primary"),
                                        html.P(product_data["description"], className="mt-3"),
                                        html.P(f"Price: {product_data['price']} RON", className="text-success fw-bold"),
                                        html.Div(
                                            className="d-flex gap-2 mt-3",
                                            children=[
                                                html.Button("Editează Produs", id="edit-product-button", className="btn btn-warning"),
                                                html.Button("Șterge Produs", id="delete-product-button", className="btn btn-danger"),
                                                html.Button("Adaugă în Coș", id="add-to-cart-button", className="btn btn-primary"),
                                            ]
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        html.H3("Comentarii", className="mt-5 text-primary"),
                        html.Div(id="comments-section", className="mt-3"),
                        html.Div(
                            className="mt-4",
                            children=[
                                html.H4("Adaugă un comentariu", className="text-secondary"),
                                dcc.Textarea(
                                    id="comment-input",
                                    className="form-control",
                                    placeholder="Scrie un comentariu...",
                                    style={"height": "100px"}
                                ),
                                dcc.Dropdown(
                                    id="stars-rating",
                                    options=[{"label": f"{i} stele", "value": i} for i in range(1, 6)],
                                    placeholder="Alege numărul de stele",
                                    className="mt-2"
                                ),
                                html.Button(
                                    "Trimite",
                                    id="submit-comment-button",
                                    className="btn btn-primary mt-2"
                                ),
                                html.Div(id="comment-feedback", className="mt-2"),
                            ]
                        ),
                    ]
                )
                return product_details, product_data, None, {"display": "none"}, None, {"display": "none"}
            else:
                return html.H1("Produsul nu a fost găsit.", className="text-center mt-5"), None, None, {"display": "none"}, None, {"display": "none"}

        elif pathname.startswith("/edit-product/"):
            product_id = pathname.split("/")[-1]
            product_data = fetch_product_by_id(product_id)
            if product_data:
                return edit_product_layout, product_data, None, {"display": "none"}, None, {"display": "none"}
            else:
                return html.H1("Produsul nu a fost găsită.", className="text-center mt-5"), None, None, {"display": "none"}, None, {"display": "none"}

        elif pathname == "/orders":
            # Fetch grouped orders from the database
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    id,  -- Order ID
                    STRING_AGG(product_name + '|' + CAST(price AS NVARCHAR), ',') AS product_details, -- Concatenate product names and prices
                    SUM(price) AS total_price,
                    order_date
                FROM orders
                GROUP BY id, order_date
                ORDER BY order_date DESC
            """)
            rows = cursor.fetchall()
            cursor.close()
            conn.close()

            # Parse grouped orders
            order_groups = []
            for row in rows:
                items = [
                    {"name": item.split("|")[0], "price": float(item.split("|")[1])}
                    for item in row[1].split(",")
                ]
                product_name = ", ".join([f"{item['name']} - {item['price']} RON" for item in items])  # Concatenate product details
                order_groups.append({
                    "order_id": row[0],  # Order ID
                    "total_price": row[2],  # Total price
                    "order_date": convert_to_local_time(row[3], pytz.timezone("Europe/Bucharest")),
                    "product_name": product_name 
                })

            from layouts.orders_layout import orders_layout
            return orders_layout(order_groups), None, None, {"display": "none"}, None, {"display": "none"}

        else:
            return html.H1("404 - Pagina nu a fost găsită", className="text-center mt-5"), None, None, {"display": "none"}, None, {"display": "none"}

    #  Save changes for products
    if ctx.triggered and "save-edit-button" in ctx.triggered[0]["prop_id"]:
        if not save_clicks or not product_data:
            raise PreventUpdate

        errors = []
        if not name:
            errors.append("Numele produsului este necesar.")
        if not price or price <= 0:
            errors.append("Prețul trebuie să fie un număr pozitiv.")
        if not description:
            errors.append("Descrierea produsului este necesară.")

        if errors:
            return (
                edit_product_layout,
                product_data,
                html.Ul([html.Li(error) for error in errors], className="alert alert-danger"),
                {"display": "block"},
                None,
                {"display": "none"}
            )

        # New image processing
        image_url = product_data.get("image_url")
        if image_content:
            try:
                image_type, image_data = save_image_to_db(image_content)
                image_path = os.path.join(UPLOAD_FOLDER, f"{name}.{image_type}")
                with open(image_path, "wb") as f:
                    f.write(image_data)
                image_url = f"/static/uploads/{name}.{image_type}"
            except ValueError as e:
                return (
                    edit_product_layout,
                    product_data,
                    html.Div(str(e), className="alert alert-danger"),
                    {"display": "block"},
                    None,
                    {"display": "none"}
                )

        try:
            update_product(product_data["id"], name, price, description, image_url)
            updated_product_data = {
                "id": product_data["id"],
                "name": name,
                "price": price,
                "description": description,
                "image_url": image_url
            }
            return (
                edit_product_layout,
                updated_product_data,
                None,
                {"display": "none"},
                html.Div("Produsul a fost modificat cu succes!", className="alert alert-success"),
                {"display": "block"}
            )
        except Exception as e:
            return (
                edit_product_layout,
                product_data,
                html.Div(f"A apărut o eroare: {str(e)}", className="alert alert-danger"),
                {"display": "block"},
                None,
                {"display": "none"}
            )

    raise PreventUpdate


# Updated callback to handle comments and deletion
@app.callback(
    [Output("comments-section", "children"),
     Output("comment-feedback", "children"),
     Output("comment-input", "value"),
     Output("stars-rating", "value")],
    [Input("submit-comment-button", "n_clicks"),
     Input({'type': 'delete-comment', 'index': dash.ALL}, 'n_clicks'),
     Input("url", "pathname")],
    [State("comment-input", "value"),
     State("stars-rating", "value"),
     State({'type': 'delete-comment', 'index': dash.ALL}, 'id')],
    prevent_initial_call=False
)
def handle_comments_and_deletion(submit_clicks, delete_clicks, pathname, comment, stars, delete_ids):
    if not pathname.startswith("/product/"):
        raise PreventUpdate

    product_id = pathname.split("/")[-1]
    ctx = callback_context

    # Handle comment deletion
    if ctx.triggered and "delete-comment" in ctx.triggered[0]["prop_id"]:
        triggered_id = ctx.triggered[0]["prop_id"]
        comment_id = json.loads(triggered_id.split(".")[0])["index"]
        delete_comment_from_db(comment_id)
        feedback = html.Div("Comentariul a fost șters cu succes!", className="alert alert-success")
        comments = fetch_comments_by_product_id(product_id)
        return generate_comment_list(comments), feedback, "", None

    # Handle comment submission
    if submit_clicks and comment and stars:
        save_comment_to_db(product_id, comment, stars)
        feedback = html.Div("Comentariul a fost adăugat cu succes!", className="alert alert-success")
        comments = fetch_comments_by_product_id(product_id)
        return generate_comment_list(comments), feedback, "", None

    # Fetch and display comments when the page is loaded
    comments = fetch_comments_by_product_id(product_id)
    return generate_comment_list(comments), None, "", None

# Store for cart items
cart_items = []

# Callback to display cart items
@app.callback(
    [Output("cart-items", "children"),
     Output("cart-total", "children")],
    [Input("url", "pathname"),
     Input("cart-items-store", "data")],
    prevent_initial_call=True
)
def update_cart(pathname, cart_items):
    if pathname != "/cart":
        raise PreventUpdate

    cart_items = cart_items or []

    if not cart_items:
        return html.Div("Coșul este gol!", className="text-center"), "Total: 0 RON"

    cart_elements = [
        html.Div(
            className="col-md-4",
            children=[
                html.Div(
                    className="card h-100",
                    children=[
                        html.Img(src=item["image_url"], className="card-img-top"),
                        html.Div(
                            className="card-body",
                            children=[
                                html.H5(item["name"], className="card-title"),
                                html.P(f"Preț: {item['price']} RON", className="card-text"),
                                html.P(item["description"], className="card-text"),
                                html.Button(
                                    "Șterge",
                                    id={'type': 'remove-item', 'index': item['id']},
                                    className="btn btn-danger btn-sm mt-2"
                                )
                            ]
                        )
                    ]
                )
            ]
        )
        for item in cart_items
    ]

    total_price = sum(item["price"] for item in cart_items)
    return cart_elements, f"Total: {total_price} RON"

# Callback to handle checkout
@app.callback(
    Output("checkout-feedback", "children"),
    [Input("checkout-button", "n_clicks")],
    [State("cart-items-store", "data")],
    prevent_initial_call=True 
)
def handle_checkout(n_clicks, cart_items):
    if not cart_items:
        return html.Div("Coșul este gol!", className="alert alert-warning")

    # Set local timezone
    local_tz = pytz.timezone("Europe/Bucharest")

    # Generate a unique order ID
    order_id = datetime.now().strftime("%Y%m%d%H%M%S")

    # Calculate total price
    total_price = sum(item["price"] for item in cart_items)

    # Concatenate product names and prices for the order
    product_details = ", ".join([f"{item['name']} - {item['price']} RON" for item in cart_items])

    # Save order details to the database with local time
    conn = get_connection()
    cursor = conn.cursor()
    local_time = datetime.now(pytz.utc).astimezone(local_tz)  # Convert UTC to local time

    # Insert the order into the orders table
    cursor.execute(
        "INSERT INTO orders (id, product_name, price, order_date) VALUES (?, ?, ?, ?)",
        (order_id, product_details, total_price, local_time)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    # cart_items.clear()
    return html.Div("Comanda a fost finalizată cu succes!", className="alert alert-success")

@app.callback(
    [Output("product-list", "children"),
     Output("page-number", "children"),
     Output("current-page", "data"),
     Output("prev-button", "disabled"),
     Output("next-button", "disabled")],
    [Input("search-input", "value"),
     Input("prev-button", "n_clicks"),
     Input("next-button", "n_clicks")],
    [State("current-page", "data")]
)
def update_product_list(search_value, prev_clicks, next_clicks, current_page):
    if current_page is None:
        current_page = 1

    all_products = fetch_products()
    items_per_page = 6

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'prev-button' in changed_id:
        current_page = max(1, current_page - 1)
    elif 'next-button' in changed_id:
        current_page += 1

    if search_value:
        filtered_products = [
            product for product in all_products if
            search_value.lower() in product["name"].lower() or
            search_value.lower() in product["description"].lower()
        ]
    else:
        filtered_products = all_products

    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_products = filtered_products[start_idx:end_idx]

    product_cards = [
        html.Div(
            className="col",
            children=[
                html.Div(
                    className="card h-100 product-card",
                    children=[
                        html.Div(className="product-card-image-container",
                                 children=[
                                     html.Img(src=f"/static/uploads/{os.path.basename(product['image_url'])}", className="card-img-top", style={"maxHeight": "150px", "objectFit": "contain"})
                                 ]),
                        html.Div(
                            className="card-body product-card-body",
                            children=[
                                html.H5(product['name'], className="card-title product-card-title"),
                                html.P(f"Price: {product['price']} RON", className="card-text product-card-price"),
                                html.Button("Vezi detalii",
                                            className="btn btn-sm btn-outline-primary view-details-button",
                                            id={'type': 'view-details', 'index': product['id']}),
                            ]
                        )
                    ]
                )
            ]
        )
        for product in page_products
    ]
    page_info = f"Page {current_page}"
    disable_prev = current_page <= 1
    disable_next = len(filtered_products) <= items_per_page * current_page

    return product_cards, page_info, current_page, disable_prev, disable_next

# Callback for adding a product
@app.callback(
    [Output("error-message", "children"),
     Output("product-name", "className"),
     Output("error-name", "children"),
     Output("product-price", "className"),
     Output("error-price", "children"),
     Output("product-description", "className"),
     Output("error-description", "children"),
     Output("upload-image", "className"),
     Output("error-image", "children"),
     Output("add-product-message", "children")],
    [Input("add-product-button", "n_clicks")],
    [State("product-name", "value"),
     State("product-price", "value"),
     State("product-description", "value"),
     State("upload-image", "contents")]
)
def add_product_and_redirect(n_clicks, name, price, description, image_content):
    if not n_clicks:
        raise PreventUpdate

    # Validate inputs
    errors = []
    if not name:
        errors.append(("product-name", "form-control is-invalid", "Numele este necesar."))
    if not price or price <= 0:
        errors.append(("product-price", "form-control is-invalid", "Prețul trebuie să fie un număr pozitiv."))
    if not description:
        errors.append(("product-description", "form-control is-invalid", "Descrierea este necesară."))
    if not image_content:
        errors.append(("upload-image", "upload-box is-invalid", "Imaginea este necesară."))

    if errors:
        # Return errors for invalid fields
        return (
            "Te rugăm să completezi toate câmpurile.",
            *[error[1] if error[0] == "product-name" else "form-control" for error in errors],
            *[error[2] if error[0] == "product-name" else "" for error in errors],
            *[error[1] if error[0] == "product-price" else "form-control" for error in errors],
            *[error[2] if error[0] == "product-price" else "" for error in errors],
            *[error[1] if error[0] == "product-description" else "form-control" for error in errors],
            *[error[2] if error[0] == "product-description" else "" for error in errors],
            *[error[1] if error[0] == "upload-image" else "upload-box" for error in errors],
            *[error[2] if error[0] == "upload-image" else "" for error in errors],
            None
        )

    # Process image
    try:
        image_type, image_data = save_image_to_db(image_content)
        image_path = os.path.join(UPLOAD_FOLDER, f"{name}.{image_type}")
        with open(image_path, "wb") as f:
            f.write(image_data)
        image_url = f"/static/uploads/{name}.{image_type}"
    except ValueError as e:
        return (
            str(e),
            "form-control", "", "form-control", "", "form-control", "", "upload-box is-invalid", str(e), None
        )

    # Add product to the database
    try:
        add_product(name, price, description, image_url)
        return (
            None,
            "form-control is-valid", "", "form-control is-valid", "", "form-control is-valid", "", "upload-box is-valid", "",
            html.Div("Produsul a fost adăugat cu succes!", className="alert alert-success")
        )
    except Exception as e:
        return (
            "A apărut o eroare la adăugarea produsului.",
            "form-control", "", "form-control", "", "form-control", "", "upload-box", str(e), None
        )

@app.callback(
    Output("url", "pathname"),
    [
        Input({'type': 'view-details', 'index': dash.ALL}, "n_clicks"),
        Input("delete-product-button", "n_clicks"),
        Input("delete-confirm-dialog", "submit_n_clicks"),
        Input("edit-product-button", "n_clicks"),
        Input("cancel-edit-button", "n_clicks"),
        Input("finalize-order-button", "n_clicks")
    ],
    [
        State({'type': 'view-details', 'index': dash.ALL}, "id"),
        State("current-product-data", "data"),
        State("cart-items-store", "data")
    ],
    prevent_initial_call=True
)
def handle_navigation_and_actions(
    view_clicks, delete_clicks, confirm_clicks, edit_clicks, cancel_clicks, finalize_clicks,
    button_ids, product_data, cart_items
):
    ctx = callback_context

    if ctx.triggered:
        triggered_id = ctx.triggered[0]["prop_id"]

        # Navigate to product details
        if "view-details" in triggered_id:
            for i, n_clicks in enumerate(view_clicks):
                if n_clicks:
                    product_id = button_ids[i]["index"]
                    return f"/product/{product_id}"

        # Confirm product deletion
        elif "delete-confirm-dialog" in triggered_id:
            if confirm_clicks and product_data:
                delete_product(product_data["id"], product_data["image_url"])
                return "/products"

        # Navigate to edit product
        elif "edit-product-button" in triggered_id:
            if edit_clicks and product_data:
                return f"/edit-product/{product_data['id']}"

        # Cancel editing
        elif "cancel-edit-button" in triggered_id:
            if cancel_clicks and product_data:
                return f"/product/{product_data['id']}"

        # Finalize order
        elif "finalize-order-button" in triggered_id:
            if finalize_clicks and cart_items:
                # Save order details to the database
                conn = get_connection()
                cursor = conn.cursor()
                for item in cart_items:
                    cursor.execute(
                        "INSERT INTO orders (product_name, price, order_date) VALUES (?, ?, ?)",
                        (item["name"], item["price"], datetime.now())
                    )
                conn.commit()
                cursor.close()
                conn.close()
                # Redirect to the orders page
                return "/orders"
    raise PreventUpdate

@app.callback(
    [Output("delete-confirm-dialog", "displayed"),
     Output("delete-confirm-dialog", "message")],
    [Input("delete-product-button", "n_clicks")],
    [State("current-product-data", "data")],
    prevent_initial_call=True
)
def show_delete_confirmation(n_clicks, product_data):
    if n_clicks and product_data:
        product_name = product_data.get("name", "Produs necunoscut")
        return True, f"Ești sigur că vrei să ștergi produsul '{product_name}'?"
    raise PreventUpdate

@app.callback(
    [Output("cart-items-store", "data"),
     Output("cart-feedback", "children")],
    [Input("add-to-cart-button", "n_clicks"),
     Input({'type': 'remove-item', 'index': dash.ALL}, 'n_clicks')],
    [State("current-product-data", "data"),
     State("cart-items-store", "data"),
     State({'type': 'remove-item', 'index': dash.ALL}, 'id')],
    prevent_initial_call=True
)
def handle_cart_operations(add_clicks, remove_clicks, product_data, cart_items, button_ids):
    ctx = callback_context
    cart_items = cart_items or []

    # Handle adding to cart
    if ctx.triggered and "add-to-cart-button" in ctx.triggered[0]["prop_id"]:
        if any(item["id"] == product_data["id"] for item in cart_items):
            feedback = html.Div(
                f"Produsul '{product_data['name']}' este deja în coș!",
                className="alert alert-warning mt-3"
            )
            return cart_items, feedback

        cart_items.append(product_data)
        feedback = html.Div(
            f"Produsul '{product_data['name']}' a fost adăugat cu succes în coș!",
            className="alert alert-success mt-3"
        )
        return cart_items, feedback

    # Handle removing from cart
    if ctx.triggered and "remove-item" in ctx.triggered[0]["prop_id"]:
        triggered_id = json.loads(ctx.triggered[0]['prop_id'].split('.')[0])
        product_id_to_remove = triggered_id['index']

        # Verifică dacă acel buton chiar a fost apăsat
        for i, btn_id in enumerate(button_ids):
            if btn_id['index'] == product_id_to_remove and remove_clicks[i]:
                updated_cart = [item for item in cart_items if item['id'] != product_id_to_remove]
                feedback = html.Div(
                    "Produsul a fost șters din coș!",
                    className="alert alert-success mt-3"
                )
                return updated_cart, feedback

        raise PreventUpdate

@app.callback(
    [
        Output("edit-product-name", "value"),
        Output("edit-product-price", "value"),
        Output("edit-product-description", "value"),
        Output("edit-output-image-upload", "children"),
    ],
    [Input("current-product-data", "data")]
)
def populate_edit_fields(product_data):
    if not product_data:
        raise PreventUpdate

    # Populate fields with product data
    name = product_data.get("name", "")
    price = product_data.get("price", "")
    description = product_data.get("description", "")
    image_url = product_data.get("image_url", "")

    # Display the current image
    image_preview = html.Img(src=f"/static/uploads/{os.path.basename(image_url)}", style={"maxHeight": "150px"}) if image_url else None

    return name, price, description, image_preview

# Helper function to generate the comment list with delete buttons
def generate_comment_list(comments):
    local_tz = pytz.timezone("Europe/Bucharest")
    return [
        html.Div(
            className="border p-3 mb-2 rounded",
            children=[
                html.Div("★" * c["stars"] + "☆" * (5 - c["stars"]), className="text-warning mb-1"),  # Star rating
                html.P(c["text"], className="mb-1"),
                html.Small(
                    f"Data: {convert_to_local_time(c['timestamp'], local_tz)}",
                    className="text-muted"
                ),
                html.Button(
                    "Șterge",
                    id={'type': 'delete-comment', 'index': c["id"]},
                    className="btn btn-danger btn-sm mt-2"
                )
            ]
        )
        for c in comments
    ]

def convert_to_local_time(timestamp, local_tz):
    """Helper function to safely convert a timestamp to local time."""
    if isinstance(timestamp, str):
        try:
            utc_time = datetime.fromisoformat(timestamp)
        except ValueError:
            return "Invalid timestamp"
    elif isinstance(timestamp, datetime):
        utc_time = timestamp
    else:
        return "Invalid timestamp"

    # Convert to local timezone
    return utc_time.astimezone(local_tz).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8050)