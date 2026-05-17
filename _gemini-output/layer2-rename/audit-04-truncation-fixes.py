"""Audit Step 4: Apply manual truncation fixes + year corrections.

Manually-curated map of real truncations to fix. False positives (Vol2, Bj581) excluded.
Also corrects year fields that were misparsed from in-title date ranges.
"""
import json, os

# Map: current_filename -> {new_filename, reason}
TRUNCATION_FIXES = {
    # Spanish Inquisition primary doc
    "InstruccionesDelSantoOficioDeLaInquisiciN-Zafra-1667-Antonio-de-Zafra.pdf": {
        "new": "InstruccionesSantoOficioInquisicion-Zafra-1667-AntonioDeZafra.pdf",
        "reason": "drop trailing 'N' cut from 'Inquisición'",
    },
    # Boucher "Cannibal Encounters" date range cut "149..." was "1492-1763"
    "CannibalEncountersEuropeansAndIslandCaribs149-Boucher-1992-JohnsHopkinsUP.pdf": {
        "new": "CannibalEncountersEuropeansIslandCaribs14921763-Boucher-1992-JohnsHopkinsUP.pdf",
        "reason": "restore full date range 1492-1763 in title",
    },
    # Kinzer "All the Shah's Men" - "Te" was "Terror"
    "AllShahsMenAmericanCoupRootsMiddleEastTe-Kinzer-2013-John-Wiley-&-Sons.pdf": {
        "new": "AllShahsMenAmericanCoupRootsMiddleEastTerror-Kinzer-2013-Wiley.pdf",
        "reason": "restore 'Terror' cut mid-word + normalize publisher slug",
    },
    # Lambert "Barbary Wars" - "W" was "World" (or just "Wars" is fine without it)
    "BarbaryWarsAmericanIndependenceAtlanticW-Lambert-2007-ZLib.epub": {
        "new": "BarbaryWarsAmericanIndependenceAtlanticWorld-Lambert-2007-ZLib.epub",
        "reason": "restore 'World' cut mid-word",
    },
    "BarbaryWarsAmericanIndependenceAtlanticW-Lambert-2007-ZLib.pdf": {
        "new": "BarbaryWarsAmericanIndependenceAtlanticWorld-Lambert-2007-ZLib.pdf",
        "reason": "restore 'World' cut mid-word",
    },
    # Allison "The Crescent Obscured" - year wrong (1776 was period start), title cut
    "CrescentObscuredUnitedStatesMuslimWorld1-Allison-1776-Chicago.pdf": {
        "new": "CrescentObscuredUSMuslimWorld17761815-Allison-1995-ChicagoUP.pdf",
        "reason": "restore date range 1776-1815, correct year (Allison 1995)",
    },
    # Göçek "Denial of Violence" - year wrong (1789 was period), title cut
    # The 'C' at end ambiguous - title is "Denial of Violence: Ottoman Past, Turkish Present, and Collective Violence Against the Armenians, 1789-2009"
    "DenialViolenceOttomanPastTurkishPresentC-Göçek-1789-Oxford.pdf": {
        "new": "DenialViolenceOttomanPastTurkishPresentCollectiveViolence-Gocek-2015-OxfordUP.pdf",
        "reason": "restore 'Collective Violence', correct year (Gocek 2015), normalize publisher",
    },
    # Byrne "Iran-Contra" - "Pr" was "Presidential" or "Presidency"
    "IranContraReagansScandalUncheckedAbusePr-Byrne-2014-TheNewPress.pdf": {
        "new": "IranContraReaganScandalUncheckedAbusePresidentialPower-Byrne-2014-NewPress.pdf",
        "reason": "restore 'Presidential Power' cut mid-word + normalize publisher",
    },
    # Kagan "Modern Iran" - title corrupted by libgen ID string
    "ModernIran10129879780300194739LibgenLi-Kagan-2018-Yale-University-Press.pdf": {
        "new": "ModernIran-Kagan-2018-YaleUP.pdf",
        "reason": "strip libgen ID hash from title + normalize publisher",
    },
    # Doumani "Rediscovering Palestine" - year wrong (1700 was period), title cut
    "RediscoveringPalestineMerchantsPeasantsJ-Doumani-1700-Berkeley.pdf": {
        "new": "RediscoveringPalestineMerchantsPeasantsJabalNablus17001900-Doumani-1995-UCalifUP.pdf",
        "reason": "restore 'Jabal Nablus 1700-1900', correct year (Doumani 1995), normalize publisher",
    },
    # Bayat "Revolution Without Revolutionaries" - "Se" cut from "Sense" or "Sensual"
    # Actual subtitle: "Making Sense of the Arab Spring"
    "RevolutionWithoutRevolutionariesMakingSe-Bayat-2017-Stanford.pdf": {
        "new": "RevolutionWithoutRevolutionariesMakingSenseArabSpring-Bayat-2017-StanfordUP.pdf",
        "reason": "restore 'Sense of the Arab Spring' + normalize publisher",
    },
    # Harris "A Social Revolution" - "I" cut from "Iran"
    # Title: "A Social Revolution: Politics and the Welfare State in Iran"
    "SocialRevolutionPoliticsAndTheWelfareStateInI-Harris-2017-UCPress.pdf": {
        "new": "SocialRevolutionPoliticsWelfareStateIran-Harris-2017-UCalifUP.pdf",
        "reason": "restore 'Iran' cut mid-word + normalize publisher",
    },
    # Akcam "Young Turks' Crime Against Humanity" - "Ge" cut from "Genocide", year wrong (1815 was period)
    # NOTE: this file is also a dupe in the Akcam 2012 cluster, will be stashed; fix anyway for consistency
    "YoungTurksCrimeAgainstHumanityArmenianGe-Akçam-1815-Princeton.pdf": {
        "new": "YoungTurksCrimeAgainstHumanityArmenianGenocide-Akcam-2012-PrincetonUP.pdf",
        "reason": "restore 'Genocide', correct year (Akcam 2012), normalize publisher",
    },
    # Edung "Culturo-Linguistic Factor" - "In" probably cut from "International..." or just trailing
    "CulturoLinguisticFactorAsFacilitatorOfPeaceIn-EDUNG-2015-ResearchAcademyOfSocialScience.pdf": {
        "new": "CulturoLinguisticFactorPeaceInternationalConflict-Edung-2015-ResearchAcadSocialScience.pdf",
        "reason": "restore probable 'International' continuation; normalize author casing",
    },
    # Anyu "ICJ and Border Conflict R..." - "R" cut from "Resolution"
    "InternationalCourtOfJusticeAndBorderConflictR-ANYU-2007-MediterraneanAffairsInc.pdf": {
        "new": "ICJBorderConflictResolution-Anyu-2007-MediterraneanAffairs.pdf",
        "reason": "restore 'Resolution', shorten 'International Court of Justice' to 'ICJ' (canonical), normalize author casing",
    },
    # Doolittle "Powerful Persuasions" - "Sa" cut from "Sabah"
    # Title: "Powerful Persuasions: The Language of Property and Politics in Sabah, Malaysia"
    "PowerfulPersuasionsLanguagePropertyPoliticsSa-Doolittle-2005-Unknown.pdf": {
        "new": "PowerfulPersuasionsLanguagePropertyPoliticsSabahMalaysia-Doolittle-2005-Unknown.pdf",
        "reason": "restore 'Sabah, Malaysia' cut mid-word",
    },
    # FALSE POSITIVES (intentionally NOT in this map):
    #   MedievalPhilosophyNewHistoryWesternPhilosophyVol2  — 'Vol2' is intentional volume marker
    #   VikingWarriorWomenReassessingBirkaGraveBj581       — 'Bj.581' is the famous Birka grave reference
}

with open(r"D:\History vs Hype\_gemini-output\layer2-rename\audit-truncation-fixes-map.json", "w", encoding="utf-8") as f:
    json.dump(TRUNCATION_FIXES, f, indent=2, ensure_ascii=False)

print(f"Truncation fixes: {len(TRUNCATION_FIXES)}")
for old, new in TRUNCATION_FIXES.items():
    print(f"  {old[:55]:55s}")
    print(f"    -> {new['new'][:90]}")
    print(f"    why: {new['reason']}")
print()
print("False positives intentionally excluded: Vol2, Bj581")
