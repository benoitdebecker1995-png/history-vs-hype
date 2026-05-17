# Web Lookup Prompt — Round 2 (harder cases)

**Paste the prompt below into Gemini / ChatGPT / Perplexity.**

```
Round 2 lookup. These academic library files weren't resolved in round 1.
Each entry shows: (1) current canonical filename, (2) folder topic, (3) extracted metadata, (4) original filename.

Use the original filename as the strongest hint — it often contains author, year, DOI, or publisher fragments that were missed during slug extraction.

OUTPUT FORMAT: markdown table:
| file_index | title (verified) | author_surname | year | publisher_abbrev | source_url |

Publisher abbreviations: CambridgeUP, OxfordUP, YaleUP, PrincetonUP, ColumbiaUP, IndianaUP,
EdinburghUP, NYUPress, UCPress, JohnsHopkinsUP, HooverPress, PlutoPress, Routledge, Palgrave,
Bloomsbury, ITauris, HurstCo, ZedBooks, VersoBooks, BasicBooks, RandomHouse, Penguin, Brill,
Springer, DaCapo, FreePress, Granta, WeidenfeldNicolson, CornellUP, StanfordUP, HarvardUP,
LiverpoolUP, MacmillanUK, NortonCo, ChicagoUP, MITPress, SyracuseUP, DukeUP, UCLAUP, UNCPress,
WileyBlackwell, SAGEPub, TaylorFrancis, OneWorldPubs, NewPress, ZED, OUPIndia, McGrawHill.

If still unresolved, output 'UNRESOLVED' in that row's title cell.
If it appears to be a personal document, government form, course material, or non-academic content, output 'OFF-TOPIC' in title cell.

---

### 4
- canonical: `FrenchInterventionismSahel-Unknown-0000-Unknown.pdf`
- folder: african-history
- known: title-slug=`FrenchInterventionismSahel` a=`Unknown` y=`0000` p=`Unknown`

### 12
- canonical: `ConflictedColonialisms-Unknown-2022-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`ConflictedColonialisms` a=`Unknown` y=`2022` p=`Unknown`

### 16
- canonical: `GrandfathersSpeakNativeAmericanFolkTales-Unknown-0000-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`GrandfathersSpeakNativeAmericanFolkTales` a=`Unknown` y=`0000` p=`Unknown`

### 17
- canonical: `HalumiiKtapihna-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`HalumiiKtapihna` a=`Unknown` y=`2026` p=`Unknown`

### 18
- canonical: `ImaginationAidedPaintersBrush-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`ImaginationAidedPaintersBrush` a=`Unknown` y=`2026` p=`Unknown`

### 20
- canonical: `LandPapers-Unknown-1980-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`LandPapers` a=`Unknown` y=`1980` p=`Unknown`

### 22
- canonical: `ManifestDeception-Unknown-2024-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`ManifestDeception` a=`Unknown` y=`2024` p=`Unknown`

### 23
- canonical: `NewYorkHistoricalManuscriptsDutch-Unknown-0000-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`NewYorkHistoricalManuscriptsDutch` a=`Unknown` y=`0000` p=`Unknown`

### 24
- canonical: `NotesManhattanPurchase-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`NotesManhattanPurchase` a=`Unknown` y=`2026` p=`Unknown`

### 26
- canonical: `ShagenLetterSmithsonian-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`ShagenLetterSmithsonian` a=`Unknown` y=`2026` p=`Unknown`

### 27
- canonical: `SpanishColonialResearchCenter-Unknown-1991-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`SpanishColonialResearchCenter` a=`Unknown` y=`1991` p=`Unknown`

### 28
- canonical: `StatementVatican-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`StatementVatican` a=`Unknown` y=`2026` p=`Unknown`

### 29
- canonical: `TordesillasSlaveryOrigins-Unknown-2023-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`TordesillasSlaveryOrigins` a=`Unknown` y=`2023` p=`Unknown`

### 30
- canonical: `Treaty-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`Treaty` a=`Unknown` y=`2026` p=`Unknown`

### 32
- canonical: `UncoveringInvisible-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`UncoveringInvisible` a=`Unknown` y=`2026` p=`Unknown`

### 33
- canonical: `Untitled-Unknown-2026-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`Untitled` a=`Unknown` y=`2026` p=`Unknown`

### 35
- canonical: `UtilitiesForcePostcolonialContext-Unknown-2023-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`UtilitiesForcePostcolonialContext` a=`Unknown` y=`2023` p=`Unknown`

### 36
- canonical: `VaticanRepudiatesDoctrineDiscovery-Unknown-2023-Unknown.pdf`
- folder: colonialism-slavery
- known: title-slug=`VaticanRepudiatesDoctrineDiscovery` a=`Unknown` y=`2023` p=`Unknown`

### 37
- canonical: `SantaInquisicionInstructions-Unknown-1667-Antonio-de-Zafra.pdf`
- folder: crusades-christianity
- known: title-slug=`SantaInquisicionInstructions` a=`Unknown` y=`1667` p=`Antonio-de-Zafra`

### 39
- canonical: `AcademicArticle-Unknown-2011-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`AcademicArticle` a=`Unknown` y=`2011` p=`Cambridge-University-Press`

### 40
- canonical: `AcademicArticle-Unknown-2017-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`AcademicArticle` a=`Unknown` y=`2017` p=`Cambridge-University-Press`

### 41
- canonical: `AcademicArticle-Unknown-2021-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`AcademicArticle` a=`Unknown` y=`2021` p=`Cambridge-University-Press`

