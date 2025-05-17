from app.models.case import Base, Case
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

def init_db():
    # Create database engine
    engine = create_engine('sqlite:///justice_ai.db')
    Base.metadata.create_all(engine)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Clear existing data
    session.query(Case).delete()
    session.commit()
    
    # Sample cases
    sample_cases = [
        Case(
            case_number="CASE-2024001",
            title="Smith vs. Corporation",
            description="""The plaintiff alleges that the corporation failed to provide 
            adequate safety measures in the workplace, leading to a serious injury. 
            Multiple witnesses have testified about the unsafe conditions, and 
            documentation shows repeated safety violations.""",
            plaintiff="John Smith",
            defendant="ABC Corporation",
            case_type="Workplace Safety",
            verdict="Guilty",
            confidence_score=0.85
        ),
        Case(
            case_number="CASE-2024002",
            title="Johnson Contract Dispute",
            description="""A contract dispute between two parties regarding the delivery 
            of goods. The defendant claims force majeure due to natural disasters, 
            while the plaintiff argues that alternative delivery methods were available.""",
            plaintiff="Johnson Enterprises",
            defendant="Global Logistics",
            case_type="Contract",
            verdict="Not Guilty",
            confidence_score=0.78
        ),
        Case(
            case_number="CASE-2024003",
            title="Property Rights Case",
            description="""A complex property rights case involving disputed land boundaries. 
            Both parties have presented historical documents and survey records, but 
            the evidence is contradictory and inconclusive.""",
            plaintiff="City Council",
            defendant="Property Developers Ltd",
            case_type="Property",
            verdict="Inconclusive",
            confidence_score=0.45
        ),
        # Additional cases
        Case(
            case_number="CASE-2024004",
            title="Workplace Harassment Case",
            description="""Multiple employees have reported systematic harassment by a senior manager. 
            HR records show previous complaints, and witness testimonies corroborate the pattern 
            of inappropriate behavior. The company failed to take action despite multiple reports.""",
            plaintiff="Employee Group",
            defendant="Tech Solutions Inc",
            case_type="Workplace Safety",
            verdict="Guilty",
            confidence_score=0.92
        ),
        Case(
            case_number="CASE-2024005",
            title="Software License Dispute",
            description="""A dispute over software licensing terms. The plaintiff claims the license 
            was violated, but the defendant has provided evidence of proper licensing and usage 
            within agreed terms. Documentation supports the defendant's position.""",
            plaintiff="Software Corp",
            defendant="IT Services Ltd",
            case_type="Contract",
            verdict="Not Guilty",
            confidence_score=0.88
        ),
        Case(
            case_number="CASE-2024006",
            title="Environmental Impact Case",
            description="""A case regarding environmental impact of a construction project. 
            Expert opinions are divided, and the available data is insufficient to make 
            a definitive determination about the environmental consequences.""",
            plaintiff="Environmental Group",
            defendant="Construction Co",
            case_type="Property",
            verdict="Inconclusive",
            confidence_score=0.52
        ),
        Case(
            case_number="CASE-2024007",
            title="Safety Protocol Violation",
            description="""Clear evidence of safety protocol violations leading to a workplace accident. 
            Security footage and maintenance records show deliberate bypassing of safety measures. 
            Multiple employees confirm the unsafe practices were common.""",
            plaintiff="Safety Inspector",
            defendant="Manufacturing Corp",
            case_type="Workplace Safety",
            verdict="Guilty",
            confidence_score=0.95
        ),
        Case(
            case_number="CASE-2024008",
            title="Service Agreement Breach",
            description="""A dispute over service level agreements. The defendant has provided 
            detailed logs showing compliance with all agreed service levels. Independent 
            audit confirms the defendant's claims.""",
            plaintiff="Client Corp",
            defendant="Service Provider",
            case_type="Contract",
            verdict="Not Guilty",
            confidence_score=0.82
        ),
        Case(
            case_number="CASE-2024009",
            title="Land Use Dispute",
            description="""A complex dispute over land use rights. Historical records are 
            ambiguous, and current usage patterns don't clearly indicate the intended purpose. 
            Expert opinions are conflicting.""",
            plaintiff="Landowners Association",
            defendant="Development Corp",
            case_type="Property",
            verdict="Inconclusive",
            confidence_score=0.48
        ),
        Case(
            case_number="CASE-2024010",
            title="Property Dispute: Land Acquisition",
            description="""A dispute over land acquisition by the government for a highway project. 
            The landowners claim inadequate compensation, while the government argues the valuation 
            is fair. Multiple survey reports and expert opinions are presented.""",
            plaintiff="Landowners Association",
            defendant="National Highways Authority",
            case_type="Property",
            verdict="Inconclusive",
            confidence_score=0.55
        ),
        Case(
            case_number="CASE-2024011",
            title="Criminal Case: Theft and Burglary",
            description="""A case involving theft and burglary at a jewelry store. 
            CCTV footage shows the accused entering the store, but the defense claims 
            the evidence is circumstantial. Witness testimonies are conflicting.""",
            plaintiff="State of Maharashtra",
            defendant="Rahul Sharma",
            case_type="Criminal",
            verdict="Guilty",
            confidence_score=0.78
        ),
        Case(
            case_number="CASE-2024012",
            title="Civil Dispute: Contract Breach",
            description="""A contract dispute between a software company and a client. 
            The client claims the software delivered does not meet the agreed specifications, 
            while the company argues the client changed requirements mid-project.""",
            plaintiff="Tech Solutions Pvt Ltd",
            defendant="Global Enterprises",
            case_type="Contract",
            verdict="Not Guilty",
            confidence_score=0.82
        ),
        Case(
            case_number="CASE-2024013",
            title="Constitutional Case: Right to Privacy",
            description="""A case challenging the constitutionality of a new surveillance law. 
            The petitioners argue the law violates the right to privacy, while the government 
            claims it is necessary for national security. Legal experts are divided on the issue.""",
            plaintiff="Civil Liberties Union",
            defendant="Union of India",
            case_type="Constitutional",
            verdict="Inconclusive",
            confidence_score=0.65
        ),
        Case(
            case_number="CASE-2024014",
            title="Family Dispute: Inheritance",
            description="""A family dispute over inheritance of ancestral property. 
            Multiple heirs claim their share, but the will is ambiguous. 
            Historical documents and family testimonies are presented.""",
            plaintiff="Rajesh Kumar",
            defendant="Family Members",
            case_type="Family",
            verdict="Inconclusive",
            confidence_score=0.58
        ),
        Case(
            case_number="CASE-2024015",
            title="Environmental Case: Pollution",
            description="""A case against a factory for violating environmental regulations. 
            The factory is accused of releasing toxic waste into a river, affecting local communities. 
            Environmental reports and expert testimonies are presented.""",
            plaintiff="Environmental Protection Agency",
            defendant="Industrial Corp",
            case_type="Environmental",
            verdict="Guilty",
            confidence_score=0.88
        ),
        Case(
            case_number="CASE-2024016",
            title="Labor Dispute: Unfair Dismissal",
            description="""A labor dispute over unfair dismissal of employees. 
            The employees claim they were fired without cause, while the company argues 
            it was due to poor performance. Employment records and witness testimonies are presented.""",
            plaintiff="Labor Union",
            defendant="Manufacturing Corp",
            case_type="Labor",
            verdict="Not Guilty",
            confidence_score=0.72
        ),
        Case(
            case_number="CASE-2024017",
            title="Intellectual Property: Patent Infringement",
            description="""A case of patent infringement between two pharmaceutical companies. 
            The plaintiff claims the defendant copied their drug formula, while the defendant 
            argues their product is independently developed. Technical reports and expert opinions are presented.""",
            plaintiff="Pharma Corp",
            defendant="Generic Drugs Ltd",
            case_type="Intellectual Property",
            verdict="Inconclusive",
            confidence_score=0.62
        ),
        Case(
            case_number="CASE-2024018",
            title="Consumer Case: Defective Product",
            description="""A consumer case against a car manufacturer for selling defective vehicles. 
            The consumers claim the cars have a critical safety flaw, while the manufacturer 
            argues the issue is minor and has been addressed. Technical reports and consumer complaints are presented.""",
            plaintiff="Consumer Group",
            defendant="Auto Corp",
            case_type="Consumer",
            verdict="Guilty",
            confidence_score=0.85
        ),
        Case(
            case_number="CASE-2024019",
            title="Tax Dispute: Evasion",
            description="""A tax evasion case against a business owner. 
            The tax authority claims the business underreported income, while the owner 
            argues it was an accounting error. Financial records and expert testimonies are presented.""",
            plaintiff="Income Tax Department",
            defendant="Business Owner",
            case_type="Tax",
            verdict="Not Guilty",
            confidence_score=0.68
        ),
        Case(
            case_number="CASE-2024020",
            title="Public Interest Litigation: Education",
            description="""A public interest litigation case demanding better infrastructure in government schools. 
            The petitioners argue the current conditions violate the right to education, while the government 
            claims budget constraints. Reports and expert opinions are presented.""",
            plaintiff="Education Rights Group",
            defendant="State Government",
            case_type="Public Interest",
            verdict="Inconclusive",
            confidence_score=0.58
        )
    ]
    
    # Add cases to database
    for case in sample_cases:
        session.add(case)
    
    # Commit changes
    session.commit()
    session.close()
    
    print("Database initialized with sample cases!")

if __name__ == "__main__":
    init_db() 