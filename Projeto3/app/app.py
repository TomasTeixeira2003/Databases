#!/usr/bin/python3
from logging.config import dictConfig

import psycopg
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool


# postgres://{user}:{password}@{hostname}:{port}/{database-name}
DATABASE_URL = "postgres://db:db@postgres/db"

pool = ConnectionPool(conninfo=DATABASE_URL)
# the pool starts connecting immediately.

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
log = app.logger


@app.route("/", methods=("GET",))
def base():
    return render_template("base.html")

@app.route("/products", methods=("GET",))
def product_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            products = cur.execute(
                """
                SELECT sku, name, description, price, ean
                FROM product
                ORDER BY sku DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(products)

    return render_template("product/index.html", products=products)


@app.route("/products/<sku>/update", methods=("GET", "POST"))
def product_update(sku):
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
                SELECT sku, name, description, price, ean
                FROM product
                WHERE sku = %(sku)s;
                """,
                {"sku": sku},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")

    if request.method == "POST":
        log.debug(request.form.to_dict())
        price = request.form["price"]
        description = request.form["description"]

        error = None

        if not price:
            error = "price is required."
            if not price.isnumeric():
                error = "price is required to be numeric."

        if error is not None:
            flash(error)
        else:
            with pool.connection() as conn:
                with conn.transaction():
                    with conn.cursor(row_factory=namedtuple_row) as cur:
                        cur.execute(
                            """
                            UPDATE product
                            SET price = %(price)s, description = %(description)s
                            WHERE sku = %(sku)s;
                            """,
                            {"sku": sku, "price": price, "description": description},
                        )
                    ##conn.commit()
            return redirect(url_for("product_index"))

    return render_template("product/update.html", product=product)

@app.route("/products/<sku>/delete", methods=("POST",))
def product_delete(sku):
    with pool.connection() as conn:
        with conn.transaction():
            with conn.cursor(row_factory=namedtuple_row) as cur:

                cur.execute(
                    """
                    UPDATE supplier SET name = NULL, address = NULL, date = NULL, sku = NULL
                    WHERE sku = %(sku)s;
                    """,
                    {"sku": sku},
                )

                cur.execute(
                    "DELETE FROM contains WHERE sku = %(sku)s",
                    {"sku": sku},
                )
                
                cur.execute(
                    "DELETE FROM product WHERE sku = %(sku)s",
                    {"sku": sku},
                )


                cur.execute(
                    """
                    DELETE FROM pay
                    WHERE order_no NOT IN (SELECT order_no FROM contains);
                    """
                )

                cur.execute(
                    """
                    DELETE FROM process
                    WHERE order_no NOT IN (SELECT order_no FROM contains);
                    """
                )
                cur.execute(
                    """
                    DELETE FROM orders
                    WHERE order_no NOT IN (SELECT order_no FROM contains);
                    """
                )

                

    return redirect(url_for("product_index"))


@app.route("/products/create", methods=("GET", "POST"))
def product_create():
    if request.method == "POST":
        sku = request.form["sku"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        try:
            ean = request.form["ean"]
        except:
            ean = None

        with pool.connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO product (sku, name, description, price, ean)
                        VALUES (%(sku)s, %(name)s, %(description)s, %(price)s, %(ean)s);
                        """,
                        {"sku": sku, "name": name, "description": description, "price": price, "ean": ean},
                    )
                #conn.commit()
        return redirect(url_for("product_index"))

    return render_template("product/create.html")

@app.route("/suppliers", methods=("GET",))
def supplier_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            suppliers = cur.execute(
                """
                SELECT tin, name, address, sku, date
                FROM supplier
                ORDER BY SKU DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")
            
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(suppliers)

    return render_template("supplier/index.html", suppliers=suppliers)

@app.route("/suppliers/create", methods=("GET", "POST"))
def supplier_create():
    if request.method == "POST":
        log.debug(request.form)
        tin = request.form["tin"]
        name = request.form["name"]
        address = request.form["address"]
        sku = request.form["sku"]
        date = request.form["date"]

        with pool.connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO supplier (tin, name, address, sku, date)
                        VALUES (%(tin)s, %(name)s, %(address)s, %(sku)s, %(date)s);
                        """,
                        {"tin": tin, "name": name, "address": address, "sku": sku, "date": date},
                    )
                #conn.commit()
        return redirect(url_for("supplier_index"))
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            products = cur.execute(
                            """
                            SELECT sku, name, description, price, ean
                            FROM product
                            ORDER BY sku DESC;
                            """,
                            {},
                    ).fetchall()

    return render_template("supplier/create.html", products=products)

@app.route("/suppliers/<tin>/delete", methods=("POST",))
def supplier_delete(tin):
    with pool.connection() as conn:
        with conn.transaction():
            with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    DELETE FROM delivery WHERE tin = %(tin)s;
                    """,
                    {"tin": tin},
                )

                cur.execute(
                    """
                    DELETE FROM supplier WHERE tin = %(tin)s;
                    """,
                    {"tin": tin},
                )
            #conn.commit()
    return redirect(url_for("supplier_index"))

@app.route("/customers", methods=("GET",))
def customer_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            customers = cur.execute(
                """
                SELECT cust_no, name, email, phone, address
                FROM customer
                ORDER BY cust_no DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")
            
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(customers)

    return render_template("customer/index.html", customers=customers)

@app.route("/customers/create", methods=("GET", "POST"))
def customer_create():
    if request.method == "POST":
        cust_no = request.form["cust_no"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]

        with pool.connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO customer (cust_no, name, email, phone, address)
                        VALUES (%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s);
                        """,
                        {"cust_no": cust_no, "name": name, "email": email, "phone": phone, "address": address},
                    )
                #conn.commit()
        return redirect(url_for("customer_index"))
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            max_cust_no = cur.execute(
                            """
                            SELECT MAX(cust_no) AS max_cust_no FROM customer;
                            """,
                            {},
                    ).fetchall()
            
            cust_no_to_use = int(max_cust_no[0].max_cust_no) + 1

    return render_template("customer/create.html", cust_no_to_use=cust_no_to_use)

@app.route("/customers/<cust_no>/delete", methods=("POST",))
def customer_delete(cust_no):
    with pool.connection() as conn:
        with conn.transaction():
            with conn.cursor(row_factory=namedtuple_row) as cur:
        
                cur.execute(
                    """
                    DELETE FROM contains
                    WHERE order_no IN (SELECT order_no FROM orders WHERE cust_no = %(cust_no)s);
                    """,
                    {"cust_no": cust_no},
                )

                cur.execute(
                    """
                    DELETE FROM process
                    WHERE order_no IN (SELECT order_no FROM orders WHERE cust_no = %(cust_no)s);
                    """,
                    {"cust_no": cust_no},
                )

                cur.execute(
                    """
                    DELETE FROM pay WHERE cust_no = %(cust_no)s;
                    """,
                    {"cust_no": cust_no},
                )

                cur.execute(
                    """
                    DELETE FROM orders WHERE cust_no = %(cust_no)s;
                    """,
                    {"cust_no": cust_no},
                )
                
                cur.execute(
                    """
                    DELETE FROM customer WHERE cust_no = %(cust_no)s;
                    """,
                    {"cust_no": cust_no},
                )
                
            #conn.commit()
    return redirect(url_for("customer_index"))

@app.route("/orders", methods=("GET",))
def order_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            unpaid_orders = cur.execute(
                """
                SELECT order_no, cust_no, date
                FROM orders 
                WHERE order_no NOT IN (SELECT order_no FROM pay)
                ORDER BY order_no DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

            paid_orders = cur.execute(
                """
                SELECT order_no, cust_no, date
                FROM orders 
                WHERE order_no IN (SELECT order_no FROM pay)
                ORDER BY order_no DESC;
                """,
                {},
            ).fetchall()
            log.debug(f"Found {cur.rowcount} rows.")

    # API-like response is returned to clients that request JSON explicitly (e.g., fetch)
    if (
        request.accept_mimetypes["application/json"]
        and not request.accept_mimetypes["text/html"]
    ):
        return jsonify(unpaid_orders, paid_orders)

    return render_template("order/index.html", unpaid_orders=unpaid_orders, paid_orders=paid_orders)

@app.route("/orders/create", methods=("GET", "POST"))
def order_create():
    if request.method == "POST":
        order_no = request.form["order_no"]
        cust_no = request.form["cust_no"]
        date = request.form["date"]
        sku = request.form["sku"]
        qty = request.form["qty"]

        with pool.connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=namedtuple_row) as cur:                
                    cur.execute(
                        """
                        INSERT INTO orders (order_no, cust_no, date)
                        VALUES (%(order_no)s, %(cust_no)s, %(date)s);
                        """,
                        {"order_no": order_no, "cust_no": cust_no, "date": date},
                    )

                    cur.execute(
                        """
                        INSERT INTO contains (order_no, sku, qty)
                        VALUES (%(order_no)s, %(sku)s, %(qty)s);
                        """,
                        {"order_no": order_no, "sku": sku, "qty": qty},
                    )

                #conn.commit()

        return redirect(url_for("order_index"))
    
    with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                products = cur.execute(
                                """
                                SELECT sku, name, description, price, ean
                                FROM product
                                ORDER BY sku DESC;
                                """,
                                {},
                        ).fetchall()
                
                customers = cur.execute(
                                """
                                SELECT cust_no, name
                                FROM customer
                                ORDER BY cust_no ASC;
                                """,
                                {},
                        ).fetchall() 
                
                max_order_no = cur.execute(
                                """
                                SELECT MAX(order_no) AS max_order_no FROM orders;
                                """,
                                {},
                        ).fetchall()
            
                order_no_to_use = int(max_order_no[0].max_order_no) + 1

    return render_template("order/create.html", products=products, customers=customers, order_no_to_use=order_no_to_use)

@app.route("/orders/<order_no>/<cust_no>/<employee>/pay", methods=("GET", "POST"))
def order_pay(order_no, cust_no, employee):
    if request.method == "POST":
        with pool.connection() as conn:
            with conn.transaction():
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        INSERT INTO pay (order_no, cust_no)
                        VALUES (%(order_no)s, %(cust_no)s);
                        """,
                        {"order_no": order_no, "cust_no": cust_no},
                    )

                    cur.execute(
                        """
                        INSERT into process (ssn, order_no)
                        VALUES (%(ssn)s, %(order_no)s);
                        """,
                        {"ssn": employee, "order_no": order_no},
                    )
                #conn.commit()
        return redirect(url_for("order_index"))
    
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            order_price = cur.execute(
                            """
                            SELECT SUM(price*qty) AS order_price
                            FROM product JOIN contains USING (SKU)
                            GROUP BY order_no
                            HAVING order_no = %(order_no)s;
                            """,
                            {"order_no": order_no},
                    ).fetchall()
            order_price_str = str(order_price[0].order_price)
            log.debug(f"Order price is {order_price_str}")
                
    
    return render_template("order/pay.html", order={"order_no": order_no, "cust_no": cust_no, "order_price": order_price_str})

if __name__ == "__main__":
    app.run()