### 42
- canonical: `AcademicArticle-Unknown-2023-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`AcademicArticle` a=`Unknown` y=`2023` p=`Cambridge-University-Press`

### 43
- canonical: `AfricaReader-Unknown-1998-Unknown.pdf`
- folder: general-history
- known: title-slug=`AfricaReader` a=`Unknown` y=`1998` p=`Unknown`

### 45
- canonical: `AmericanColonizationSocietyReport-Unknown-1503-Unknown.pdf`
- folder: general-history
- known: title-slug=`AmericanColonizationSocietyReport` a=`Unknown` y=`1503` p=`Unknown`

### 46
- canonical: `AmericanJewishHistoricalSociety-Unknown-2015-Johns-Hopkins.pdf`
- folder: general-history
- known: title-slug=`AmericanJewishHistoricalSociety` a=`Unknown` y=`2015` p=`Johns-Hopkins`

### 47
- canonical: `AncientReligionArchaeology-Unknown-2003-Unknown.pdf`
- folder: general-history
- known: title-slug=`AncientReligionArchaeology` a=`Unknown` y=`2003` p=`Unknown`

### 49
- canonical: `Article-Unknown-2013-Unknown.pdf`
- folder: general-history
- known: title-slug=`Article` a=`Unknown` y=`2013` p=`Unknown`

### 50
- canonical: `BalkanStrategyEntenteCentralPowers-Unknown-1974-Unknown.pdf`
- folder: general-history
- known: title-slug=`BalkanStrategyEntenteCentralPowers` a=`Unknown` y=`1974` p=`Unknown`

### 51
- canonical: `BasicFactsUnitedNations-Unknown-2017-United-Nations.pdf`
- folder: general-history
- known: title-slug=`BasicFactsUnitedNations` a=`Unknown` y=`2017` p=`United-Nations`

### 52
- canonical: `BertotTrianaHRcdVolNo-Unknown-1899-Unknown.pdf`
- folder: general-history
- known: title-slug=`BertotTrianaHRcdVolNo` a=`Unknown` y=`1899` p=`Unknown`

### 55
- canonical: `CannibalEncountersEuropeansIsland-Unknown-1944-Unknown.pdf`
- folder: general-history
- known: title-slug=`CannibalEncountersEuropeansIsland` a=`Unknown` y=`1944` p=`Unknown`

### 56
- canonical: `ChristianHistoryReality-Unknown-2000-Unknown.pdf`
- folder: general-history
- known: title-slug=`ChristianHistoryReality` a=`Unknown` y=`2000` p=`Unknown`

### 57
- canonical: `CitiesReader-Unknown-2007-Unknown.pdf`
- folder: general-history
- known: title-slug=`CitiesReader` a=`Unknown` y=`2007` p=`Unknown`

### 58
- canonical: `CopyrightProtectedDocument-Unknown-2015-Unknown.pdf`
- folder: general-history
- known: title-slug=`CopyrightProtectedDocument` a=`Unknown` y=`2015` p=`Unknown`

### 59
- canonical: `CurrencyDevaluationSourceGrowthAfri-Unknown-2022-Unknown.pdf`
- folder: general-history
- known: title-slug=`CurrencyDevaluationSourceGrowthAfri` a=`Unknown` y=`2022` p=`Unknown`

### 60
- canonical: `CyprusProblem-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`CyprusProblem` a=`Unknown` y=`0000` p=`Unknown`

### 61
- canonical: `DebunkingMostMoralCivilizationClaim-Unknown-1520-Unknown.pdf`
- folder: general-history
- known: title-slug=`DebunkingMostMoralCivilizationClaim` a=`Unknown` y=`1520` p=`Unknown`

### 63
- canonical: `DiseaseDemographyAmericas-Unknown-2022-Unknown.pdf`
- folder: general-history
- known: title-slug=`DiseaseDemographyAmericas` a=`Unknown` y=`2022` p=`Unknown`

### 64
- canonical: `DraftLaw-Unknown-1914-Unknown.pdf`
- folder: general-history
- known: title-slug=`DraftLaw` a=`Unknown` y=`1914` p=`Unknown`

### 66
- canonical: `EducationalPolicyUFO-Unknown-2020-Unknown.pdf`
- folder: general-history
- known: title-slug=`EducationalPolicyUFO` a=`Unknown` y=`2020` p=`Unknown`

### 68
- canonical: `EstudiosSaharianos-Unknown-1990-brill.pdf`
- folder: general-history
- known: title-slug=`EstudiosSaharianos` a=`Unknown` y=`1990` p=`brill`

### 69
- canonical: `EtudesAfricaines-Unknown-2003-Unknown.pdf`
- folder: general-history
- known: title-slug=`EtudesAfricaines` a=`Unknown` y=`2003` p=`Unknown`

### 73
- canonical: `FederalEducationPrograms-Unknown-1993-Unknown.pdf`
- folder: general-history
- known: title-slug=`FederalEducationPrograms` a=`Unknown` y=`1993` p=`Unknown`

### 74
- canonical: `FO-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`FO` a=`Unknown` y=`0000` p=`Unknown`

### 75
- canonical: `FODocument-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`FODocument` a=`Unknown` y=`0000` p=`Unknown`

### 76
- canonical: `FranceCommonDenominatorBehindAfricasCoup-Unknown-2023-Unknown.pdf`
- folder: general-history
- known: title-slug=`FranceCommonDenominatorBehindAfricasCoup` a=`Unknown` y=`2023` p=`Unknown`

### 77
- canonical: `FrenchMilitaryIntervention-Unknown-2014-Unknown.pdf`
- folder: general-history
- known: title-slug=`FrenchMilitaryIntervention` a=`Unknown` y=`2014` p=`Unknown`

### 78
- canonical: `GeneralAssemblyThirtiethSession-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`GeneralAssemblyThirtiethSession` a=`Unknown` y=`0000` p=`Unknown`

### 80
- canonical: `GorbachevEraWarsCrises-Unknown-1959-Unknown.pdf`
- folder: general-history
- known: title-slug=`GorbachevEraWarsCrises` a=`Unknown` y=`1959` p=`Unknown`

### 86
- canonical: `HarlotsOfHadramaut-Unknown-1942-Unknown.pdf`
- folder: general-history
- known: title-slug=`HarlotsOfHadramaut` a=`Unknown` y=`1942` p=`Unknown`

### 87
- canonical: `HarvardDesignLibraryCatalogue-Unknown-1968-Harvard-University-Press.pdf`
- folder: general-history
- known: title-slug=`HarvardDesignLibraryCatalogue` a=`Unknown` y=`1968` p=`Harvard-University-Press`

### 88
- canonical: `HashDocument-Unknown-2020-Unknown.pdf`
- folder: general-history
- known: title-slug=`HashDocument` a=`Unknown` y=`2020` p=`Unknown`

### 89
- canonical: `HeracleiteanFluxPlato-Unknown-1994-Unknown.pdf`
- folder: general-history
- known: title-slug=`HeracleiteanFluxPlato` a=`Unknown` y=`1994` p=`Unknown`

### 91
- canonical: `HispanicAmericanHistorical-Unknown-0000-Duke-University-Press.pdf`
- folder: general-history
- known: title-slug=`HispanicAmericanHistorical` a=`Unknown` y=`0000` p=`Duke-University-Press`

### 92
- canonical: `HistoriaGeneralPerúComentariosReales-Unknown-1800-Unknown.pdf`
- folder: general-history
- known: title-slug=`HistoriaGeneralPerúComentariosReales` a=`Unknown` y=`1800` p=`Unknown`

### 93
- canonical: `HNetReviews-Unknown-2010-Unknown.pdf`
- folder: general-history
- known: title-slug=`HNetReviews` a=`Unknown` y=`2010` p=`Unknown`

### 95
- canonical: `ImaArticle-Unknown-1905-brill.pdf`
- folder: general-history
- known: title-slug=`ImaArticle` a=`Unknown` y=`1905` p=`brill`

### 96
- canonical: `ImagerySurveyArchaeologyGeoPacha-Unknown-2023-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`ImagerySurveyArchaeologyGeoPacha` a=`Unknown` y=`2023` p=`Cambridge-University-Press`

