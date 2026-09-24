# 🛒 NexCart

### Modern Full-Stack E-Commerce Platform

NexCart is a full-stack e-commerce platform built with Django, HTML5, CSS3, JavaScript, and MySQL (with seamless SQLite fallback for local development). Designed to offer a responsive shopping experience alongside a powerful seller/admin management dashboard, NexCart bridges consumer facing functionality with robust back-office store operations.

The platform solves core operational and user experience challenges inherent in modern online retail. Customers benefit from intuitive product discovery, persistent shopping cart management, wishlist curation, real-time search filtering, and step-by-step order tracking. Concurrently, store administrators and sellers gain access to centralized KPI analytics, inventory threshold alerts, and streamlined order status fulfillment workflows.

Built as a modular Django application split into dedicated domain apps (`accounts`, `categories`, `products`, `cart`, `orders`, `wishlist`, `reviews`, `dashboard`, `core`), NexCart demonstrates structured architectural patterns, clean data modeling, and customizable database persistence.

---

## ⚡ Project Highlights

- 🛍️ **Customer Shopping Experience** – Modern storefront featuring hero promotions, curated collections, discount badges, and product rating aggregation.
- 🔐 **Authentication & User Profiles** – Session-based authentication with account registration, profile management, and saved delivery address management.
- 🔎 **Product Discovery & Search** – Category hierarchy navigation with real-time client-side keyword search, category filtering, and sorting options.
- 🛒 **Dynamic Cart & Wishlist** – Session/User persistent shopping cart with subtotal, tax, dynamic shipping calculation, coupon application, and wishlist toggle features.
- 📦 **Order Management & Logistics** – Comprehensive checkout process, order summary creation, order history logging, and itemized step-by-step shipment tracking.
- 🏪 **Seller Dashboard & KPI Analytics** – Staff-only executive panel summarizing key performance metrics including total revenue, order counts, average order value (AOV), and customer totals.
- 📊 **Inventory & Fulfillment Monitoring** – Automated low-stock inventory alerts (`stock <= 5`) and quick-action order fulfillment status update controls.
- 📱 **Responsive UI & Interactive UX** – Built with HTML5, custom CSS layout systems, and Vanilla JavaScript for smooth toast notifications, modal dialogues, and dynamic dynamic interactions.
- 🗄️ **Dual Database Support** – Native support for production MySQL setups alongside zero-configuration SQLite for rapid local prototyping.
- ⚡ **Django Backend Architecture** – Powered by Django's ORM, signals, context processors, object-level permissions, and modular app structuring.

---

## ✨ Features

### 👤 Customer Features

- **Authentication & User Management**
  - User registration, login, and secure session logout (`accounts` app).
  - Profile customization including name, bio, avatar image URL, and contact detail management.
  - Saved shipping and billing address book with default address designation (`Address` model).

- **Product Discovery & Exploration**
  - Multilevel product catalog display featuring categories (`categories` app).
  - Advanced sorting (Price Low to High, High to Low, Top Rated, Newest Arrival).
  - Live client-side product search filtering by title and description keywords.
  - Detailed product page including multi-image gallery views, key specifications JSON data display, stock status, discount calculations, and savings highlights.

- **Shopping Cart & Checkout**
  - Dual persistent cart system supporting both authenticated users (`User`) and unauthenticated guest sessions (`session_key`).
  - Automated calculation of subtotals, configurable state tax (8%), conditional free shipping (orders over $150), and promotional coupon code discounts.
  - Full-featured multi-step checkout workflow with shipping address selection, saved address loading, and order confirmation.

- **Wishlist & Saved Items**
  - Personal saved item wishlist repository (`wishlist` app).
  - Direct one-click transfer of wishlist items into the active shopping cart.

- **Orders & Tracking**
  - Detailed order history overview showcasing itemized line items, order totals, and status markers (`placed`, `processing`, `shipped`, `out_for_delivery`, `delivered`, `cancelled`).
  - Interactive visual timeline view for tracking shipment progress via milestone logs (`OrderTracking` model).
  - Order return request submission functionality (`ReturnRequest` model).

