# FINAL-SCRIPT-V3 Quality Check

**Date:** 2026-01-01
**Purpose:** Read-aloud test + fact-check against NotebookLM sources

---

## PART 1: SPOKEN DELIVERY ISSUES

### Numbers - Convert to Spoken Format

**Current issues in script:**

| Line | Written | Should Say When Speaking |
|------|---------|-------------------------|
| 73 | "240 BC" | "two hundred forty BC" |
| 75 | "7.2 degrees" | "seven point two degrees" ✅ (already correct) |
| 81 | "5,000 stadia" | "five thousand stadia" |
| 83 | "250,000 stadia" | "two hundred fifty thousand stadia" |
| 83 | "29,000 miles" | "twenty-nine thousand miles" |
| 85 | "24,860 miles" | "twenty-four thousand eight hundred sixty miles" |
| 87 | "15 percent" | "fifteen percent" |
| 139 | "750,000 students" | "seven hundred fifty thousand students" |
| 139 | "1350 and 1500" | "thirteen fifty and fifteen hundred" |

**Action:** Numbers are written correctly for readability but will sound natural when spoken. No changes needed to script.

### Contractions - Check Usage

**Audit results:** ✅ Script uses contractions appropriately throughout
- "didn't" (line 71)
- "wasn't" (line 89)
- "weren't" (line 115)
- "wasn't" (line 158)
- "can't" (multiple instances)

### Sentence Length - Check for Breath Control

**Potential issues:**

**Line 73-74:**
> "In 240 BC, Eratosthenes of Cyrene used sticks and shadows to calculate the earth's circumference. At noon on the summer solstice in Syene—modern Aswan—a vertical stick cast no shadow."

✅ **GOOD** - Two sentences, natural pause point

**Line 79-81:**
> "If the sun's rays are parallel, the only reason for different shadow angles is the curvature of the earth's surface. Seven point two degrees is one-fiftieth of a circle. So the distance between the two cities—about 5,000 stadia—is one-fiftieth of the earth's circumference."

✅ **GOOD** - Three short sentences with clear logic flow

**Line 137-139:**
> "Between 1350 and 1500 alone, about 750,000 students went through European universities. All of them studied Sacrobosco."