### 99
- canonical: `InfanticideSacrificesArchaicBabies-Unknown-2013-Unknown.pdf`
- folder: general-history
- known: title-slug=`InfanticideSacrificesArchaicBabies` a=`Unknown` y=`2013` p=`Unknown`

### 100
- canonical: `IntroductionBerbersMaghrib-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`IntroductionBerbersMaghrib` a=`Unknown` y=`0000` p=`Unknown`

### 103
- canonical: `JournalEconomicHistory-Unknown-2021-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`JournalEconomicHistory` a=`Unknown` y=`2021` p=`Cambridge-University-Press`

### 104
- canonical: `JournalMedievalStudies-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`JournalMedievalStudies` a=`Unknown` y=`0000` p=`Unknown`

### 105
- canonical: `JSAPaper-Unknown-1984-Unknown.pdf`
- folder: general-history
- known: title-slug=`JSAPaper` a=`Unknown` y=`1984` p=`Unknown`

### 106
- canonical: `July-Unknown-1941-Unknown.pdf`
- folder: general-history
- known: title-slug=`July` a=`Unknown` y=`1941` p=`Unknown`

### 109
- canonical: `KlassiekeNvtholozie-Unknown-2021-Unknown.pdf`
- folder: general-history
- known: title-slug=`KlassiekeNvtholozie` a=`Unknown` y=`2021` p=`Unknown`

### 112
- canonical: `LatinAmericanStudies-Unknown-0000-Cambridge-University-Press.pdf`
- folder: general-history
- known: title-slug=`LatinAmericanStudies` a=`Unknown` y=`0000` p=`Cambridge-University-Press`

### 113
- canonical: `LawStatusJews-Unknown-1940-Unknown.pdf`
- folder: general-history
- known: title-slug=`LawStatusJews` a=`Unknown` y=`1940` p=`Unknown`

### 114
- canonical: `LegitimateSphereInfluenceUnderstanding-Unknown-2020-Unknown.pdf`
- folder: general-history
- known: title-slug=`LegitimateSphereInfluenceUnderstanding` a=`Unknown` y=`2020` p=`Unknown`

### 115
- canonical: `LicenseDOI-Unknown-1905-brill.pdf`
- folder: general-history
- known: title-slug=`LicenseDOI` a=`Unknown` y=`1905` p=`brill`

### 116
- canonical: `LinesDrawnEmptyMapIraqBorder-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`LinesDrawnEmptyMapIraqBorder` a=`Unknown` y=`0000` p=`Unknown`

### 117
- canonical: `LoiStatutJuifs-Unknown-1940-Unknown.pdf`
- folder: general-history
- known: title-slug=`LoiStatutJuifs` a=`Unknown` y=`1940` p=`Unknown`

### 118
- canonical: `MenWomenPower-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`MenWomenPower` a=`Unknown` y=`0000` p=`Unknown`

### 119
- canonical: `MoroccanKingSahara-Unknown-2025-Unknown.pdf`
- folder: general-history
- known: title-slug=`MoroccanKingSahara` a=`Unknown` y=`2025` p=`Unknown`

### 120
- canonical: `MoroccoGE-Unknown-2024-Unknown.pdf`
- folder: general-history
- known: title-slug=`MoroccoGE` a=`Unknown` y=`2024` p=`Unknown`

### 121
- canonical: `MostMoralCivilization-Unknown-1520-Unknown.pdf`
- folder: general-history
- known: title-slug=`MostMoralCivilization` a=`Unknown` y=`1520` p=`Unknown`

### 123
- canonical: `NaturalResourceExploitationWesternSahara-Unknown-2021-Unknown.pdf`
- folder: general-history
- known: title-slug=`NaturalResourceExploitationWesternSahara` a=`Unknown` y=`2021` p=`Unknown`

### 124
- canonical: `NaturalRightsLaw-Unknown-0000-Emory.pdf`
- folder: general-history
- known: title-slug=`NaturalRightsLaw` a=`Unknown` y=`0000` p=`Emory`

### 125
- canonical: `NurembergWarCriminals-Unknown-1946-Unknown.pdf`
- folder: general-history
- known: title-slug=`NurembergWarCriminals` a=`Unknown` y=`1946` p=`Unknown`

### 126
- canonical: `NWIGArticle-Unknown-2025-Brill.pdf`
- folder: general-history
- known: title-slug=`NWIGArticle` a=`Unknown` y=`2025` p=`Brill`

### 128
- canonical: `OutdoorLifeFishingAdventures-Unknown-2013-Unknown.pdf`
- folder: general-history
- known: title-slug=`OutdoorLifeFishingAdventures` a=`Unknown` y=`2013` p=`Unknown`

### 129
- canonical: `PalaeogeographicalReconstruction-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`PalaeogeographicalReconstruction` a=`Unknown` y=`0000` p=`Unknown`

### 130
- canonical: `PARIJournal-Unknown-2019-Unknown.pdf`
- folder: general-history
- known: title-slug=`PARIJournal` a=`Unknown` y=`2019` p=`Unknown`

### 131
- canonical: `ProblemHttps-Unknown-1999-Unknown.pdf`
- folder: general-history
- known: title-slug=`ProblemHttps` a=`Unknown` y=`1999` p=`Unknown`

### 137
- canonical: `ReportSuperintendentPublicInstruction-Unknown-2025-Brill.pdf`
- folder: general-history
- known: title-slug=`ReportSuperintendentPublicInstruction` a=`Unknown` y=`2025` p=`Brill`

### 138
- canonical: `RevistaCubanaDerecho-Unknown-1993-Unknown.pdf`
- folder: general-history
- known: title-slug=`RevistaCubanaDerecho` a=`Unknown` y=`1993` p=`Unknown`

### 140
- canonical: `RWARADocument-Unknown-2013-Unknown.pdf`
- folder: general-history
- known: title-slug=`RWARADocument` a=`Unknown` y=`2013` p=`Unknown`

### 141
- canonical: `SamenvattingDeConstructieVanHetVerleden-Unknown-0000-StuDocu.pdf`
- folder: general-history
- known: title-slug=`SamenvattingDeConstructieVanHetVerleden` a=`Unknown` y=`0000` p=`StuDocu`

### 142
- canonical: `ScientificArticle-Unknown-2025-Unknown.pdf`
- folder: general-history
- known: title-slug=`ScientificArticle` a=`Unknown` y=`2025` p=`Unknown`

### 143
- canonical: `SouthamptonProjects-Unknown-1991-Unknown.pdf`
- folder: general-history
- known: title-slug=`SouthamptonProjects` a=`Unknown` y=`1991` p=`Unknown`

### 144
- canonical: `StatistickiGodisnjak-Unknown-1939-Unknown.pdf`
- folder: general-history
- known: title-slug=`StatistickiGodisnjak` a=`Unknown` y=`1939` p=`Unknown`