- **Product Reviews & Q&A**
  - Verified buyer review submission system with rating stars (1–5 scale), headlines, and written feedback (`reviews` app).
  - Customer product question and answer (Q&A) inquiry module.

---

### 🏪 Seller Features

- **Executive Seller Dashboard**
  - Overview panel restricted to staff/seller accounts (`@staff_member_required`).
  - Key performance metric (KPI) scorecards tracking Total Revenue, Total Orders, Average Order Value (AOV), and Registered Customer Count.
  - Graphical sales trend visualization chart built with inline SVG rendering.

- **Order Fulfillment & Logistics Control**
  - Real-time order fulfillment table displaying recent customer purchases.
  - Order status management interface allowing status updates (`Placed` ➔ `Processing` ➔ `Shipped` ➔ `Delivered`).
  - Both standard POST form submission endpoints and RESTful JSON API endpoints (`/seller/orders/update-status-api/`) for status updates.

- **Inventory Alerts & Management**
  - Automated low-stock notification center identifying products with stock levels at or below 5 units.
  - Direct navigation links to update stock levels and product catalog properties via Django Admin.

---

## 🎨 UI / UX Design

NexCart's user interface is crafted with focus on visual aesthetic balance, modern web conventions, and interface responsiveness:

- **Design System & Layout**: Styled using custom Vanilla CSS (`static/css/styles.css`) leveraging CSS Grid and Flexbox for responsive grid layouts across desktop, tablet, and mobile devices.
- **Color Palette & Visual Cues**: Clean visual hierarchy incorporating contextual color badges for flash sales ("Sale"), stock urgency ("Low Stock"), and order status progress indicators.
- **Interactive Micro-Interactions**: Vanilla JavaScript (`static/js/main.js`) handles client-side dynamic state updates including real-time search filtering, dynamic tab switching, interactive rating stars, and toast notification alerts.
- **Modal Dialogues & Quick Views**: Integrated UI overlays for quick product detail inspection and return request initiation without interrupting user navigation flow.
- **Seller Workspace**: Dashboard interface tailored for quick administrative scanning with KPI stat tiles, data summary tables, and stock status indicators.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend Language** | Python 3.10+ | Core server-side application logic |
| **Framework** | Django 4.2+ | Web framework handling routing, ORM, security, templates, and sessions |
| **Database** | MySQL / SQLite3 | Primary relational data store (MySQL configurable, SQLite default) |
| **Frontend Logic** | Vanilla JavaScript (ES6+) | Dynamic DOM manipulation, filtering, modals, and API calls |
| **Styling & UI** | CSS3 | Custom design system using Flexbox, CSS Grid, and responsive media queries |
| **Structure** | HTML5 | Semantic HTML markup with Django Template Language (DTL) |
| **Assets & Utilities** | FontAwesome 6 | System icons for cart, wishlist, user profiles, and order status |

---

## 📐 Architecture

NexCart follows a classic Django Model-View-Template (MVT) monolithic architecture, ensuring high cohesion and clean separation of concerns across domain apps.

```
                  ┌──────────────────────────────────────────────┐
                  │                 Web Browser                  │
                  │   (HTML5 / CSS3 / Vanilla JS / FontAwesome)  │
                  └──────────────────────┬───────────────────────┘
                                         │ HTTP Request / Response
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │              Django WSGI / Server            │
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │            nexcart / URL Routing             │
                  └──────────────────────┬───────────────────────┘
                                         │
    ┌───────────────────┬────────────────┼───────────────────┬───────────────────┐
    ▼                   ▼                ▼                   ▼                   ▼
┌─────────┐       ┌───────────┐    ┌───────────┐       ┌───────────┐       ┌───────────┐
│  core   │       │ accounts  │    │ products  │       │   cart    │       │  orders   │
└────┬────┘       └─────┬─────┘    └─────┬─────┘       └─────┬─────┘       └─────┬─────┘
     │                  │                │                   │                   │
     ├──────────────────┼────────────────┴───────────────────┼───────────────────┤
     │                  ▼                                    ▼                   │
     │      ┌───────────────────────┐            ┌───────────────────────┐       │
     │      │   Context Processors  │            │  Django Views & DTL   │       │
     │      └───────────┬───────────┘            └───────────┬───────────┘       │
     │                  │                                    │                   │
     └──────────────────┼────────────────────────────────────┘                   │
                        ▼                                                        │
                  ┌──────────────────────────────────────────────┐               │
                  │              Django ORM Models               │◀──────────────┘
                  └──────────────────────┬───────────────────────┘
                                         │
                                         ▼
                  ┌──────────────────────────────────────────────┐
                  │     Database (MySQL / SQLite3 Fallback)      │
                  └──────────────────────────────────────────────┘
```

