from typing import Optional
from pydantic import BaseModel, Field

class AGT(BaseModel):
    company_name :Optional[str] = Field(description="Name of the intermediary company")
    full_name :Optional[str] = Field(description="Full name of person in charge")
    email_addr: Optional[str] = Field(description="Email address of the intermediary company")
    country_name: Optional[str] = Field(description="Name of contry where the intermediary company is")

class Customer(BaseModel):
    first_name: Optional[str] = Field(description="First name of the customer")
    family_name: Optional[str] = Field(description="Family name of the customer")
    nationality: Optional[str] = Field(description="Nationality or nationalities of the customers, who actually make the trip")
    number_of_customers: Optional[str] = Field(description="Number of customers and their age groups, e.g., '2 adults in their 30s, 2 children 8 years & 12 years old'")
    relationships_between_customers: Optional[str] = Field(description="Relationships between customers, e.g., 'family, friends, couples' and their occupational status")
    arrival_date: Optional[str] = Field(description="Arrival date in YYYY-MM-DD format")
    departure_date: Optional[str] = Field(description="Departure date in YYYY-MM-DD format")
    budget: Optional[str] = Field(description="Total budget or budget per day")
    first_time_visitor: Optional[str] = Field(description="Whether they are first-time visitors in Japan, 'yes' or 'no'")
    preferences_in_cities: Optional[str] = Field(description="Preferences in cities, whether they want to visit typical places such as Tokyo and Kyoto")
    areas_of_interests: Optional[str] = Field(description="Types of activities they prefer, e.g., 'traditional cultural experiences, food, sports'")
    accommodations: Optional[str] = Field(description="Accommodation preferences including hotel ranks, brands, and room types")
    transportation: Optional[str] = Field(description="Transportation needs, including bullet train tickets, private cars, and airport transfers")
    guide: Optional[str] = Field(description="Whether they need an English speaking or any other languages guide, 'yes' or 'no' and specify the language if 'yes'")

class AllInfo(BaseModel):
    intermediate_company_info : AGT = Field(description="Information of the intermediary company")
    customer_info : Customer = Field(description="Information of the Customer")