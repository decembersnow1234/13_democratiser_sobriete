from typing import Optional
from pydantic import BaseModel
from enum import Enum

# WSL Taxonomy

class Author_gender(str, Enum):
    male = 'Male'
    female = 'Female'
    unknown = 'Unknown'

class Author(BaseModel):
    name: str
    gender: Optional[Author_gender]

class Publication_type(str, Enum):
    research_article  = 'Research article'
    article_in_press  = 'Article-in-Press (AiP)'
    book              = 'Book'
    case_study        = 'Case study'
    chapter           = 'Chapter'
    conference_paper  = 'Conference Paper'
    data_paper        = 'Data paper'
    editorial         = 'Editorial'
    erratum           = 'Erratum'
    letter            = 'Letter'
    note              = 'Note'
    retracted_article = 'Retracted article'
    review            = 'Review'
    short_survey      = 'Short survey'
    commentary        = 'Commentary '
    presentation      = 'Presentation'
    technical_report  = 'Technical report'
    policy_report     = 'Policy report'
    policy_brief      = 'Policy brief'
    factsheet         = 'Factsheet'

class Science_type(str, Enum):
    natural_science = 'Natural science'
    social_science  = 'Social science'
    formal_science  = 'Formal science'

class Scientif_discipline(str, Enum):
    ## TODO : Add hierarchy between science_type and scientific_discipline
    # Social science
    anthropology         = 'Anthropology'
    criminology          = 'Criminology'
    geography            = 'Geography'
    economics            = 'Economics'
    education_sciences   = 'Education sciences'
    linguistics          = 'Linguistics'
    military_science     = 'Military science'
    management_science   = 'Management science'
    organization_studies = 'Organization studies'
    political_science    = 'Political science'
    public_health        = 'Public health'
    psychology           = 'Psychology'
    religious_studies    = 'Religious studies'
    sociology            = 'Sociology'

    # Natural science
    biology           = 'Biology'
    earth_science     = 'Earth science'
    chemistry         = 'Chemistry'
    physics           = 'Physics'
    astronomy         = 'Astronomy'
    materials_science = 'Materials science'

    # Formal science
    logic               = 'Logic'
    mathematics         = 'Mathematics'
    statistics          = 'Statistics'
    systems_science     = 'Systems science'
    data_science        = 'Data science'
    information_science = 'Information science'
    computer_science    = 'Computer science'
    cryptography        = 'Cryptography'


class Regional_group(str, Enum): #Mandatory:	YES, Type:	EXCLUSIVE
    world = 'World'
    african_states = 'African States'
    asia_pacific_states = 'Asia-Pacific States'
    eastern_european_states = 'Eastern European States'
    latin_american_and_caribbean_states = 'Latin American and Caribbean States'
    north_america = 'North America'
    western_european = 'Western European'
    oceania = 'Oceania'

class Geographical_scope(str, Enum): #Mandatory:	YES, Type:	MUTLIPLE CHOICE
    global_scope = 'Global'
    countries = 'Countries'
    large_regions = 'Large regions'
    small_regions = 'Small regions'
    local_areas = 'Local areas'



