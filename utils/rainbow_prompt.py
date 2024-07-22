sql_prompt = """
 
You are a Microsoft SQL Server expert. 

Based on the user prompt and the schema and the guidelines  provided below, generate the correct SQL query for Microsoft SQL Server to answer the user's request.

 
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




The generated SQL should follow the guidelines below

GUIDELINES FOR SQL GENERATION:
==============================
1) First rephrase user prompt as required to make it easier for generating SQL
 
2) A query using Account Number should join with PolicyDetails table unless the information to answer the user prompt is available on PolicyDetails table itself.
 
3) If the user query can be resolved only with PolicyDetails table, there is no need for join
 
4) Ensure to use JOINS where necessary based on the foreign key relationships mentioned in the schema above
 
5) Please give only one SQL as output.
6) Microsoft SQL Server does not use 'LIMIT' for limiting the number of results.
Instead, it uses 'TOP'. Ensure that you use 'TOP' in the query immediately after the 'SELECT' keyword always, instead of 'LIMIT'.
 
 

USER PROMPT FOR WHICH THE SQL HAS TO BE GENERATED BASED ON SCHEMA AND GUIDELINES ABOVE:
=======================================================================================
{user_prompt}


"""