import google.generativeai as genai
import os
import time
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=api_key)
models = genai.GenerativeModel('gemini-pro')
    
prompt = """
You are an expert in generating user questions for a Microsoft SQL Server database. Based on the following table schemas, generate a list of questions that users might ask.

Here are the table schemas for the Insurance database:

DATABASE SCHEMA GIVING TABLE NAMES , PRIMARY AND FOREIGN KEYS TO BE USED FOR SQL GENERATION:
===============================================================================================

/****** Object:  Table [PolicyD].[Agency]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[Agency](
	[AgencyID] [varchar](10) NOT NULL,
	[Name] [varchar](255) NULL,
	[AddressLine1] [varchar](255) NULL,
	[AddressLine2] [varchar](255) NULL,
	[City] [varchar](40) NULL,
	[State] [varchar](40) NULL,
	[ZipCode] [varchar](40) NULL,
	[EmailID] [varchar](255) NULL,
	[PhoneNumber] [varchar](40) NULL,
PRIMARY KEY CLUSTERED 
(
	[AgencyID] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [PolicyD].[Coverage]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[Coverage](
	[PolicyNumber] [varchar](40) NOT NULL,
	[CoverageID] [varchar](40) NOT NULL,
	[CoverageCode] [varchar](40) NOT NULL,
	[CoverageDescription] [varchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyNumber] ASC,
	[CoverageID] ASC,
	[CoverageCode] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [PolicyD].[Insured]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[Insured](
	[PolicyNumber] [varchar](40) NOT NULL,
	[Name] [varchar](40) NOT NULL,
	[PolicyRole] [varchar](40) NULL,
	[AddressLine1] [varchar](255) NULL,
	[AddressLine2] [varchar](255) NULL,
	[City] [varchar](40) NULL,
	[State] [varchar](40) NULL,
	[ZipCode] [varchar](40) NULL,
	[EmailID] [varchar](40) NULL,
	[PhoneNumber] [varchar](40) NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyNumber] ASC,
	[Name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [PolicyD].[PolicyDetails]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[PolicyDetails](
	[PolicyNumber] [varchar](40) NOT NULL,
	[LineOfBusiness] [varchar](5) NULL,
	[TermNumber] [varchar](5) NULL,
	[AccountNumber] [varchar](40) NULL,
	[EffectiveDate] [datetime] NULL,
	[ExpirationDate] [datetime] NULL,
	[PolicyStatus] [varchar](2) NULL,
	[PremiumDue] [decimal](18, 2) NULL,
	[PremiumDueDate] [datetime] NULL,
	[PaymentFrequency] [varchar](40) NULL,
	[AgencyID] [varchar](10) NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyNumber] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [PolicyD].[PrimaryInsured]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[PrimaryInsured](
	[PolicyNumber] [varchar](40) NOT NULL,
	[Name] [varchar](40) NOT NULL,
	[AddressLine1] [varchar](255) NULL,
	[AddressLine2] [varchar](255) NULL,
	[City] [varchar](40) NULL,
	[State] [varchar](40) NULL,
	[ZipCode] [varchar](40) NULL,
	[EmailID] [varchar](40) NULL,
	[PhoneNumber] [varchar](40) NULL, 
PRIMARY KEY CLUSTERED 
(
	[PolicyNumber] ASC,
	[Name] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY],
	FOREIGN KEY (PolicyNumber) REFERENCES PolicyDetails(PolicyNumber)
GO
/****** Object:  Table [PolicyD].[Risks]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[Risks](
	[PolicyNumber] [varchar](40) NOT NULL,
	[VehicleUnitNumber] [varchar](40) NULL,
	[CoverageID] [varchar](40) NOT NULL,
	[VehicleMake] [varchar](255) NULL,
	[VehicleModel] [varchar](255) NULL,
	[VehicleYear] [varchar](40) NULL,
	[LocationUnitNumber] [varchar](40) NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyNumber] ASC,
	[CoverageID] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [PolicyD].[SupportingPolicies]    Script Date: 19-07-2024 17:02:08 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [PolicyD].[SupportingPolicies](
	[PolicyNumber] [varchar](40) NOT NULL,
	[SupportingPolicyNumber] [varchar](40) NOT NULL,
	[SupportingPolicyLineOfBusiness] [varchar](40) NULL,
	[SupportingPolicyEffectiveDate] [datetime] NULL,
	[SupportingPolicyExpirationDate] [datetime] NULL,
PRIMARY KEY CLUSTERED 
(
	[PolicyNumber] ASC,
	[SupportingPolicyNumber] ASC
)WITH (STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [PolicyD].[Insured]  WITH CHECK ADD  CONSTRAINT [FK_Insured_PolicyDetails] FOREIGN KEY([PolicyNumber])
REFERENCES [PolicyD].[PolicyDetails] ([PolicyNumber])
GO
ALTER TABLE [PolicyD].[Insured] CHECK CONSTRAINT [FK_Insured_PolicyDetails]
GO
ALTER TABLE [PolicyD].[PolicyDetails]  WITH CHECK ADD  CONSTRAINT [FK_PolicyDetails_Agency] FOREIGN KEY([AgencyID])
REFERENCES [PolicyD].[Agency] ([AgencyID])
GO
ALTER TABLE [PolicyD].[PolicyDetails] CHECK CONSTRAINT [FK_PolicyDetails_Agency]
GO

ALTER TABLE [PolicyD].[SupportingPolicies]  WITH CHECK ADD  CONSTRAINT [FK_SupportingPolicies_PolicyDetails] FOREIGN KEY([PolicyNumber])
REFERENCES [PolicyD].[PolicyDetails] ([PolicyNumber])
GO
ALTER TABLE [PolicyD].[SupportingPolicies] CHECK CONSTRAINT [FK_SupportingPolicies_PolicyDetails]
GO
ALTER TABLE [PolicyD].[Risks]  WITH CHECK ADD  CONSTRAINT [FK_Risks_PolicyDetails] FOREIGN KEY([PolicyNumber])
REFERENCES [PolicyD].[PolicyDetails] ([PolicyNumber])
GO
ALTER TABLE [PolicyD].[Risks] CHECK CONSTRAINT [FK_Risks_PolicyDetails]
GO

ALTER TABLE [PolicyD].[Coverage]  WITH CHECK ADD  CONSTRAINT [FK_Coverage_PolicyDetails] FOREIGN KEY([PolicyNumber])
REFERENCES [PolicyD].[PolicyDetails] ([PolicyNumber])
GO
ALTER TABLE [PolicyD].[Risks] CHECK CONSTRAINT [FK_Coverage_PolicyDetails]
GO

ALTER TABLE PolicyD.Coverage
   ADD CONSTRAINT FK_Coverage_Risks FOREIGN KEY (PolicyNumber, CoverageID )
      REFERENCES PolicyD.Risks (PolicyNumber, CoverageID)
GO
ALTER TABLE [PolicyD].[Coverage] CHECK CONSTRAINT [FK_Coverage_Risks]
GO



Based on these table schemas, please generate a list of 25 unique set of questions not repeated ones, that users might ask for Agency, PolicyDetails, PrimaryInsured, Insured, 
SupportingPolicies, Coverage, Risks. Don't put anything before the questions(hyphen, asterisk).
The questions should always be for one customer AccountNumber as if one customer is asking the question.
Don't write questions like 'with my account number Z011330744'.

PolicyNumber: 1330740, 1330744. 
CoverageID : HO 133074014|000,HO 133074014|000,APV133074428|001,APV133074428|001
VehicleUnitNumber: 001
VehicleMake : ATYTA RAV4
CoverageDescription : HOMEOWNERS,PROPERTY DAMAGE,AUTO MEDICAL PAYMENTS
Name : ANN LAMPKINS

These are some valid data provided above. Accordingly generate questions based on the data provided. 
Include PolicyNumber, CoverageID, VehicleUnitNumber,VehicleMake, VehicleModel, Risks, coverage description, PolicyRole, Name, Policy role  within the questions.
Don't put anything before the questions.
The questions should include a combination of "show", "what", "list down", "which".


Generate various prompts to query the Agency, PolicyDetails, PrimaryInsured, InsuredOther, SupportingPolicies, Coverage, Risks  on provided customer details, 
ensuring to use joins where necessary. The prompts should be a combination of Agency, PolicyDetails, PrimaryInsured, InsuredOther, 
SupportingPolicies, Coverage, Risks. Also try to form combined questions for risks and coverages.
The questions should include a combination of "show", "what", "list down", "which".

The query should return relevant columns from all the tables involved.
"""

def generate_questions(prompt):
    config = genai.types.GenerationConfig(temperature=0)
    response = models.generate_content(prompt, generation_config=config)
    return response.text

if not os.path.exists('test_prompt.txt'):
    with open('test_prompt.txt', 'w') as file:
        questions = generate_questions(prompt)
        file.write(questions)
    print("Questions have been saved to test_prompt.txt")