class Studied_country(str, Enum): #Mandatory:	YES, Type:	MUTLIPLE CHOICE
    afghanistan = "Afghanistan"
    albania = "Albania"
    algeria = "Algeria"
    andorra = "Andorra"
    angola = "Angola"
    antigua_and_barbuda = "Antigua and Barbuda"
    argentina = "Argentina"
    armenia = "Armenia"
    australia = "Australia"
    austria = "Austria"
    azerbaijan = "Azerbaijan"
    bahamas = "Bahamas"
    bahrain = "Bahrain"
    bangladesh = "Bangladesh"
    barbados = "Barbados"
    belarus = "Belarus"
    belgium = "Belgium"
    belize = "Belize"
    benin = "Benin"
    bhutan = "Bhutan"
    bolivia = "Bolivia"
    bosnia_and_herzegovina = "Bosnia and Herzegovina"
    botswana = "Botswana"
    brazil = "Brazil"
    brunei_darussalam = "Brunei Darussalam"
    bulgaria = "Bulgaria"
    burkina_faso = "Burkina Faso"
    burundi = "Burundi"
    cabo_verde = "Cabo Verde"
    cambodia = "Cambodia"
    cameroon = "Cameroon"
    canada = "Canada"
    central_african_republic = "Central African Republic"
    chad = "Chad"
    chile = "Chile"
    china = "China"
    colombia = "Colombia"
    comoros = "Comoros"
    congo = "Congo"
    costa_rica = "Costa Rica"
    croatia = "Croatia"
    cuba = "Cuba"
    cyprus = "Cyprus"
    czech_republic = "Czech Republic"
    democratic_republic_of_the_congo = "Democratic Republic of the Congo"
    denmark = "Denmark"
    djibouti = "Djibouti"
    dominica = "Dominica"
    dominican_republic = "Dominican Republic"
    ecuador = "Ecuador"
    egypt = "Egypt"
    el_salvador = "El Salvador"
    equatorial_guinea = "Equatorial Guinea"
    eritrea = "Eritrea"
    estonia = "Estonia"
    eswatini_swaziland = "Eswatini (Swaziland)"
    ethiopia = "Ethiopia"
    fiji = "Fiji"
    finland = "Finland"
    france = "France"
    gabon = "Gabon"
    gambia = "Gambia"
    georgia = "Georgia"
    germany = "Germany"
    ghana = "Ghana"
    greece = "Greece"
    grenada = "Grenada"
    guatemala = "Guatemala"
    guinea = "Guinea"
    guinea_bissau = "Guinea-Bissau"
    guyana = "Guyana"
    haiti = "Haiti"
    honduras = "Honduras"
    hungary = "Hungary"
    iceland = "Iceland"
    india = "India"
    indonesia = "Indonesia"
    iran = "Iran"
    iraq = "Iraq"
    ireland = "Ireland"
    israel = "Israel"
    italy = "Italy"
    jamaica = "Jamaica"
    japan = "Japan"
    jordan = "Jordan"
    kazakhstan = "Kazakhstan"
    kenya = "Kenya"
    kiribati = "Kiribati"
    korea_north = "Korea, North"
    korea_south = "Korea, South"
    kuwait = "Kuwait"
    kyrgyzstan = "Kyrgyzstan"
    laos = "Laos"
    latvia = "Latvia"
    lebanon = "Lebanon"
    lesotho = "Lesotho"
    liberia = "Liberia"
    libya = "Libya"
    liechtenstein = "Liechtenstein"
    lithuania = "Lithuania"
    luxembourg = "Luxembourg"
    madagascar = "Madagascar"
    malawi = "Malawi"
    malaysia = "Malaysia"
    maldives = "Maldives"
    mali = "Mali"
    malta = "Malta"
    marshall_islands = "Marshall Islands"
    mauritania = "Mauritania"
    mauritius = "Mauritius"
    mexico = "Mexico"
    micronesia = "Micronesia"
    moldova = "Moldova"
    monaco = "Monaco"
    mongolia = "Mongolia"
    montenegro = "Montenegro"
    morocco = "Morocco"
    mozambique = "Mozambique"
    myanmar = "Myanmar"
    namibia = "Namibia"
    nauru = "Nauru"
    nepal = "Nepal"
    netherlands = "Netherlands"
    new_zealand = "New Zealand"
    nicaragua = "Nicaragua"
    niger = "Niger"
    nigeria = "Nigeria"
    north_macedonia = "North Macedonia"
    norway = "Norway"
    oman = "Oman"
    pakistan = "Pakistan"
    palau = "Palau"
    panama = "Panama"
    papua_new_guinea = "Papua New Guinea"
    paraguay = "Paraguay"
    peru = "Peru"
    philippines = "Philippines"
    poland = "Poland"
    portugal = "Portugal"
    qatar = "Qatar"
    romania = "Romania"
    russia = "Russia"
    rwanda = "Rwanda"
    saint_kitts_and_nevis = "Saint Kitts and Nevis"
    saint_lucia = "Saint Lucia"
    saint_vincent_and_the_grenadines = "Saint Vincent and the Grenadines"
    samoa = "Samoa"
    san_marino = "San Marino"
    sao_tome_and_principe = "Sao Tome and Principe"
    saudi_arabia = "Saudi Arabia"
    senegal = "Senegal"
    serbia = "Serbia"
    seychelles = "Seychelles"
    sierra_leone = "Sierra Leone"
    singapore = "Singapore"
    slovakia = "Slovakia"
    slovenia = "Slovenia"
    solomon_islands = "Solomon Islands"
    somalia = "Somalia"
    south_africa = "South Africa"
    south_sudan = "South Sudan"
    spain = "Spain"
    sri_lanka = "Sri Lanka"
    sudan = "Sudan"
    suriname = "Suriname"
    sweden = "Sweden"
    switzerland = "Switzerland"
    syria = "Syria"
    tajikistan = "Tajikistan"
    tanzania = "Tanzania"
    thailand = "Thailand"
    timor_leste = "Timor-Leste"
    togo = "Togo"
    tonga = "Tonga"
    trinidad_and_tobago = "Trinidad and Tobago"
    tunisia = "Tunisia"
    turkey = "Turkey"
    turkmenistan = "Turkmenistan"
    tuvalu = "Tuvalu"
    uganda = "Uganda"
    ukraine = "Ukraine"
    united_arab_emirates = "United Arab Emirates"
    united_kingdom = "United Kingdom"
    united_states = "United States"
    uruguay = "Uruguay"
    uzbekistan = "Uzbekistan"
    vanuatu = "Vanuatu"
    vatican_city = "Vatican City (Holy See)"
    venezuela = "Venezuela"
    vietnam = "Vietnam"
    yemen = "Yemen"
    zambia = "Zambia"
    zimbabwe = "Zimbabwe"