---

## 🔁 Core Application Workflow

### 🛍️ Customer Journey Workflow

```
 ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
 │ Account Reg/  │ ──► │ Browse & Filter│ ──► │ Product Detail│ ──► │ Add to Cart / │
 │  Guest Session│     │ Catalog Items │     │ & Review Specs│     │ Toggle Wishlist│
 └───────────────┘     └───────────────┘     └───────────────┘     └───────┬───────┘
                                                                           │
 ┌───────────────┐     ┌───────────────┐     ┌───────────────┐             │
 │ Order History │ ◄── │ Order Placed  │ ◄── │ Checkout &    │ ◄───────────┘
 │ & Shipment Log│     │ & Inventory -1│     │ Address Select│
 └───────────────┘     └───────────────┘     └───────────────┘
```

### 🏪 Seller Management Workflow

```
 ┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
 │ Staff Login   │ ──► │ Seller        │ ──► │ Monitor KPI   │ ──► │ Inventory Low-│
 │ Authentication│     │ Dashboard     │     │ Metrics & AOV │     │ Stock Alert   │
 └───────────────┘     └───────┬───────┘     └───────────────┘     └───────────────┘
                               │
                               ▼
                       ┌───────────────┐     ┌───────────────┐
                       │ Update Order  │ ──► │ Status Sync   │
                       │ Status        │     │ to Customer   │
                       └───────────────┘     └───────────────┘
```

---

## 🗄️ Database Schema Overview

NexCart utilizes relational models mapped via Django ORM:

- **`User` & `UserProfile`**: Auth record coupled 1-to-1 with profile data (phone, bio, avatar URL).
- **`Address`**: ForeignKey to `User`, handling shipping and billing address records with `is_default` handling.
- **`Category`**: Parent-child nested categories with slug, font-icon strings, and display ordering.
- **`Product` & `ProductImage`**: Core product attributes (price, discount price, SKU, stock, specifications JSON, badges) and additional gallery images.
- **`Cart` & `CartItem`**: Persistent shopping cart mapped to a `User` or guest `session_key`, containing items, quantities, and discount state.
- **`Wishlist` & `WishlistItem`**: User-bound saved product wishlist items.
- **`Order` & `OrderItem`**: Purchase records maintaining immutable snapshot copies of shipping addresses, item titles, prices, status tracking, and totals.
- **`OrderTracking`**: Milestone timeline entries (`step_name`, `description`, `location`, `timestamp`) for package movement.
- **`Review` & `ProductQuestion`**: User product ratings, verified purchase flags, written feedback, and product Q&A threads.

---

## 📁 Project Structure

