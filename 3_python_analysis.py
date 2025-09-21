#!/usr/bin/env python3
"""
Healthcare Billing Analytics - Python Analysis
Advanced analytics and visualization for healthcare billing data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Set style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class HealthcareAnalytics:
    """Healthcare billing analytics class"""
    
    def __init__(self, db_path="healthcare_billing.db"):
        self.db_path = db_path
        self.engine = create_engine(f"sqlite:///{db_path}")
        self.conn = sqlite3.connect(db_path)
        
    def load_data(self):
        """Load data from SQLite database"""
        try:
            # Load main tables
            self.patients = pd.read_sql("SELECT * FROM patients", self.conn)
            self.billing = pd.read_sql("SELECT * FROM billing", self.conn)
            self.departments = pd.read_sql("SELECT * FROM departments", self.conn)
            self.services = pd.read_sql("SELECT * FROM services", self.conn)
            
            print("✅ Data loaded successfully!")
            print(f"Patients: {len(self.patients)} records")
            print(f"Billing: {len(self.billing)} records")
            print(f"Departments: {len(self.departments)} records")
            print(f"Services: {len(self.services)} records")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
    
    def revenue_analysis(self):
        """Analyze revenue patterns"""
        print("\n📊 REVENUE ANALYSIS")
        print("=" * 50)
        
        # Total revenue
        total_revenue = self.billing['amount'].sum()
        print(f"Total Revenue: ${total_revenue:,.2f}")
        
        # Revenue by department
        dept_revenue = self.billing.groupby('department')['amount'].agg(['sum', 'count', 'mean']).round(2)
        dept_revenue.columns = ['Total Revenue', 'Claim Count', 'Avg Claim Amount']
        dept_revenue = dept_revenue.sort_values('Total Revenue', ascending=False)
        
        print("\nRevenue by Department:")
        print(dept_revenue)
        
        # Create visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Revenue by department
        dept_revenue['Total Revenue'].plot(kind='bar', ax=axes[0,0], color='skyblue')
        axes[0,0].set_title('Revenue by Department')
        axes[0,0].set_ylabel('Revenue ($)')
        axes[0,0].tick_params(axis='x', rotation=45)
        
        # Claim count by department
        dept_revenue['Claim Count'].plot(kind='bar', ax=axes[0,1], color='lightcoral')
        axes[0,1].set_title('Claim Count by Department')
        axes[0,1].set_ylabel('Number of Claims')
        axes[0,1].tick_params(axis='x', rotation=45)
        
        # Average claim amount
        dept_revenue['Avg Claim Amount'].plot(kind='bar', ax=axes[1,0], color='lightgreen')
        axes[1,0].set_title('Average Claim Amount by Department')
        axes[1,0].set_ylabel('Average Amount ($)')
        axes[1,0].tick_params(axis='x', rotation=45)
        
        # Revenue distribution
        self.billing['amount'].hist(bins=20, ax=axes[1,1], color='gold', alpha=0.7)
        axes[1,1].set_title('Revenue Distribution')
        axes[1,1].set_xlabel('Amount ($)')
        axes[1,1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('revenue_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return dept_revenue
    
    def patient_demographics(self):
        """Analyze patient demographics"""
        print("\n👥 PATIENT DEMOGRAPHICS")
        print("=" * 50)
        
        # Age analysis
        if 'age' in self.patients.columns:
            age_stats = self.patients['age'].describe()
            print("Age Statistics:")
            print(age_stats)
            
            # Age groups
            age_groups = pd.cut(self.patients['age'], 
                              bins=[0, 18, 30, 50, 70, 100], 
                              labels=['Under 18', '18-30', '31-50', '51-70', 'Over 70'])
            age_dist = age_groups.value_counts()
            print("\nAge Group Distribution:")
            print(age_dist)
        
        # Insurance analysis
        if 'insurance_type' in self.patients.columns:
            insurance_dist = self.patients['insurance_type'].value_counts()
            print("\nInsurance Distribution:")
            print(insurance_dist)
        
        # Create demographics visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Age distribution
        if 'age' in self.patients.columns:
            self.patients['age'].hist(bins=20, ax=axes[0,0], color='skyblue', alpha=0.7)
            axes[0,0].set_title('Age Distribution')
            axes[0,0].set_xlabel('Age')
            axes[0,0].set_ylabel('Frequency')
        
        # Insurance distribution
        if 'insurance_type' in self.patients.columns:
            insurance_dist.plot(kind='pie', ax=axes[0,1], autopct='%1.1f%%')
            axes[0,1].set_title('Insurance Type Distribution')
        
        # Gender distribution
        if 'gender' in self.patients.columns:
            gender_dist = self.patients['gender'].value_counts()
            gender_dist.plot(kind='bar', ax=axes[1,0], color='lightcoral')
            axes[1,0].set_title('Gender Distribution')
            axes[1,0].set_ylabel('Count')
        
        # Patient charges distribution
        if 'total_charges' in self.patients.columns:
            self.patients['total_charges'].hist(bins=20, ax=axes[1,1], color='lightgreen', alpha=0.7)
            axes[1,1].set_title('Total Charges Distribution')
            axes[1,1].set_xlabel('Charges ($)')
            axes[1,1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('patient_demographics.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def billing_insights(self):
        """Analyze billing patterns and insights"""
        print("\n💰 BILLING INSIGHTS")
        print("=" * 50)
        
        # Claim status analysis
        if 'status' in self.billing.columns:
            status_dist = self.billing['status'].value_counts()
            print("Claim Status Distribution:")
            print(status_dist)
            
            # Status percentages
            status_pct = self.billing['status'].value_counts(normalize=True) * 100
            print("\nClaim Status Percentages:")
            print(status_pct.round(2))
        
        # Payment method analysis
        if 'payment_method' in self.billing.columns:
            payment_dist = self.billing['payment_method'].value_counts()
            print("\nPayment Method Distribution:")
            print(payment_dist)
        
        # Monthly trends
        if 'date' in self.billing.columns:
            self.billing['date'] = pd.to_datetime(self.billing['date'])
            monthly_revenue = self.billing.groupby(self.billing['date'].dt.to_period('M'))['amount'].sum()
            print("\nMonthly Revenue Trend:")
            print(monthly_revenue)
        
        # Create billing insights visualization
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Claim status
        if 'status' in self.billing.columns:
            status_dist.plot(kind='pie', ax=axes[0,0], autopct='%1.1f%%')
            axes[0,0].set_title('Claim Status Distribution')
        
        # Payment methods
        if 'payment_method' in self.billing.columns:
            payment_dist.plot(kind='bar', ax=axes[0,1], color='lightcoral')
            axes[0,1].set_title('Payment Method Distribution')
            axes[0,1].set_ylabel('Count')
            axes[0,1].tick_params(axis='x', rotation=45)
        
        # Monthly revenue trend
        if 'date' in self.billing.columns:
            monthly_revenue.plot(kind='line', ax=axes[1,0], marker='o', color='green')
            axes[1,0].set_title('Monthly Revenue Trend')
            axes[1,0].set_ylabel('Revenue ($)')
            axes[1,0].tick_params(axis='x', rotation=45)
        
        # Amount distribution
        self.billing['amount'].hist(bins=20, ax=axes[1,1], color='gold', alpha=0.7)
        axes[1,1].set_title('Claim Amount Distribution')
        axes[1,1].set_xlabel('Amount ($)')
        axes[1,1].set_ylabel('Frequency')
        
        plt.tight_layout()
        plt.savefig('billing_insights.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def performance_metrics(self):
        """Calculate key performance metrics"""
        print("\n📈 PERFORMANCE METRICS")
        print("=" * 50)
        
        # Overall metrics
        total_revenue = self.billing['amount'].sum()
        total_claims = len(self.billing)
        avg_claim_amount = self.billing['amount'].mean()
        
        print(f"Total Revenue: ${total_revenue:,.2f}")
        print(f"Total Claims: {total_claims:,}")
        print(f"Average Claim Amount: ${avg_claim_amount:,.2f}")
        
        # Department performance
        dept_performance = self.billing.groupby('department')['amount'].agg(['sum', 'count', 'mean']).round(2)
        dept_performance.columns = ['Total Revenue', 'Claim Count', 'Avg Claim Amount']
        dept_performance = dept_performance.sort_values('Total Revenue', ascending=False)
        
        print("\nDepartment Performance:")
        print(dept_performance)
        
        # Top performing department
        top_dept = dept_performance.index[0]
        top_revenue = dept_performance.iloc[0]['Total Revenue']
        print(f"\nTop Performing Department: {top_dept} (${top_revenue:,.2f})")
        
        return dept_performance
    
    def generate_report(self):
        """Generate comprehensive analytics report"""
        print("\n" + "="*60)
        print("🏥 HEALTHCARE BILLING ANALYTICS REPORT")
        print("="*60)
        
        # Load data
        self.load_data()
        
        # Run analyses
        revenue_analysis = self.revenue_analysis()
        self.patient_demographics()
        self.billing_insights()
        performance_metrics = self.performance_metrics()
        
        print("\n✅ Analysis complete! Charts saved as PNG files.")
        print("📊 Generated visualizations:")
        print("   - revenue_analysis.png")
        print("   - patient_demographics.png")
        print("   - billing_insights.png")

def main():
    """Main function"""
    print("🏥 Healthcare Billing Analytics")
    print("=" * 40)
    
    # Initialize analytics
    analytics = HealthcareAnalytics()
    
    # Generate report
    analytics.generate_report()

if __name__ == "__main__":
    main()