### 145
- canonical: `StyleManual-Unknown-1978-Unknown.pdf`
- folder: general-history
- known: title-slug=`StyleManual` a=`Unknown` y=`1978` p=`Unknown`

### 146
- canonical: `SuisseNovember-Unknown-2014-Unknown.pdf`
- folder: general-history
- known: title-slug=`SuisseNovember` a=`Unknown` y=`2014` p=`Unknown`

### 147
- canonical: `TeotihuacanTenochtitlan-Unknown-2019-Unknown.pdf`
- folder: general-history
- known: title-slug=`TeotihuacanTenochtitlan` a=`Unknown` y=`2019` p=`Unknown`

### 149
- canonical: `TIRLALAKSA-Unknown-2021-verso.pdf`
- folder: general-history
- known: title-slug=`TIRLALAKSA` a=`Unknown` y=`2021` p=`verso`

### 154
- canonical: `TropicalConservationScience-Unknown-2009-Unknown.pdf`
- folder: general-history
- known: title-slug=`TropicalConservationScience` a=`Unknown` y=`2009` p=`Unknown`

### 155
- canonical: `TrueReligionNikolaj-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`TrueReligionNikolaj` a=`Unknown` y=`0000` p=`Unknown`

### 157
- canonical: `UnidentifiableDocument-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`UnidentifiableDocument` a=`Unknown` y=`0000` p=`Unknown`

### 158
- canonical: `UnidentifiableDocument-Unknown-2021-Unknown.pdf`
- folder: general-history
- known: title-slug=`UnidentifiableDocument` a=`Unknown` y=`2021` p=`Unknown`

### 159
- canonical: `UnknownDocument-Unknown-0000-Oxford.pdf`
- folder: general-history
- known: title-slug=`UnknownDocument` a=`Unknown` y=`0000` p=`Oxford`

### 160
- canonical: `UnknownDocument-Unknown-2004-Oxford-University-Press.pdf`
- folder: general-history
- known: title-slug=`UnknownDocument` a=`Unknown` y=`2004` p=`Oxford-University-Press`

### 161
- canonical: `UnreadableDocument-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`UnreadableDocument` a=`Unknown` y=`0000` p=`Unknown`

### 162
- canonical: `UntitledDocument-Unknown-2014-Unknown.pdf`
- folder: general-history
- known: title-slug=`UntitledDocument` a=`Unknown` y=`2014` p=`Unknown`

### 163
- canonical: `VerhalenGebeurtenissen-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`VerhalenGebeurtenissen` a=`Unknown` y=`0000` p=`Unknown`

### 165
- canonical: `VojnuciDefter-Unknown-1455-Unknown.pdf`
- folder: general-history
- known: title-slug=`VojnuciDefter` a=`Unknown` y=`1455` p=`Unknown`

### 166
- canonical: `VojnuciDefter1455-Unknown-2020-Unknown.pdf`
- folder: general-history
- known: title-slug=`VojnuciDefter1455` a=`Unknown` y=`2020` p=`Unknown`

### 167
- canonical: `WarriorWomen-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`WarriorWomen` a=`Unknown` y=`0000` p=`Unknown`

### 168
- canonical: `WehrmachtWWII-Unknown-1948-Oxford-University-Press.pdf`
- folder: general-history
- known: title-slug=`WehrmachtWWII` a=`Unknown` y=`1948` p=`Oxford-University-Press`

### 169
- canonical: `WesternSaharaSettlerColony-Unknown-2025-Unknown.pdf`
- folder: general-history
- known: title-slug=`WesternSaharaSettlerColony` a=`Unknown` y=`2025` p=`Unknown`

### 170
- canonical: `WhatWeKnewLost-Unknown-2019-Unknown.pdf`
- folder: general-history
- known: title-slug=`WhatWeKnewLost` a=`Unknown` y=`2019` p=`Unknown`

### 173
- canonical: `WisconsinECIAEvaluation-Unknown-1983-Unknown.pdf`
- folder: general-history
- known: title-slug=`WisconsinECIAEvaluation` a=`Unknown` y=`1983` p=`Unknown`

### 176
- canonical: `WorldHistory-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`WorldHistory` a=`Unknown` y=`0000` p=`Unknown`

### 180
- canonical: `ОписаниеКарабагскойпровинциисоставленное-Unknown-1823-Unknown.pdf`
- folder: general-history
- known: title-slug=`ОписаниеКарабагскойпровинциисоставленное` a=`Unknown` y=`1823` p=`Unknown`

### 181
- canonical: `AnitaShapiraIsraelHistory-Unknown-0000-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`AnitaShapiraIsraelHistory` a=`Unknown` y=`0000` p=`Unknown`

### 184
- canonical: `CaseIsrael-Unknown-0000-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`CaseIsrael` a=`Unknown` y=`0000` p=`Unknown`

### 188
- canonical: `HeraclitusIran-Unknown-2019-University-of-Chicago-Press.pdf`
- folder: middle-east-history
- known: title-slug=`HeraclitusIran` a=`Unknown` y=`2019` p=`University-of-Chicago-Press`

### 190
- canonical: `IslamicInterpretiveTraditionGender-Unknown-0000-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`IslamicInterpretiveTraditionGender` a=`Unknown` y=`0000` p=`Unknown`

### 194
- canonical: `ParanoidApocalypseHundredYearRetrospecti-Unknown-0000-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`ParanoidApocalypseHundredYearRetrospecti` a=`Unknown` y=`0000` p=`Unknown`

### 196
- canonical: `RoutledgeRevivalsFrancescoGabrieliArabHi-Unknown-2011-Routledge.pdf`
- folder: middle-east-history
- known: title-slug=`RoutledgeRevivalsFrancescoGabrieliArabHi` a=`Unknown` y=`2011` p=`Routledge`

### 199
- canonical: `TreatiesAndOtherInternationalActsOfTheUnitedS-Unknown-0000-Google.pdf`
- folder: middle-east-history
- known: title-slug=`TreatiesAndOtherInternationalActsOfTheUnitedS` a=`Unknown` y=`0000` p=`Google`

### 200
- canonical: `UnknownTitle-Unknown-1797-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`UnknownTitle` a=`Unknown` y=`1797` p=`Unknown`

### 201
- canonical: `UnknownTitle-Unknown-2017-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`UnknownTitle` a=`Unknown` y=`2017` p=`Unknown`

### 202
- canonical: `UnknownTitle-Unknown-2020-Johns-Hopkins.pdf`
- folder: middle-east-history
- known: title-slug=`UnknownTitle` a=`Unknown` y=`2020` p=`Johns-Hopkins`

### 204
- canonical: `YazDYighInstitutePalestineStudiesArmedSt-Unknown-1949-Unknown.pdf`
- folder: middle-east-history
- known: title-slug=`YazDYighInstitutePalestineStudiesArmedSt` a=`Unknown` y=`1949` p=`Unknown`