class Human_needs(str, Enum):
    nutrition = 'Nutrition'
    shelter_and_living_conditions = 'Shelter and living conditions'
    hygiene = 'Hygiene'
    clothing = 'Clothing'
    healthcare = 'Healthcare'
    education = 'Education'
    communication_and_information = 'Communication and information'
    mobility = 'Mobility'


class Studied_sector(str, Enum):
    agriculture_forestry_fishing = 'Agriculture, forestry, fishing'
    mining_and_quarrying = 'Mining and quarrying'
    manufacturing = 'Manufacturing'
    electricity_gas_steam_air_conditioning = 'Electricity, gas, steam, air conditioning'
    water_sewerage_waste = 'Water, sewerage, waste'
    construction = 'Construction'
    trade_vehicle_motorcycle_repair = 'Trade; vehicle and motorcycle repair'
    transport_storage = 'Transport and storage'
    accommodation_food_services = 'Accommodation and food services'
    information_communication = 'Information and communication'
    financial_insurance_services = 'Financial and insurance services'
    real_estate = 'Real estate'
    professional_scientific_technical_services = 'Professional, scientific, technical services'
    administrative_support_services = 'Administrative and support services'
    public_administration_defence_social_security = 'Public administration, defence, social security'
    education = 'Education'
    health_social_work = 'Health and social work'
    arts_entertainment_recreation = 'Arts, entertainment, recreation'
    other_services = 'Other services'
    household_employment_goods_services_for_own_use = 'Household employment, goods/services for own use'
    extraterritorial_organizations = 'Extraterritorial organizations'

class Studied_policy_area(str, Enum):
    jobs = 'Jobs'
    social_rights = 'Social Rights'
    economy = 'Economy'
    agriculture = 'Agriculture'
    cohesion = 'Cohesion'
    reforms = 'Reforms'
    health = 'Health'
    food = 'Food'
    justice = 'Justice'
    equality = 'Equality'
    home_affairs = 'Home Affairs'
    energy = 'Energy'
    finance_and_capital_markets = 'Finance and Capital Markets'
    innovation_and_research = 'Innovation and Research'
    culture = 'Culture'
    education_and_youth = 'Education and Youth'
    climate_action = 'Climate Action'

class Natural_ressource(str, Enum):
    freshwater = 'Freshwater'
    marine_resources = 'Marine Resources'
    wetlands = 'Wetlands'
    metals_and_ores = 'Metals and Ores'
    non_metallic_minerals = 'Non-Metallic Minerals'
    fossil_fuels = 'Fossil Fuels'
    agricultural_land = 'Agricultural Land'
    forests = 'Forests'
    urban_land = 'Urban Land'
    biomass = 'Biomass'

class Wellbeing(str, Enum):
    housing = 'Housing'
    jobs = 'Jobs'
    education = 'Education'
    civic_engagement = 'Civic Engagement'
    life_satisfaction = 'Life Satisfaction'
    work_life_balance = 'Work-Life Balance'
    income = 'Income'
    community = 'Community'
    environment = 'Environment'
    health = 'Health'
    safety = 'Safety'

class Justice_consideration(str, Enum):
    distributional = 'Distributional'
    procedural = 'Procedural'
    corrective = 'Corrective'
    recognitional = 'Recognitional'
    transitional = 'Transitional'

class Planetary_boundaries(str, Enum):
    land_system_change = 'Land-System Change'
    climate_change = 'Climate Change'
    biosphere_integrity = 'Biosphere Integrity'
    biogeochemical_flows = 'Biogeochemical Flows'
    ocean_acidification = 'Ocean Acidification'
    freshwater_use = 'Freshwater Use'
    atmospheric_aerosol_loading = 'Atmospheric Aerosol Loading'
    ozone_depletion = 'Ozone Depletion'
    introduction_of_novel_entities = 'Introduction of Novel Entities'

class Paper(BaseModel):
    title: str
    authors: list[Author]
    abstract: str
    year_of_publication: int
    peer_reviewed: bool
    grey_literature: bool
    publication_type: Publication_type
    sufficiency_mentioned: bool
    science_type: Science_type
    scientific_discipline: Scientif_discipline
    regional_group: Regional_group
    geographical_scope: Geographical_scope
    studied_country: set[Studied_country]
    human_needs: set[Human_needs]
    studied_sector: set[Studied_sector]
    studied_policy_area: set[Studied_policy_area]
    natural_ressource: set[Natural_ressource]
    wellbeing: set[Wellbeing]
    justice_consideration: Optional[set[Justice_consideration]]
    planetary_boundaries: Optional[set[Planetary_boundaries]]


    ## Optional fields
    keywords: list[str]
    url: Optional[str]
    doi: Optional[str]
    source: Optional[str]
    source_type: Optional[str]
    source_url: Optional[str]
    source_doi: Optional[str]
    source_publication_date: Optional[str]
    source_access_date: Optional[str]
    source_publication_type: Optional[str]
    source_language: Optional[str]
    source_publisher: Optional[str]
    source_publisher_location: Optional[str]
    source_publisher_country: Optional[str]
    source_publisher_contact: Optional[str]
    source_publisher_contact_email: Optional[str]
