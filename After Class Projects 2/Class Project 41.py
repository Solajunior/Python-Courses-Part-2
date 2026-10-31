import json
import tkinter as tk
import uuid
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk


PRODUCTS = {
    "A4 notebook": 3.50,
    "Ballpoint pens (pack of 5)": 2.25,
    "Colored pencils (pack of 12)": 5.75,
    "Erasers (pack of 3)": 1.50,
    "Glue sticks (pack of 2)": 2.00,
    "Pencil case": 6.50,
    "Ruler": 1.25,
    "School backpack": 24.00,
    "Pencils": 8.00
}
ORDER_STATUSES = (
    "Pending",
    "Processing",
    "Ready for pickup",
    "Completed",
    "Cancelled",
)
ORDERS_FILE = Path(__file__).resolve().with_name("stationery_orders.json")

BACKGROUND = "#f3f5f8"
INK = "#202b3c"
MUTED = "#65738a"
ACCENT = "#315e66"


def load_orders(path: Path) -> list[dict]:
    """Load saved orders and reject malformed order data."""
    try:
        orders = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []

    if not isinstance(orders, list):
        raise ValueError("The saved orders file must contain a list.")
    for order in orders:
        if (
            not isinstance(order, dict)
            or not isinstance(order.get("id"), str)
            or not isinstance(order.get("customer"), str)
            or not isinstance(order.get("created_at"), str)
            or not isinstance(order.get("items"), list)
            or not isinstance(order.get("total"), (int, float))
            or order.get("status") not in ORDER_STATUSES
        ):
            raise ValueError("The saved orders file contains an invalid order.")
        for item in order["items"]:
            if (
                not isinstance(item, dict)
                or not isinstance(item.get("product"), str)
                or not isinstance(item.get("quantity"), int)
                or item["quantity"] < 1
                or not isinstance(item.get("unit_price"), (int, float))
            ):
                raise ValueError("The saved orders file contains an invalid item.")
    return orders


def calculate_total(items: list[dict]) -> float:
    return sum(item["quantity"] * item["unit_price"] for item in items)