```
NexCart/
├── accounts/               # User authentication, user profiles, and address management
│   ├── models.py           # UserProfile and Address models
│   ├── urls.py             # Auth and profile URL routes
│   └── views.py            # Login, register, profile, and address views
├── cart/                   # Cart functionality and coupon handling
│   ├── context_processors.py# Cart item count processor
│   ├── models.py           # Cart and CartItem models
│   ├── urls.py             # Add, update, remove, and clear cart endpoints
│   └── views.py            # Cart display and management views
├── categories/             # Category management and hierarchy
│   ├── models.py           # Category model
│   └── views.py            # Category listing views
├── core/                   # Home page, global views, and global context processors
│   ├── context_processors.py# Global store metadata processor
│   ├── urls.py             # Core routes (home, search, static pages)
│   └── views.py            # Home page and global search logic
├── dashboard/              # Seller and admin management dashboard
│   ├── urls.py             # Seller dashboard routes
│   └── views.py            # Analytics KPIs, low-stock alerts, and status update handlers
├── nexcart/                # Core Django project configuration directory
│   ├── settings.py         # App settings, DB setup (MySQL/SQLite), static & media paths
│   ├── urls.py             # Global URL router
│   ├── wsgi.py             # WSGI application entry point
│   └── asgi.py             # ASGI application entry point
├── orders/                 # Order processing, checkout, tracking, and returns
│   ├── models.py           # Order, OrderItem, OrderTracking, ReturnRequest models
│   ├── urls.py             # Checkout, order list, detail, tracking, and return routes
│   └── views.py            # Checkout handling and order tracking views
├── payments/               # Payment app module placeholder
├── products/               # Product catalog, product details, and image galleries
│   ├── models.py           # Product and ProductImage models
│   ├── urls.py             # Product detail and listing routes
│   └── views.py            # Product list, category filter, detail views
├── reviews/                # Customer reviews and product Q&A
│   ├── models.py           # Review and ProductQuestion models
│   └── views.py            # Review submission endpoints
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css      # Custom styling design system
│   └── js/
│       └── main.js         # Frontend interactive logic
├── templates/              # HTML templates
│   ├── base.html           # Layout template
│   ├── accounts/           # Auth and profile views
│   ├── cart/               # Shopping cart and checkout pages
│   ├── core/               # Home page and main index
│   ├── dashboard/          # Seller admin dashboard
│   ├── orders/             # Order confirmation, list, and tracking pages
│   ├── products/           # Catalog grid and detail views
│   └── wishlist/           # Saved wishlist layout
├── wishlist/               # Wishlist app module
│   ├── models.py           # Wishlist and WishlistItem models
│   ├── urls.py             # Add, remove, and view wishlist items
│   └── views.py            # Wishlist toggle and view actions
├── db.sqlite3              # Local SQLite development database
├── manage.py               # Django management CLI utility
└── seed_data.py            # Database seeder script for sample data population
```

---

## 🚀 Setup & Installation

Follow these instructions to set up and run NexCart on your local system.

### Prerequisites

- **Python**: Version 3.10 or higher installed
- **Git**: Installed on your system
- **MySQL** *(Optional)*: Required only if running with MySQL database mode. SQLite is used by default.

---

### Step 1: Clone Repository

```bash
git clone https://github.com/shivansh-sharma-18/NexCart.git
cd Cartivex
```

---

### Step 2: Create and Activate Virtual Environment

```bash
# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate

# On Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

---

### Step 3: Install Dependencies

```bash
pip install django mysqlclient
```

*(Note: `mysqlclient` is optional if you intend to run strictly using default SQLite mode).*

---

### Step 4: Configure Database & Environment Variables

By default, NexCart operates using local SQLite (`db.sqlite3`).

To optionally enable MySQL, set the `USE_MYSQL` environment variable to `true` and supply your database credentials:

```bash
# Example for Linux/macOS bash shell
export USE_MYSQL=true
export DB_NAME=nexcart_db
export DB_USER=root
export DB_PASSWORD=your_mysql_password
export DB_HOST=127.0.0.1
export DB_PORT=3306
```

---

### Step 5: Run Database Migrations

Apply database schema migrations to set up database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 6: Seed Sample Data *(Optional but Recommended)*

Populate the database with sample categories, products, customer reviews, demo users, and orders:

```bash
python seed_data.py
```

**Default Seed Credentials:**

- **Admin / Seller Account**: Username: `admin` | Password: `admin123`
- **Customer Account**: Username: `shopper` | Password: `shopper123`

---

### Step 7: Start Development Server

```bash
python manage.py runserver
```

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

- Access Customer Storefront: `http://127.0.0.1:8000/`
- Access Seller Dashboard: `http://127.0.0.1:8000/seller/` *(Requires logging in with `admin` account)*
- Access Django Admin: `http://127.0.0.1:8000/admin/`