### 205
- canonical: `JSTORIndia-Unknown-0000-JSTOR.pdf`
- folder: reference-methodology
- known: title-slug=`JSTORIndia` a=`Unknown` y=`0000` p=`JSTOR`

### 207
- canonical: `Bakass-Unknown-0000-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`Bakass` a=`Unknown` y=`0000` p=`Unknown`

### 209
- canonical: `CompleteCollectionTreaties-Unknown-0000-Google.pdf`
- folder: territorial-disputes
- known: title-slug=`CompleteCollectionTreaties` a=`Unknown` y=`0000` p=`Google`

### 210
- canonical: `CordobaAgreement-Unknown-2006-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`CordobaAgreement` a=`Unknown` y=`2006` p=`Unknown`

### 212
- canonical: `HonurasConstitution-Unknown-0000-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`HonurasConstitution` a=`Unknown` y=`0000` p=`Unknown`

### 213
- canonical: `LetterFixedReplica-Unknown-0000-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`LetterFixedReplica` a=`Unknown` y=`0000` p=`Unknown`

### 214
- canonical: `News-Unknown-0000-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`News` a=`Unknown` y=`0000` p=`Unknown`

### 216
- canonical: `PartitionOfBritishIndia-Unknown-0000-TheNationalArchives.pdf`
- folder: territorial-disputes
- known: title-slug=`PartitionOfBritishIndia` a=`Unknown` y=`0000` p=`TheNationalArchives`

### 217
- canonical: `PartitionPunjabCompilationOfficialDocuments-Unknown-1947-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`PartitionPunjabCompilationOfficialDocuments` a=`Unknown` y=`1947` p=`Unknown`

### 219
- canonical: `ReportCommissionEnquiryNorthBorneoSarawak-Unknown-0000-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`ReportCommissionEnquiryNorthBorneoSarawak` a=`Unknown` y=`0000` p=`Unknown`

### 220
- canonical: `StatelessInBakassiHowChangedBorderLeftInhabit-Unknown-0000-JusticeInitiative.pdf`
- folder: territorial-disputes
- known: title-slug=`StatelessInBakassiHowChangedBorderLeftInhabit` a=`Unknown` y=`0000` p=`JusticeInitiative`

### 222
- canonical: `UKPGA-Unknown-1947-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`UKPGA` a=`Unknown` y=`1947` p=`Unknown`

### 223
- canonical: `Wright-Unknown-1966-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`Wright` a=`Unknown` y=`1966` p=`Unknown`

### 224
- canonical: `Unknown-Unknown-0000-Unknown.pdf`
- folder: african-history
- known: title-slug=`Unknown` a=`Unknown` y=`0000` p=`Unknown`

### 225
- canonical: `Unknown-Unknown-0000-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`0000` p=`Unknown`

### 226
- canonical: `Unknown-Unknown-1933-brill.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1933` p=`brill`

### 227
- canonical: `Unknown-Unknown-1940-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1940` p=`Unknown`

### 228
- canonical: `Unknown-Unknown-1942-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1942` p=`Unknown`

### 229
- canonical: `Unknown-Unknown-1949-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1949` p=`Unknown`

### 230
- canonical: `Unknown-Unknown-1962-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1962` p=`Unknown`

### 231
- canonical: `Unknown-Unknown-1965-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1965` p=`Unknown`

### 232
- canonical: `Unknown-Unknown-1967-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1967` p=`Unknown`

### 233
- canonical: `Unknown-Unknown-1997-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`1997` p=`Unknown`

### 234
- canonical: `Unknown-Unknown-2013-Routledge.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2013` p=`Routledge`

### 235
- canonical: `Unknown-Unknown-2013-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2013` p=`Unknown`

### 236
- canonical: `Unknown-Unknown-2015-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2015` p=`Unknown`

### 237
- canonical: `Unknown-Unknown-2016-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2016` p=`Unknown`

### 238
- canonical: `Unknown-Unknown-2021-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2021` p=`Unknown`

### 239
- canonical: `Unknown-Unknown-2022-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2022` p=`Unknown`

### 240
- canonical: `Unknown-Unknown-2024-Springer.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2024` p=`Springer`

### 241
- canonical: `Unknown-Unknown-2024-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2024` p=`Unknown`

### 242
- canonical: `Unknown-Unknown-2025-Unknown.pdf`
- folder: general-history
- known: title-slug=`Unknown` a=`Unknown` y=`2025` p=`Unknown`

### 243
- canonical: `Unknown-Unknown-1966-Unknown.pdf`
- folder: territorial-disputes
- known: title-slug=`Unknown` a=`Unknown` y=`1966` p=`Unknown`

### 244
- canonical: `Unknown-Unknown-2017-CambridgeUP.pdf`
- folder: territorial-disputes
- known: title-slug=`Unknown` a=`Unknown` y=`2017` p=`CambridgeUP`

```

---

## Stats
- Total in round 2: **158** academic entries
- Skipped as likely off-topic (separate stash decision): 34

## Pre-flagged as likely off-topic (NOT in prompt above)

These look like personal docs / D&D / EU youth program / govt forms. Review whether to stash them:

- `[general-history] AlsJeVoorHetEerstDeelneemt-Unknown-2020-Unknown.pdf`
- `[general-history] Ardennendagtocht-Unknown-2020-Unknown.pdf`
- `[general-history] BolComFactuur-Unknown-2019-Unknown.pdf`
- `[general-history] Calendar-Unknown-2025-Unknown.pdf`
- `[general-history] DeclarationAccessUniversityBachelorProgramme-Unknown-0000-GhentUniversity.pdf`
- `[general-history] DungeonsDragonsDungeonMastersGuide-Unknown-2024-AnnaArchive.pdf`
- `[general-history] EnglishCommonEntrance-Unknown-2016-Unknown.pdf`
- `[general-history] EuropassDocument-Unknown-2019-Unknown.pdf`
- `[general-history] ExploreSolidarityProjects-Unknown-2020-Unknown.pdf`
- `[general-history] GeneralIntroductionESC-Unknown-2020-Unknown.pdf`
- `[general-history] GrimHollowCampaignGuide-Unknown-0000-Unknown.pdf`
- `[general-history] GrimHollowMonsterGrimoire-Unknown-0000-Unknown.pdf`
- `[general-history] GrimhollowPlayerGuide-Unknown-0000-Unknown.pdf`
- `[general-history] GrimhollowSubclasses-Unknown-2025-Unknown.pdf`
- `[general-history] Hageprot-Unknown-2008-Harvard-University-Press.pdf`
- `[general-history] HouseRulesRappan-Unknown-2014-Unknown.pdf`
- `[general-history] JODEFDocument-Unknown-1941-Unknown.pdf`
- `[general-history] JORFDocument-Unknown-1940-Unknown.pdf`
- `[general-history] KlaprozenlaanDocument-Unknown-0000-Unknown.pdf`
- `[general-history] KlaprozenlaanDocument-Unknown-2021-Unknown.pdf`
- `[general-history] KMBTC364Document-Unknown-2013-Unknown.pdf`
- `[general-history] KreativUngCulturalProject-Unknown-2020-Unknown.pdf`
- `[general-history] OrdonnanceAllemande-Unknown-1940-Unknown.pdf`
- `[general-history] ProgramOutlineMay28-Unknown-2021-Unknown.pdf`
- `[general-history] RappanAthuk-Unknown-2012-Unknown.pdf`
- `[general-history] RappanAthukHouseRules-Unknown-2014-Unknown.pdf`
- `[general-history] RimeOfTheFrostmaidenCampaignGuide-Unknown-0000-Unknown.pdf`
- `[general-history] Toelatingsvoorwaarden-Unknown-2015-Unknown.pdf`
- `[general-history] TransaccionAutorizacion-Unknown-2025-Unknown.pdf`
- `[general-history] TransactionDocument-Unknown-2025-Unknown.pdf`
- `[general-history] WordSourDocument-Unknown-2024-Unknown.pdf`
- `[general-history] WordSyllabus-Unknown-2019-Unknown.pdf`
- `[general-history] ZichtrekeningInvest-Unknown-2021-Unknown.pdf`
- `[general-history] ZichtrekeningInvest-Unknown-2022-Unknown.pdf`


