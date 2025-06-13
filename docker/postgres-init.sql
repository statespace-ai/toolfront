-- PostgreSQL initialization script for toolfront
-- Includes e-commerce OLTP schema and sample data

-- Source the e-commerce schema
\i /docker-entrypoint-initdb.d/01_ecommerce_oltp_schema.sql

-- Source the e-commerce sample data
\i /docker-entrypoint-initdb.d/02_ecommerce_oltp_data.sql

-- Create some additional views for common queries
CREATE VIEW active_user_sessions AS
SELECT 
    us.session_id,
    us.user_id,
    ua.email,
    us.ip_address,
    us.last_activity,
    us.expires_at
FROM user_sessions us
JOIN users_auth ua ON us.user_id = ua.user_id
WHERE us.is_active = TRUE 
    AND us.expires_at > CURRENT_TIMESTAMP;

CREATE VIEW current_inventory_levels AS
SELECT 
    i.product_id,
    w.warehouse_name,
    i.quantity_available,
    i.quantity_reserved,
    i.reorder_point,
    CASE 
        WHEN i.quantity_available <= i.reorder_point THEN 'LOW_STOCK'
        WHEN i.quantity_available = 0 THEN 'OUT_OF_STOCK'
        ELSE 'IN_STOCK'
    END as stock_status
FROM inventory i
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
WHERE w.is_active = TRUE;

CREATE VIEW abandoned_carts_summary AS
SELECT 
    sc.cart_id,
    sc.user_id,
    ua.email,
    COUNT(ci.cart_item_id) as item_count,
    SUM(ci.quantity * ci.unit_price) as cart_value,
    sc.updated_at as last_activity,
    EXTRACT(DAYS FROM (CURRENT_TIMESTAMP - sc.updated_at)) as days_abandoned
FROM shopping_carts sc
JOIN cart_items ci ON sc.cart_id = ci.cart_id
LEFT JOIN users_auth ua ON sc.user_id = ua.user_id
WHERE sc.cart_status = 'abandoned'
GROUP BY sc.cart_id, sc.user_id, ua.email, sc.updated_at;

CREATE VIEW pending_support_tickets AS
SELECT 
    st.ticket_id,
    st.user_id,
    ua.email,
    st.ticket_type,
    st.priority,
    st.subject,
    st.assigned_to,
    st.created_at,
    EXTRACT(HOURS FROM (CURRENT_TIMESTAMP - st.created_at)) as hours_open
FROM support_tickets st
LEFT JOIN users_auth ua ON st.user_id = ua.user_id
WHERE st.status IN ('open', 'in_progress');

-- Grant permissions for testuser
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testuser;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO testuser;