class StationeryOrderManagement:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Paper & Pine | Order Management")
        self.root.geometry("1120x780")
        self.root.minsize(900, 680)
        self.root.configure(bg=BACKGROUND)

        self.orders = load_orders(ORDERS_FILE)
        self.cart: dict[str, int] = {}
        self._configure_styles()
        self._build_ui()
        self._refresh_cart()
        self._refresh_orders()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.configure("Page.TFrame", background=BACKGROUND)
        style.configure("Card.TLabelframe", background="white", borderwidth=0)
        style.configure(
            "Card.TLabelframe.Label",
            background="white",
            foreground=INK,
            font=("Segoe UI", 11, "bold"),
        )
        style.configure("Title.TLabel", background=BACKGROUND, foreground=INK,
                        font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", background=BACKGROUND, foreground=MUTED,
                        font=("Segoe UI", 10))
        style.configure("Field.TLabel", background="white", foreground=MUTED,
                        font=("Segoe UI", 9, "bold"))
        style.configure("Total.TLabel", background="white", foreground=ACCENT,
                        font=("Segoe UI", 14, "bold"))
        style.configure("Treeview", rowheight=27, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Accent.TButton", font=("Segoe UI", 9, "bold"))

    def _build_ui(self) -> None:
        page = ttk.Frame(self.root, style="Page.TFrame", padding=(24, 20))
        page.pack(fill="both", expand=True)
        page.columnconfigure(0, weight=1)
        page.rowconfigure(2, weight=1)

        header = ttk.Frame(page, style="Page.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        ttk.Label(header, text="Paper & Pine", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Stationery orders, from the first pencil to pickup.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(3, 0))

        workspace = ttk.Frame(page, style="Page.TFrame")
        workspace.grid(row=1, column=0, sticky="nsew", pady=(0, 14))
        workspace.columnconfigure(0, weight=1)
        workspace.columnconfigure(1, weight=2)

        self._build_order_form(workspace)
        self._build_cart(workspace)
        self._build_order_history(page)

        self.message_var = tk.StringVar()
        ttk.Label(
            page,
            textvariable=self.message_var,
            style="Subtitle.TLabel",
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))

    def _build_order_form(self, parent: ttk.Frame) -> None:
        form = ttk.LabelFrame(
            parent,
            text="  New order  ",
            padding=16,
            style="Card.TLabelframe",
        )
        form.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        form.columnconfigure(0, weight=1)

        ttk.Label(form, text="Customer name", style="Field.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 5)
        )
        self.customer_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.customer_var).grid(
            row=1, column=0, sticky="ew", pady=(0, 14)
        )

        ttk.Label(form, text="Stationery item", style="Field.TLabel").grid(
            row=2, column=0, sticky="w", pady=(0, 5)
        )
        self.product_var = tk.StringVar(value=next(iter(PRODUCTS)))
        self.product_picker = ttk.Combobox(
            form,
            textvariable=self.product_var,
            values=tuple(PRODUCTS),
            state="readonly",
        )
        self.product_picker.grid(row=3, column=0, sticky="ew", pady=(0, 5))
        self.product_picker.bind("<<ComboboxSelected>>", self._update_product_price)

        self.product_price_var = tk.StringVar()
        ttk.Label(
            form, textvariable=self.product_price_var, style="Subtitle.TLabel"
        ).grid(row=4, column=0, sticky="w", pady=(0, 14))
        self._update_product_price()

        ttk.Label(form, text="Quantity", style="Field.TLabel").grid(
            row=5, column=0, sticky="w", pady=(0, 5)
        )
        self.quantity_var = tk.StringVar(value="1")
        quantity_entry = ttk.Spinbox(
            form, from_=1, to=999, textvariable=self.quantity_var, width=8
        )
        quantity_entry.grid(row=6, column=0, sticky="w", pady=(0, 14))

        ttk.Button(
            form,
            text="Add item to cart",
            command=self.add_to_cart,
            style="Accent.TButton",
        ).grid(row=7, column=0, sticky="ew")

    def _build_cart(self, parent: ttk.Frame) -> None:
        card = ttk.LabelFrame(
            parent,
            text="  Current order  ",
            padding=14,
            style="Card.TLabelframe",
        )
        card.grid(row=0, column=1, sticky="nsew", padx=(8, 0))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(0, weight=1)

        self.cart_table = ttk.Treeview(
            card,
            columns=("product", "quantity", "price", "total"),
            show="headings",
            selectmode="browse",
            height=6,
        )
        for column, title, width, anchor in (
            ("product", "Item", 220, "w"),
            ("quantity", "Qty", 55, "center"),
            ("price", "Each", 80, "e"),
            ("total", "Line total", 95, "e"),
        ):
            self.cart_table.heading(column, text=title)
            self.cart_table.column(column, width=width, anchor=anchor)
        self.cart_table.grid(row=0, column=0, sticky="nsew")
        cart_scrollbar = ttk.Scrollbar(
            card, orient="vertical", command=self.cart_table.yview
        )
        self.cart_table.configure(yscrollcommand=cart_scrollbar.set)
        cart_scrollbar.grid(row=0, column=1, sticky="ns")

        cart_actions = ttk.Frame(card)
        cart_actions.grid(row=1, column=0, sticky="ew", pady=(9, 8))
        ttk.Button(
            cart_actions, text="Remove selected", command=self.remove_cart_item
        ).pack(side="left")
        ttk.Button(
            cart_actions, text="Clear cart", command=self.clear_cart
        ).pack(side="left", padx=(8, 0))

        totals = ttk.Frame(card)
        totals.grid(row=2, column=0, sticky="ew")
        totals.columnconfigure(0, weight=1)
        ttk.Label(totals, text="Order total", style="Field.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        self.total_var = tk.StringVar(value="$0.00")
        ttk.Label(totals, textvariable=self.total_var, style="Total.TLabel").grid(
            row=0, column=1, sticky="e"
        )
        ttk.Button(
            card,
            text="Place order",
            command=self.place_order,
            style="Accent.TButton",
        ).grid(row=3, column=0, sticky="ew", pady=(10, 0))

    def _build_order_history(self, parent: ttk.Frame) -> None:
        history = ttk.LabelFrame(
            parent,
            text="  Order history  ",
            padding=14,
            style="Card.TLabelframe",
        )
        history.grid(row=2, column=0, sticky="nsew")
        history.columnconfigure(0, weight=1)
        history.rowconfigure(0, weight=1)

        self.order_table = ttk.Treeview(
            history,
            columns=("id", "customer", "date", "items", "total", "status"),
            show="headings",
            selectmode="browse",
            height=7,
        )
        for column, title, width, anchor in (
            ("id", "Order", 145, "w"),
            ("customer", "Customer", 145, "w"),
            ("date", "Placed", 145, "w"),
            ("items", "Items", 60, "center"),
            ("total", "Total", 90, "e"),
            ("status", "Status", 150, "w"),
        ):
            self.order_table.heading(column, text=title)
            self.order_table.column(column, width=width, anchor=anchor)
        self.order_table.grid(row=0, column=0, sticky="nsew")
        history_scrollbar = ttk.Scrollbar(
            history, orient="vertical", command=self.order_table.yview
        )
        self.order_table.configure(yscrollcommand=history_scrollbar.set)
        history_scrollbar.grid(row=0, column=1, sticky="ns")

        status_actions = ttk.Frame(history)
        status_actions.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        ttk.Label(status_actions, text="Update selected order:").pack(side="left")
        self.status_var = tk.StringVar(value=ORDER_STATUSES[1])
        ttk.Combobox(
            status_actions,
            textvariable=self.status_var,
            values=ORDER_STATUSES,
            state="readonly",
            width=20,
        ).pack(side="left", padx=(8, 8))
        ttk.Button(
            status_actions,
            text="Save status",
            command=self.update_order_status,
        ).pack(side="left")

    def _update_product_price(self, event: tk.Event | None = None) -> None:
        product = self.product_var.get()
        if product in PRODUCTS:
            self.product_price_var.set(f"${PRODUCTS[product]:.2f} each")

    def add_to_cart(self) -> None:
        product = self.product_var.get()
        try:
            quantity = int(self.quantity_var.get())
        except ValueError:
            self.message_var.set("Enter a whole-number quantity greater than zero.")
            return
        if product not in PRODUCTS:
            self.message_var.set("Choose a stationery item from the list.")
            return
        if quantity < 1:
            self.message_var.set("Quantity must be greater than zero.")
            return

        self.cart[product] = self.cart.get(product, 0) + quantity
        self.quantity_var.set("1")
        self.message_var.set(f"Added {quantity} × {product} to the order.")
        self._refresh_cart()

    def remove_cart_item(self) -> None:
        selected = self.cart_table.selection()
        if not selected:
            self.message_var.set("Select an item in the cart to remove it.")
            return
        self.cart.pop(selected[0], None)
        self._refresh_cart()
        self.message_var.set("Cart item removed.")

    def clear_cart(self) -> None:
        self.cart.clear()
        self._refresh_cart()
        self.message_var.set("Cart cleared.")

    def _refresh_cart(self) -> None:
        for row in self.cart_table.get_children():
            self.cart_table.delete(row)

        items = []
        for product, quantity in self.cart.items():
            price = PRODUCTS[product]
            line_total = quantity * price
            items.append(
                {"product": product, "quantity": quantity, "unit_price": price}
            )
            self.cart_table.insert(
                "",
                "end",
                iid=product,
                values=(product, quantity, f"${price:.2f}", f"${line_total:.2f}"),
            )
        self.total_var.set(f"${calculate_total(items):.2f}")

    def place_order(self) -> None:
        customer = self.customer_var.get().strip()
        if not customer:
            self.message_var.set("Enter the customer's name before placing the order.")
            return
        if not self.cart:
            self.message_var.set("Add at least one item to the cart first.")
            return

        items = [
            {"product": product, "quantity": quantity, "unit_price": PRODUCTS[product]}
            for product, quantity in self.cart.items()
        ]
        order = {
            "id": f"ORD-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}",
            "customer": customer,
            "created_at": datetime.now().isoformat(timespec="minutes"),
            "items": items,
            "total": calculate_total(items),
            "status": ORDER_STATUSES[0],
        }
        updated_orders = [order, *self.orders]
        try:
            self._save_orders(updated_orders)
        except OSError as error:
            messagebox.showerror(
                "Could not save order",
                f"The order was not placed because it could not be saved:\n{error}",
                parent=self.root,
            )
            return

        self.orders = updated_orders
        self.cart.clear()
        self.customer_var.set("")
        self._refresh_cart()
        self._refresh_orders()
        self.message_var.set(f"Order {order['id']} placed successfully.")

    def update_order_status(self) -> None:
        selected = self.order_table.selection()
        if not selected:
            self.message_var.set("Select an order from the history first.")
            return
        new_status = self.status_var.get()
        if new_status not in ORDER_STATUSES:
            self.message_var.set("Choose a valid order status.")
            return

        order_id = selected[0]
        updated_orders = [
            {**order, "status": new_status} if order["id"] == order_id else order
            for order in self.orders
        ]
        try:
            self._save_orders(updated_orders)
        except OSError as error:
            messagebox.showerror(
                "Could not update order",
                f"The order status was not changed because it could not be saved:\n{error}",
                parent=self.root,
            )
            return

        self.orders = updated_orders
        self._refresh_orders()
        self.message_var.set(f"Order {order_id} updated to {new_status}.")

    def _save_orders(self, orders: list[dict]) -> None:
        ORDERS_FILE.write_text(
            json.dumps(orders, indent=2),
            encoding="utf-8",
        )

    def _refresh_orders(self) -> None:
        for row in self.order_table.get_children():
            self.order_table.delete(row)
        for order in self.orders:
            try:
                placed = datetime.fromisoformat(order["created_at"]).strftime(
                    "%b %d, %Y %I:%M %p"
                )
            except ValueError:
                placed = order["created_at"]
            self.order_table.insert(
                "",
                "end",
                iid=order["id"],
                values=(
                    order["id"],
                    order["customer"],
                    placed,
                    sum(item["quantity"] for item in order["items"]),
                    f"${order['total']:.2f}",
                    order["status"],
                ),
            )


def main() -> None:
    root = tk.Tk()
    try:
        StationeryOrderManagement(root)
    except (OSError, ValueError) as error:
        messagebox.showerror(
            "Could not open orders",
            f"Saved orders could not be loaded:\n{error}",
            parent=root,
        )
        root.destroy()
        return
    root.mainloop()


if __name__ == "__main__":
    main()
