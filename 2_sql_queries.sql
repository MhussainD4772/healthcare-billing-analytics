-- Healthcare Billing Analytics - Core SQL Queries
-- This file contains essential SQL queries for healthcare billing analysis

-- =============================================
-- 1. REVENUE ANALYSIS
-- =============================================

-- Total revenue by department
SELECT 
    department,
    SUM(amount) as total_revenue,
    COUNT(*) as total_claims,
    AVG(amount) as avg_claim_amount
FROM billing 
GROUP BY department 
ORDER BY total_revenue DESC;

-- Monthly revenue trend
SELECT 
    strftime('%Y-%m', date) as month,
    SUM(amount) as monthly_revenue,
    COUNT(*) as total_claims
FROM billing 
GROUP BY strftime('%Y-%m', date)
ORDER BY month;

-- =============================================
-- 2. PATIENT DEMOGRAPHICS
-- =============================================

-- Patient count by age group
SELECT 
    CASE 
        WHEN age < 18 THEN 'Under 18'
        WHEN age BETWEEN 18 AND 30 THEN '18-30'
        WHEN age BETWEEN 31 AND 50 THEN '31-50'
        WHEN age BETWEEN 51 AND 70 THEN '51-70'
        ELSE 'Over 70'
    END as age_group,
    COUNT(*) as patient_count,
    AVG(total_charges) as avg_charges
FROM patients 
GROUP BY age_group
ORDER BY patient_count DESC;

-- Insurance coverage analysis
SELECT 
    insurance_type,
    COUNT(*) as patient_count,
    AVG(coverage_percentage) as avg_coverage,
    SUM(total_charges) as total_charges
FROM patients 
GROUP BY insurance_type
ORDER BY patient_count DESC;

-- =============================================
-- 3. BILLING INSIGHTS
-- =============================================

-- Top services by revenue
SELECT 
    service_name,
    SUM(amount) as total_revenue,
    COUNT(*) as service_count,
    AVG(amount) as avg_service_cost
FROM services s
JOIN billing b ON s.service_id = b.service_id
GROUP BY service_name
ORDER BY total_revenue DESC
LIMIT 10;

-- Claim status analysis
SELECT 
    status,
    COUNT(*) as claim_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM billing 
GROUP BY status
ORDER BY claim_count DESC;

-- =============================================
-- 4. PERFORMANCE METRICS
-- =============================================

-- Department performance
SELECT 
    d.department_name,
    COUNT(b.claim_id) as total_claims,
    SUM(b.amount) as total_revenue,
    AVG(b.amount) as avg_claim_amount,
    AVG(b.processing_days) as avg_processing_days
FROM departments d
LEFT JOIN billing b ON d.department_id = b.department_id
GROUP BY d.department_name
ORDER BY total_revenue DESC;

-- Insurance claim success rate
SELECT 
    insurance_type,
    COUNT(*) as total_claims,
    SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved_claims,
    ROUND(
        (SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 2
    ) as approval_rate
FROM billing b
JOIN patients p ON b.patient_id = p.patient_id
GROUP BY insurance_type
ORDER BY approval_rate DESC;

-- =============================================
-- 5. FINANCIAL ANALYSIS
-- =============================================

-- Revenue vs Costs analysis
SELECT 
    department,
    SUM(amount) as total_revenue,
    SUM(cost) as total_cost,
    (SUM(amount) - SUM(cost)) as profit,
    ROUND(((SUM(amount) - SUM(cost)) / SUM(amount)) * 100, 2) as profit_margin
FROM billing 
GROUP BY department
ORDER BY profit DESC;

-- Payment method analysis
SELECT 
    payment_method,
    COUNT(*) as transaction_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM billing 
GROUP BY payment_method
ORDER BY total_amount DESC;

-- =============================================
-- 6. TIME-BASED ANALYSIS
-- =============================================

-- Daily revenue pattern
SELECT 
    strftime('%w', date) as day_of_week,
    CASE strftime('%w', date)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        WHEN '6' THEN 'Saturday'
    END as day_name,
    SUM(amount) as total_revenue,
    COUNT(*) as total_claims
FROM billing 
GROUP BY strftime('%w', date)
ORDER BY strftime('%w', date);

-- Quarterly performance
SELECT 
    strftime('%Y-Q', date) as quarter,
    SUM(amount) as quarterly_revenue,
    COUNT(*) as total_claims,
    AVG(amount) as avg_claim_amount
FROM billing 
GROUP BY strftime('%Y-Q', date)
ORDER BY quarter;

-- =============================================
-- 7. ADVANCED ANALYTICS
-- =============================================

-- Patient lifetime value
SELECT 
    p.patient_id,
    p.first_name,
    p.last_name,
    COUNT(b.claim_id) as total_claims,
    SUM(b.amount) as total_spent,
    AVG(b.amount) as avg_claim_amount,
    MIN(b.date) as first_visit,
    MAX(b.date) as last_visit
FROM patients p
JOIN billing b ON p.patient_id = b.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name
HAVING COUNT(b.claim_id) > 1
ORDER BY total_spent DESC;

-- Service profitability analysis
SELECT 
    s.service_name,
    s.base_cost,
    AVG(b.amount) as avg_charge,
    (AVG(b.amount) - s.base_cost) as avg_profit,
    ROUND(((AVG(b.amount) - s.base_cost) / AVG(b.amount)) * 100, 2) as profit_margin
FROM services s
JOIN billing b ON s.service_id = b.service_id
GROUP BY s.service_id, s.service_name, s.base_cost
ORDER BY avg_profit DESC;
