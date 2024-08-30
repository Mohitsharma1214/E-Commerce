
# E-Commerce Website

This is a comprehensive e-commerce platform developed using Django, Razorpay for payment processing, and various features including session handling, coupon claiming, checkout, login/logout, and size selection. The platform is designed to provide a seamless shopping experience, ensuring security and scalability.

## Features

- **User Authentication:**
  - Secure user login and registration.
  - Password reset and change options.
  - Session management for a personalized shopping experience.

- **Product Management:**
  - Browse through a variety of products.
  - Filter products based on categories, sizes, and other attributes.
  - Detailed product pages with size selection.

- **Shopping Cart & Checkout:**
  - Add products to the shopping cart.
  - Update quantities or remove items.
  - Apply discount coupons at checkout.
  - Secure payment processing using Razorpay.
  - Order summary and confirmation.

- **Session Handling:**
  - Persistent cart and session management.
  - Maintain user session across multiple pages and interactions.

- **Coupon Claiming:**
  - Apply discount codes for promotional offers.
  - Validate coupon codes and update order total.

- **Payment Gateway Integration:**
  - Integrated with Razorpay for secure payment processing.
  - Support for multiple payment methods including credit/debit cards, UPI, and more.

- **Order Management:**
  - View past orders and track order status.
  - Email notifications for order confirmation and updates.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/e-commerce-website.git
    ```
2. Navigate to the project directory:
    ```bash
    cd e-commerce-website
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Apply migrations:
    ```bash
    python manage.py migrate
    ```
5. Create a superuser to access the admin panel:
    ```bash
    python manage.py createsuperuser
    ```
6. Run the development server:
    ```bash
    python manage.py runserver
    ```

## Usage

- Access the website at `http://localhost:8000/`.
- Admin panel is available at `http://localhost:8000/admin/`.
- Manage products, orders, and users through the admin panel.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.