✅ **GOOD** - Short declarative for emphasis (user's Pattern 4)

### Quote Attributions - Sound Natural?

**Line 103-105 (Isidore quote):**
> Isidore defines day and night in Book III, Chapter 51. Here's the quote:
> "Day is the sun over the earth, and night is the sun under the earth."

✅ **GOOD** - Attribution before quote, conversational setup

**Line 144-146 (Sacrobosco quote):**
> Sacrobosco writes:
> "When a ship approaches land, a signal on shore is visible from the masthead..."

✅ **GOOD** - Simple attribution

**Line 258 (Irving quote):**
> Historian Samuel Eliot Morison later called Irving's account "pure moonshine."

✅ **GOOD** - Embedded in sentence naturally

### Date Formats

**Line 95:**
> "Jump to the year 630."

✅ **GOOD** - Spoken naturally

**Line 127:**
> "Now jump to 1230."

✅ **GOOD** - "twelve thirty" when spoken

### Embedded Definitions (User's Pattern 1)

**Line 39:**
> "Johannes de Sacrobosco's *Sphere*—the standard university astronomy textbook from 1230, used for four hundred years, surviving in hundreds of manuscripts."

✅ **GOOD** - Dash-separated clarification (Pattern 5)

**Line 162:**
> "This is the *globus cruciger*—the royal orb. A golden sphere surmounted by a cross."

✅ **GOOD** - Latin term → English translation → concrete description

---

## PART 2: FACT-CHECK AGAINST NOTEBOOKLM SOURCES

### ACT 1 - Opening Claims

| Claim | Script Line | NotebookLM Source | Status |
|-------|-------------|-------------------|--------|
| Textbook shift 1850→1890 | 19-29 | Need to verify with Russell's textbook survey | ⏳ PENDING |
| Bede 725 AD | 37 | "AD 725" confirmed (Bede: Reckoning of Time) | ✅ VERIFIED |
| Sacrobosco 1230 | 39 | "c. 1230" confirmed (Tractatus de sphaera) | ✅ VERIFIED |
| Sacrobosco "400 years" | 39 | "standard university textbook for four centuries" confirmed | ✅ VERIFIED |
| Irving 1828 | 49 | Need to verify exact date | ⏳ PENDING |
| Draper 1874 | 51 | Need to verify exact date | ⏳ PENDING |
| White 1896 | 53 | Need to verify exact date | ⏳ PENDING |

### ACT 2 - Medieval Evidence

| Claim | Script Line | NotebookLM Source | Status |
|-------|-------------|-------------------|--------|
| Eratosthenes 240 BC | 73 | "c. 240 BC" - need exact citation | ⏳ PENDING |
| 7.2 degrees | 75 | Need to verify | ⏳ PENDING |
| 5,000 stadia distance | 81 | Need to verify | ⏳ PENDING |
| 250,000 stadia circumference | 83 | Need to verify | ⏳ PENDING |
| 29,000 miles | 83 | "Roughly 29,000 miles" - verify | ⏳ PENDING |
| Actual 24,860 miles | 85 | Should be 24,901 miles (check this!) | ❌ POTENTIAL ERROR |
| Within 15% | 87 | Verify calculation | ⏳ PENDING |
| **Isidore quote** | 107 | "Day is sun over earth, night is sun under earth" | ✅ NEED EXACT QUOTE |
| Isidore date 630 | 95 | "c. 630" confirmed (Etymologies) | ✅ VERIFIED |
| **Sacrobosco ship quote** | 144-146 | "bulge of the water" - exact quote needed | ⏳ NEED EXACT QUOTE |
| 750,000 students 1350-1500 | 139 | "approximately 750,000 students" confirmed (NOTEBOOKLM p.33) | ✅ VERIFIED |
| 80 editions | 135 | "went through eighty different editions" - verify | ⏳ PENDING |
| Globus cruciger 11th century | 162 | "11th-century Holy Roman Emperors" confirmed (NOTEBOOKLM p.15) | ✅ VERIFIED |
| **Isidore on globus** | 167-168 | Need exact quote from Etymologies XVIII.iii.4 | ⏳ NEED EXACT QUOTE |
| Lactantius 4th century | 179 | Confirmed as marginal figure | ✅ VERIFIED |
| Cosmas 6th century | 179 | "Cosmas Indicopleustes" 6th century confirmed | ✅ VERIFIED |
| "No followers whatsoever" | 181 | Jeffrey Burton Russell quote - need exact citation | ⏳ NEED SOURCE |

### ACT 3 - Columbus

| Claim | Script Line | NotebookLM Source | Status |
|-------|-------------|-------------------|--------|
| Columbus 21,000 miles estimate | 196 | Need to verify | ⏳ PENDING |
| Actual 24,901 miles | 197 | This is correct | ✅ VERIFIED |
| 4,000 mile error | 198 | Verify calculation: 24,901 - 21,000 = 3,901 ≈ 4,000 | ✅ VERIFIED |
| Alfraganus 56⅔ miles | 200 | Need to verify | ⏳ PENDING |
| Roman mile 4,856 feet | 202 | Need to verify | ⏳ PENDING |
| Arabic mile 7,091 feet | 202 | Need to verify | ⏳ PENDING |
| 25% difference | 203 | Verify: 7,091/4,856 = 1.46 (46% larger, not 25%) | ❌ POTENTIAL ERROR |
| Spain to Japan 2,500 miles (Columbus) | 208 | Need to verify | ⏳ PENDING |
| Spain to Japan 12,500 miles (actual) | 208 | Need to verify | ⏳ PENDING |
| Hernando de Talavera | 214 | "headed by Hernando de Talavera" confirmed | ✅ VERIFIED |
| Abraham Zacuto | 215 | "Rabbi Abraham Zacuto" confirmed | ✅ VERIFIED |
| Irving fabricated scene | 229-232 | Confirmed from audio 3 | ✅ VERIFIED |
| Morison "pure moonshine" | 258 | Need exact citation from Morison | ⏳ NEED SOURCE |

### ACT 4 - Perpetrators

| Claim | Script Line | NotebookLM Source | Status |
|-------|-------------|-------------------|--------|
| Irving 1828 book | 239-241 | *History of Life and Voyages of Christopher Columbus* (1828) | ⏳ VERIFY DATE |
| 10,000 copies sold | 250 | Need to verify | ⏳ PENDING |
| Draper 1874 | 261-263 | *History of the Conflict Between Religion and Science* (1874) | ⏳ VERIFY DATE |
| Papal Infallibility 1870 | 269 | Historical fact | ✅ VERIFIED |
| 4 years after (1874-1870=4) | 269 | Correct | ✅ VERIFIED |
| "Over fifty printings" | 274 | Audio 3 said "went through dozens of editions" - verify exact number | ⚠️ CHECK |
| White 1896 | 281 | *History of the Warfare of Science with Theology* (1896) | ⏳ VERIFY DATE |
| "Two-volume work" | 283 | Verify | ⏳ PENDING |
| Darwin 1859 | 350 | *Origin of Species* (1859) | ✅ VERIFIED |

### ACT 5 - Educational Lag

| Claim | Script Line | NotebookLM Source | Status |
|-------|-------------|-------------------|--------|
| Russell textbook survey | 303-304 | "Jeffrey Burton Russell surveyed..." | ⏳ NEED SOURCE |
| Before 1870 vs After 1880 | 305-308 | Verify from Russell's *Inventing the Flat Earth* | ⏳ PENDING |
| Russell 1991 | 320 | *Inventing the Flat Earth* (1991) | ⏳ VERIFY DATE |
| 30 years (1991-2026=35) | 320 | Should be "over 30 years" or "35 years" | ⚠️ MINOR |
| Church never took official position | 330 | Counter-fact from audio 3 | ⏳ VERIFY |

### ACT 6 - Modern Consequences

| Claim | Script Line | NotebookLM Source | Status |
|-------|-------------|-------------------|--------|
| Trust in science dropped 15% (2020-2023) | 347 | Need source | ⏳ PENDING |
| 27% low confidence | 347 | Need source | ⏳ PENDING |
| Gateway effect | 350 | "Research shows a 'gateway effect'" - need citation | ⏳ PENDING |

---

## CRITICAL ISSUES TO RESOLVE

### ❌ ERRORS FOUND:

1. **Line 85: Earth's circumference**
   - Script says: "24,860 miles"
   - Should be: "24,901 miles" (this is mentioned correctly in line 197)
   - **ACTION:** Change line 85 to 24,901 miles OR explain this is rounding

2. **Line 203: Gallon analogy percentage**
   - Script says: "off by 25 percent"
   - Calculation: 7,091 ÷ 4,856 = 1.46 (46% larger)
   - **ACTION:** Either fix the percentage OR remove the percentage claim

3. **Line 274: "Over fifty printings"**
   - Audio 3 said "dozens of editions"
   - Need to verify exact number from sources
   - **ACTION:** Check NotebookLM for exact figure

### ⏳ QUOTES NEED EXACT VERIFICATION:

1. **Isidore quote (line 107):** "Day is the sun over the earth, and night is the sun under the earth."
   - Need exact Latin + English from Etymologies III.51
   - Need page number citation

2. **Isidore on globus (lines 167-168):** "Augustus established the orb..."
   - Need exact quote from Etymologies XVIII.iii.4
   - NotebookLM has it: "Augustus is said to have established the orb (pila) as a standard... so that he might the more display the figure of the globe (orbis)"
   - **ACTION:** Use exact quote with page number

3. **Sacrobosco ship quote (lines 144-146):**
   - NotebookLM has exact: "When a ship approaches land, a signal on shore is visible from the masthead but invisible from the foot of the mast because of the 'bulge of the water'"
   - Need page number

4. **Russell "no followers whatsoever" (line 181):**
   - Need exact citation from *Inventing the Flat Earth*
   - **ACTION:** Find page number

5. **Morison "pure moonshine" (line 258):**
   - Need exact citation from *Admiral of the Ocean Sea*
   - **ACTION:** Find page number

### ⏳ DATES/NUMBERS NEED VERIFICATION:

- Eratosthenes exact calculation (lines 73-87)
- Irving 1828 exact date
- Draper 1874 exact date
- White 1896 exact date
- Russell textbook survey findings
- Trust in science statistics (lines 347-348)

---

## NEXT ACTIONS

### IMMEDIATE (Before Filming):

1. **Fix error on line 85:** Change 24,860 to 24,901 miles
2. **Fix or remove percentage on line 203:** Gallon analogy
3. **Get exact quotes with page numbers:**
   - Isidore "sun under earth"
   - Isidore on globus
   - Sacrobosco ship/mast
   - Russell "no followers"
   - Morison "moonshine"

### READ NOTEBOOKLM FILES TO VERIFY:

- `NOTEBOOKLM-RESEARCH-COMPILATION.md` (already started)
- `NOTEBOOKLM-ADDITIONAL-RESEARCH.md`
- `03-COLUMBUS-CALCULATION-ERROR.md`
- `01-VERIFIED-RESEARCH.md`

### AFTER VERIFICATION:

- Update FINAL-SCRIPT-V3.md with corrections
- Add page numbers to all quotes
- Mark script as **READY FOR FILMING**

---

## SPOKEN DELIVERY TEST: OVERALL ASSESSMENT

✅ **STRENGTHS:**
- Uses contractions appropriately
- Numbers written in readable format (will sound natural when spoken)
- Sentence lengths manageable
- Quote attributions conversational
- Embedded definitions follow user's patterns
- Dash-separated clarifications used well

⚠️ **MINOR ADJUSTMENTS:**
- None needed for spoken delivery
- Script sounds natural when read aloud
- Pattern interrupts clearly marked

---

## FACT-CHECK TEST: OVERALL ASSESSMENT

⚠️ **NEEDS WORK:**
- 2 factual errors identified (circumference figure, percentage)
- 5 quotes need exact wording + page numbers
- 15+ claims need source verification
- Dates need confirmation

**ESTIMATED TIME TO COMPLETE VERIFICATION:** 2-3 hours

**RECOMMENDATION:**
1. Fix the 2 errors immediately
2. Read all NotebookLM files to get exact quotes and page numbers
3. Update script with corrections
4. Then mark as filming-ready

---

**STATUS:** Script structure is excellent. Spoken delivery is natural. Fact-checking in progress.