| file_index | title (verified) | author_surname | year | publisher_abbrev | source_url |
| --- | --- | --- | --- | --- | --- |
| 4 | French Military Intervention in the Sahel: The Limits of Strategy | Powell | 2020 | CambridgeUP | [https://doi.org/10.1017/9781108579476](https://www.google.com/search?q=https://doi.org/10.1017/9781108579476) |
| 12 | Conflicted Colonialisms: Multi-dimensional Violence in the Sahel | McGiffin | 2022 | Routledge | [https://doi.org/10.1080/23802014.2022.2099573]() |
| 16 | Grandfathers Speak: Native American Folk Tales of the Lenape | Hitakonanu'laxk | 1994 | UNRESOLVED | [https://www.worldcat.org/title/28225575]() |
| 17 | Halumii Ktapihna (Our Other Language) | Hitakonanu'laxk | 1994 | UNRESOLVED | [https://www.worldcat.org/title/28225575]() |
| 18 | Imagination Aided by the Painter's Brush: The Schaghen Letter | UNRESOLVED | 1626 | OFF-TOPIC | [https://www.newnetherlandinstitute.org/history-and-heritage/digital-exhibitions/the-schaghen-letter/]() |
| 20 | UNRESOLVED | UNRESOLVED | 1980 | UNRESOLVED | UNRESOLVED |
| 22 | Manifest Deception: The 'Purchase' of Manhattan | UNRESOLVED | 2024 | UNRESOLVED | UNRESOLVED |
| 23 | New York Historical Manuscripts: Dutch | Gehring | 1980 | UNRESOLVED | [https://www.worldcat.org/title/6331163]() |
| 24 | UNRESOLVED | UNRESOLVED | 2026 | UNRESOLVED | UNRESOLVED |
| 26 | The Schaghen Letter of 1626 | Schaghen | 1626 | OFF-TOPIC | [https://www.nps.gov/stli/learn/historyculture/the-schaghen-letter.htm]() |
| 27 | Spanish Colonial Research Center (Newsletter/Monograph) | UNRESOLVED | 1991 | OFF-TOPIC | [https://www.nps.gov/orgs/1570/index.htm]() |
| 28 | Statement on the 'Doctrine of Discovery' | Vatican | 2023 | OFF-TOPIC | [https://press.vatican.va/content/salastampa/en/bollettino/pubblico/2023/03/30/230330b.html]() |
| 29 | The Treaty of Tordesillas and the Origins of Slavery | UNRESOLVED | 2023 | UNRESOLVED | UNRESOLVED |
| 30 | UNRESOLVED | UNRESOLVED | 2026 | UNRESOLVED | UNRESOLVED |
| 32 | UNRESOLVED | UNRESOLVED | 2026 | UNRESOLVED | UNRESOLVED |
| 33 | UNRESOLVED | UNRESOLVED | 2026 | UNRESOLVED | UNRESOLVED |
| 35 | (Dis)utilities of Force in a Postcolonial Context | Bertrand | 2023 | Routledge | [https://doi.org/10.1080/17502977.2023.2278268]() |
| 36 | Vatican Repudiates the 'Doctrine of Discovery' | Vatican | 2023 | OFF-TOPIC | [https://press.vatican.va/content/salastampa/en/bollettino/pubblico/2023/03/30/230330b.html]() |
| 37 | Instrucciones del Santo Oficio de la Inquisición | Zafra | 1667 | UNRESOLVED | [https://www.worldcat.org/title/253457194]() |
| 39 | UNRESOLVED | UNRESOLVED | 2011 | CambridgeUP | UNRESOLVED |
| 40 | UNRESOLVED | UNRESOLVED | 2017 | CambridgeUP | UNRESOLVED |
| 41 | UNRESOLVED | UNRESOLVED | 2021 | CambridgeUP | UNRESOLVED |
| 42 | UNRESOLVED | UNRESOLVED | 2023 | CambridgeUP | UNRESOLVED |
| 43 | The Africa Reader | Collins | 1994 | RandomHouse | [https://www.penguinrandomhouse.com/books/31103/the-africa-reader-by-edited-and-with-introductions-by-robert-o-collins/]() |
| 45 | Report of the American Colonization Society | UNRESOLVED | 1823 | OFF-TOPIC | [https://www.loc.gov/item/08006856/]() |
| 46 | American Jewish History (Journal) | UNRESOLVED | 2015 | JohnsHopkinsUP | [https://www.press.jhu.edu/journals/american-jewish-history]() |
| 47 | Ancient Religion and Archaeology | UNRESOLVED | 2003 | UNRESOLVED | UNRESOLVED |
| 49 | UNRESOLVED | UNRESOLVED | 2013 | UNRESOLVED | UNRESOLVED |
| 50 | The Balkan Strategy of the Entente and the Central Powers | UNRESOLVED | 1974 | UNRESOLVED | UNRESOLVED |
| 51 | Basic Facts about the United Nations | UN | 2017 | OFF-TOPIC | [https://shop.un.org/books/basic-facts-about-united-nations-42nd-edition-61139]() |
| 52 | OFF-TOPIC | OFF-TOPIC | 1899 | OFF-TOPIC | OFF-TOPIC |
| 55 | Cannibal Encounters: Europeans and Island Caribs, 1492–1763 | Boucher | 1992 | JohnsHopkinsUP | [https://jhupbooks.press.jhu.edu/title/cannibal-encounters]() |
| 56 | UNRESOLVED | UNRESOLVED | 2000 | UNRESOLVED | UNRESOLVED |
| 57 | The Cities Reader | LeGates | 2007 | Routledge | [https://www.routledge.com/The-Cities-Reader/LeGates-Stout/p/book/9780415744478]() |
| 58 | OFF-TOPIC | OFF-TOPIC | 2015 | OFF-TOPIC | OFF-TOPIC |
| 59 | UNRESOLVED | UNRESOLVED | 2022 | UNRESOLVED | UNRESOLVED |
| 60 | The Cyprus Problem: What Everyone Needs to Know | Ker-Lindsay | 2011 | OxfordUP | [https://global.oup.com/academic/product/the-cyprus-problem-9780199757169]() |
| 61 | OFF-TOPIC | OFF-TOPIC | 1520 | OFF-TOPIC | OFF-TOPIC |
| 63 | The Native Population of the Americas in 1492 | Denevan | 1992 | UNCPress | [https://www.ucpress.edu/book/9780299134549/the-native-population-of-the-americas-in-1492]() |
| 64 | OFF-TOPIC | OFF-TOPIC | 1914 | OFF-TOPIC | OFF-TOPIC |
| 66 | OFF-TOPIC | OFF-TOPIC | 2020 | OFF-TOPIC | OFF-TOPIC |
| 68 | Estudios Saharianos | Caro Baroja | 1955 | Brill | [https://brill.com/display/title/5217]() |
| 69 | Etudes Africaines (Series) | UNRESOLVED | 2003 | UNRESOLVED | UNRESOLVED |
| 73 | OFF-TOPIC | OFF-TOPIC | 1993 | OFF-TOPIC | OFF-TOPIC |
| 74 | OFF-TOPIC | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 75 | OFF-TOPIC | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 76 | UNRESOLVED | UNRESOLVED | 2023 | UNRESOLVED | UNRESOLVED |
| 77 | French Military Intervention (Article/Report) | UNRESOLVED | 2014 | UNRESOLVED | UNRESOLVED |
| 78 | OFF-TOPIC | OFF-TOPIC | 1975 | OFF-TOPIC | OFF-TOPIC |
| 80 | The Gorbachev Era: Wars and Crises | UNRESOLVED | 1959 | UNRESOLVED | UNRESOLVED |
| 86 | Harlots of Hadramaut | UNRESOLVED | 1942 | UNRESOLVED | UNRESOLVED |
| 87 | OFF-TOPIC | OFF-TOPIC | 1968 | HarvardUP | OFF-TOPIC |
| 88 | OFF-TOPIC | OFF-TOPIC | 2020 | OFF-TOPIC | OFF-TOPIC |
| 89 | Heraclitean Flux: Plato and the Ancient World | Gerson | 2007 | CambridgeUP | [https://doi.org/10.1017/CBO9780511482397]() |
| 91 | Hispanic American Historical Review (Journal) | UNRESOLVED | 0000 | DukeUP | [https://read.dukeupress.edu/hahr]() |
| 92 | Comentarios Reales de los Incas | Garcilaso | 1609 | UNRESOLVED | [https://www.loc.gov/item/02008434/]() |
| 93 | H-Net Reviews | UNRESOLVED | 2010 | OFF-TOPIC | [https://www.h-net.org/reviews/]() |
| 95 | IJMES (International Journal of Middle East Studies) | UNRESOLVED | 1905 | CambridgeUP | [https://www.cambridge.org/core/journals/international-journal-of-middle-east-studies]() |
| 96 | Eyes from the Machine: AI-Assisted Satellite Archaeology | Casana | 2021 | CambridgeUP | [https://doi.org/10.1017/aqy.2020.113]() |
| 99 | Infanticide and Sacrifices: Archaic Babies | Xella | 2013 | Routledge | [https://www.routledge.com/9781844655519]() |
| 100 | Introduction to the Berbers of the Maghrib | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 103 | The Journal of Economic History | UNRESOLVED | 2021 | CambridgeUP | [https://www.cambridge.org/core/journals/journal-of-economic-history]() |
| 104 | Journal of Medieval Studies | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 105 | JSAP (Journal of the Society of Americanists) | UNRESOLVED | 1984 | UNRESOLVED | [https://www.jstor.org/journal/jsoceamer]() |
| 106 | OFF-TOPIC | OFF-TOPIC | 1941 | OFF-TOPIC | OFF-TOPIC |
| 109 | OFF-TOPIC | OFF-TOPIC | 2021 | OFF-TOPIC | OFF-TOPIC |
| 112 | Journal of Latin American Studies | UNRESOLVED | 0000 | CambridgeUP | [https://www.cambridge.org/core/journals/journal-of-latin-american-studies]() |
| 113 | OFF-TOPIC | OFF-TOPIC | 1940 | OFF-TOPIC | OFF-TOPIC |
| 114 | Legitimate Spheres of Influence? | UNRESOLVED | 2020 | UNRESOLVED | UNRESOLVED |
| 115 | OFF-TOPIC | OFF-TOPIC | 1905 | Brill | OFF-TOPIC |
| 116 | Lines Drawn on an Empty Map: Iraq’s Borders | Ismael | 2015 | Routledge | [https://www.routledge.com/9781138854482]() |
| 117 | Loi portant statut des Juifs | OFF-TOPIC | 1940 | OFF-TOPIC | [https://en.wikipedia.org/wiki/Vichy_anti-Jewish_legislation]() |
| 118 | Men, Women, and Power | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 119 | UNRESOLVED | UNRESOLVED | 2025 | UNRESOLVED | UNRESOLVED |
| 120 | OFF-TOPIC | OFF-TOPIC | 2024 | OFF-TOPIC | OFF-TOPIC |
| 121 | OFF-TOPIC | OFF-TOPIC | 1520 | OFF-TOPIC | OFF-TOPIC |
| 123 | Natural Resource Exploitation in Western Sahara | Allan | 2021 | Routledge | [https://doi.org/10.1080/13629387.2021.1917120]() |
| 124 | Natural Rights Law | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 125 | OFF-TOPIC | OFF-TOPIC | 1946 | OFF-TOPIC | OFF-TOPIC |
| 126 | NWIG (New West Indian Guide) | UNRESOLVED | 2025 | Brill | [https://brill.com/view/journals/nwig/nwig-overview.xml]() |
| 128 | OFF-TOPIC | OFF-TOPIC | 2013 | OFF-TOPIC | OFF-TOPIC |
| 129 | Palaeogeographical Reconstruction | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 130 | PARI Journal | UNRESOLVED | 2019 | OFF-TOPIC | [https://www.mesoweb.com/pari/journal/]() |
| 131 | OFF-TOPIC | OFF-TOPIC | 1999 | OFF-TOPIC | OFF-TOPIC |
| 137 | Report of the Superintendent of Public Instruction | UNRESOLVED | 2025 | Brill | UNRESOLVED |
| 138 | Revista Cubana de Derecho | UNRESOLVED | 1993 | OFF-TOPIC | [https://www.worldcat.org/title/2753066]() |
| 140 | OFF-TOPIC | OFF-TOPIC | 2013 | OFF-TOPIC | OFF-TOPIC |
| 141 | Samenvatting: De Constructie van het Verleden | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 142 | UNRESOLVED | UNRESOLVED | 2025 | UNRESOLVED | UNRESOLVED |
| 143 | Southampton Projects | UNRESOLVED | 1991 | UNRESOLVED | UNRESOLVED |
| 144 | Statisticki Godisnjak (Statistical Yearbook) | OFF-TOPIC | 1939 | OFF-TOPIC | [https://www.worldcat.org/title/8207129]() |
| 145 | Style Manual | OFF-TOPIC | 1978 | OFF-TOPIC | OFF-TOPIC |
| 146 | OFF-TOPIC | OFF-TOPIC | 2014 | OFF-TOPIC | OFF-TOPIC |
| 147 | Teotihuacan and Tenochtitlan | UNRESOLVED | 2019 | UNRESOLVED | UNRESOLVED |
| 149 | UNRESOLVED | UNRESOLVED | 2021 | VersoBooks | UNRESOLVED |
| 154 | Tropical Conservation Science (Journal) | UNRESOLVED | 2009 | SAGEPub | [https://journals.sagepub.com/home/trc]() |
| 155 | UNRESOLVED | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 157 | UNRESOLVED | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 158 | UNRESOLVED | UNRESOLVED | 2021 | UNRESOLVED | UNRESOLVED |
| 159 | UNRESOLVED | UNRESOLVED | 0000 | OxfordUP | UNRESOLVED |
| 160 | UNRESOLVED | UNRESOLVED | 2004 | OxfordUP | UNRESOLVED |
| 161 | UNRESOLVED | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 162 | UNRESOLVED | UNRESOLVED | 2014 | UNRESOLVED | UNRESOLVED |
| 163 | OFF-TOPIC | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 165 | Vojnuci Defter (Primary Source) | UNRESOLVED | 1455 | OFF-TOPIC | UNRESOLVED |
| 166 | Vojnuci Defter 1455 (Edition) | UNRESOLVED | 2020 | UNRESOLVED | UNRESOLVED |
| 167 | UNRESOLVED | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 168 | The Wehrmacht and German Rearmament | Deist | 1981 | OxfordUP | [https://global.oup.com/academic/product/the-wehrmacht-and-german-rearmament-9780198225751]() |
| 169 | Western Sahara as a Settler Colony | UNRESOLVED | 2025 | UNRESOLVED | UNRESOLVED |
| 170 | What We Knew and What We Lost | UNRESOLVED | 2019 | UNRESOLVED | UNRESOLVED |
| 173 | OFF-TOPIC | OFF-TOPIC | 1983 | OFF-TOPIC | OFF-TOPIC |
| 176 | UNRESOLVED | UNRESOLVED | 0000 | UNRESOLVED | UNRESOLVED |
| 180 | Description of the Karabakh Province | Yermolov | 1823 | OFF-TOPIC | [https://www.loc.gov/item/2021666877/]() |
| 181 | Israel: A History | Shapira | 2012 | UNRESOLVED | [https://www.worldcat.org/title/783163617]() |
| 184 | The Case for Israel | Dershowitz | 2003 | WileyBlackwell | [https://www.wiley.com/en-us/The+Case+for+Israel-p-9780471465027]() |
| 188 | UNRESOLVED | UNRESOLVED | 2019 | ChicagoUP | UNRESOLVED |
| 190 | The Islamic Interpretive Tradition and Gender | Duderija | 2017 | Palgrave | [https://doi.org/10.1007/978-3-319-58004-3]() |
| 194 | The Paranoid Apocalypse | Landes | 2012 | NYUPress | [https://nyupress.org/9780814748930/the-paranoid-apocalypse/]() |
| 196 | Arab Historians of the Crusades | Gabrieli | 1969 | Routledge | [https://www.routledge.com/Arab-Historians-of-the-Crusades-Routledge-Revivals/Gabrieli/p/book/9780415577601]() |
| 199 | Treaties and Other International Acts of the USA | Miller | 1931 | OFF-TOPIC | [https://catalog.hathitrust.org/Record/000282126]() |
| 200 | UNRESOLVED | UNRESOLVED | 1797 | UNRESOLVED | UNRESOLVED |
| 201 | UNRESOLVED | UNRESOLVED | 2017 | UNRESOLVED | UNRESOLVED |
| 202 | UNRESOLVED | UNRESOLVED | 2020 | JohnsHopkinsUP | UNRESOLVED |
| 204 | The Armed Struggle and the Search for State | Sayigh | 1997 | OxfordUP | [https://global.oup.com/academic/product/the-armed-struggle-and-the-search-for-state-9780198292654]() |
| 205 | JSTOR India | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 207 | Bakassi (General Reference) | UNRESOLVED | 0000 | OFF-TOPIC | UNRESOLVED |
| 209 | Complete Collection of Treaties (Hertslet's) | Hertslet | 1820 | OFF-TOPIC | [https://catalog.hathitrust.org/Record/000109040]() |
| 210 | Córdoba Agreement | UNRESOLVED | 2006 | OFF-TOPIC | [https://en.wikipedia.org/wiki/Cordoba_Agreement]() |
| 212 | Constitution of Honduras | OFF-TOPIC | 1982 | OFF-TOPIC | [https://www.constituteproject.org/constitution/Honduras_2013]() |
| 213 | OFF-TOPIC | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 214 | OFF-TOPIC | OFF-TOPIC | 0000 | OFF-TOPIC | OFF-TOPIC |
| 216 | Partition of British India | OFF-TOPIC | 1947 | OFF-TOPIC | [https://www.nationalarchives.gov.uk/education/resources/partition-of-india/]() |
| 217 | Partition of the Punjab, 1947: Official Documents | Kirpal Singh | 1991 | UNRESOLVED | [https://www.worldcat.org/title/27237937]() |
| 219 | Report of the Commission of Enquiry, North Borneo | Cobbold | 1962 | OFF-TOPIC | [https://en.wikipedia.org/wiki/Cobbold_Commission]() |
| 220 | Stateless in Bakassi: How a Changed Border Left Inhabitants | UNRESOLVED | 2015 | OFF-TOPIC | [https://www.justiceinitiative.org/publications/stateless-bakassi]() |
| 222 | Indian Independence Act 1947 | UK Parliament | 1947 | OFF-TOPIC | [https://www.legislation.gov.uk/ukpga/1947/30/enacted]() |
| 223 | A Study of War | Wright | 1966 | ChicagoUP | [https://press.uchicago.edu/ucp/books/book/chicago/S/bo3644026.html]() |