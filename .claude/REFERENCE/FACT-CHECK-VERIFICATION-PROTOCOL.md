# FACT-CHECK VERIFICATION PROTOCOL

**Purpose:** Prevent factual errors in scripts before filming
**Created:** 2025-01-27 (after Nicaragua v Colombia error)
**Status:** MANDATORY for all legal/historical claims

---

## 🚨 THE PROBLEM

**What happened:**
- Script claimed ICJ "ruled the treaty was valid" in Nicaragua v Colombia
- ICJ actually ruled it had "no jurisdiction" - completely different
- Material breach quote attributed to wrong case
- Error discovered AFTER filming 11 minutes of A-roll

**Root cause:**
- Claude worked from general knowledge, not primary sources
- No verification step before filming
- User trusted AI output without checking

**Impact:**
- Wasted filming time
- Required re-filming/editing fixes
- Risk to channel credibility if published

---

## ✅ MANDATORY VERIFICATION PROTOCOL

### **RULE 1: Never Film Legal Claims Without Primary Source Verification**

**Applies to:**
- Court rulings (ICJ, Supreme Court, any legal decision)
- Treaty provisions (specific articles, clauses)
- Legal definitions (material breach, estoppel, jurisdictional standards)
- Case precedents (what court actually decided vs what parties claimed)
- Historical documents (what they actually say vs common interpretations)

**Before filming:**
1. Upload primary sources to NotebookLM
2. Run verification prompts (see templates below)
3. Compare script claims to verified facts
4. Correct ANY discrepancies before filming

---

### **RULE 2: Flag Claude's Unverified Claims**

**When Claude writes a script with legal/historical claims, ALWAYS ask:**

| Claude's Claim | Verification Question |
|----------------|----------------------|
| "The ICJ ruled X..." | Which paragraph of the ruling? What's the exact quote? |
| "The court said..." | What page? What's the operative clause? |
| "The treaty required X..." | Which article? What's the exact language? |
| "This is defined as..." | Source? Convention? Case law? |
| "The precedent shows..." | Which case? What was the actual holding? |

**If Claude can't cite page numbers and paragraphs:** The claim is unverified. Check it yourself.

---

### **RULE 3: Use NotebookLM for Legal Verification**

**Why NotebookLM:**
- Grounds answers in uploaded sources only
- Provides page numbers and quotes
- Can't hallucinate or work from general knowledge
- Forces you to have the actual documents

**Required sources:**
- Full court rulings (PDF), not summaries
- Complete treaty texts, not excerpts
- Primary documents, not secondary analysis

---

## 📋 VERIFICATION PROMPT TEMPLATES

### **Template 1: Court Ruling Verification**

```
I need to verify what the [Court Name] actually ruled in [Case Name] ([Year]).

From the sources provided, answer these questions with exact quotes and page numbers:

1. WHAT DID THE COURT DECIDE?
   - What was the operative decision (the actual ruling)?
   - Did the court rule on [specific issue] or decline to rule?
   - What's the exact language of the decision?

2. WHAT DID THE COURT SAY ABOUT [SPECIFIC CLAIM]?
   - Quote the relevant passages with page numbers
   - Did the court affirm, reject, or not address this?

3. WHAT LANGUAGE DID THE COURT USE?
   - Quote key phrases (e.g., "material breach," "no jurisdiction," "violate")
   - Context for each quote?

4. WHAT DID THE COURT NOT DECIDE?
   - What questions did the court explicitly avoid?
   - What issues were outside its jurisdiction?

5. HOW SHOULD THIS BE CHARACTERIZED?
   Is it accurate to say: "[Your script's claim]"

   YES / NO / PARTIALLY - explain with quotes
```

---

### **Template 2: Treaty/Document Verification**

```
I need to verify what [Treaty/Document Name] actually says about [specific topic].

From the sources provided:

1. EXACT TEXT
   - Quote Article [X] in full
   - What's the exact language?

2. WHAT IT REQUIRES/PROHIBITS
   - What obligations does it create?
   - What's mandatory vs aspirational?

3. WHAT IT DOESN'T SAY
   - Does it address [topic]?
   - What's NOT covered?

4. SCRIPT ACCURACY CHECK
   My script says: "[claim]"

   Is this accurate based on the treaty text? Quote supporting passages.
```

---

### **Template 3: Legal Definition Verification**

```
I need to verify the definition of [legal term] as used in [context].

From the sources:

1. OFFICIAL DEFINITION
   - Where is it defined? (Convention, case law, statute)
   - Quote the definition with citation

2. HOW IT'S APPLIED
   - How did [Court/Treaty] apply this term?
   - Quote examples of its use

3. COMMON MISUNDERSTANDINGS
   - What does it NOT mean?
   - What's the difference between [term] and [similar term]?

4. SCRIPT CHECK
   My script says: "[definition/application]"

   Accurate? Cite supporting sources.
```

---

### **Template 4: Case Precedent Verification**

```
I'm using [Case Name] as a precedent for [Your Argument].

Verify this parallel:

1. WHAT ACTUALLY HAPPENED IN THE CASE?
   - Facts
   - What parties claimed
   - What court decided

2. WHAT'S THE PRECEDENT?
   - What legal principle did it establish?
   - Quote the key holding

3. DOES IT SUPPORT MY ARGUMENT?
   My argument: "[Your claim about what the case shows]"

   Accurate parallel? YES / NO / PARTIALLY

   Quote supporting or contradicting passages.

4. WHAT ARE THE LIMITS?
   - What makes this case different from [your situation]?
   - What did the court specifically NOT decide?
```

---

## 🎯 WORKFLOW INTEGRATION

### **Phase 1: Script Drafting (Claude)**
- Claude writes initial script
- Flags sources needed for verification
- Notes: "VERIFY BEFORE FILMING: [list of claims]"

### **Phase 2: NotebookLM Verification (You)**
1. Gather primary sources (court PDFs, treaty texts)
2. Upload to NotebookLM
3. Run verification prompts for each flagged claim
4. Document findings in FACT-CHECK-VERIFICATION.md

### **Phase 3: Script Correction (Claude)**
- Compare NotebookLM findings to script
- Correct any inaccuracies
- Update with exact quotes/page numbers
- Mark as "VERIFIED - READY FOR FILMING"

### **Phase 4: Filming**
- Only film scripts marked "VERIFIED"
- Keep verification notes for YouTube description sources

---

## 📝 FACT-CHECK-VERIFICATION.md TEMPLATE

For each video, create this file:

```markdown
# FACT-CHECK VERIFICATION - [Video Title]

## Claims Requiring Verification

### Claim 1: [Script statement]
**Source Needed:** [Court ruling / Treaty / Document]
**NotebookLM Finding:** [Quote with page number]
**Status:** ✅ VERIFIED / ❌ INCORRECT / 🔄 CORRECTED
**Correction:** [If needed]

### Claim 2: [Next statement]
[Repeat...]

## Sources Uploaded to NotebookLM
1. [Document name - URL or file]
2. [Document name - URL or file]

## Verification Complete
- [ ] All legal claims verified with primary sources
- [ ] All quotes accurate with page numbers
- [ ] All case precedents correctly characterized
- [ ] Script corrected where needed
- [ ] READY FOR FILMING
```

---

## ⚠️ RED FLAGS (Stop and Verify)

**If you see these in a Claude-written script, VERIFY IMMEDIATELY:**

| Red Flag | Why It's Risky | Verification Needed |
|----------|---------------|---------------------|
| "The court ruled X..." | Courts use specific language - verify exact wording | Court ruling PDF, operative clause |
| "Material breach" | Specific legal definition (VCLT Article 60) | Vienna Convention, case applying it |
| "The treaty says..." | Need exact article text | Full treaty PDF |
| "Precedent shows..." | Need actual holding, not interpretation | Case ruling, operative decision |
| "Defined as..." | Legal definitions have specific sources | Convention/statute/case law |
| Quote without citation | Could be paraphrased or misattributed | Primary source with page number |
| "The court said it couldn't..." vs "The court said it was valid" | Huge difference - verify which | Exact court language |

---

## 🔥 EMERGENCY CHECKLIST (If Error Found After Filming)

- [ ] **How bad is it?** Minor nuance vs fundamental mischaracterization?
- [ ] **Can we fix in editing?** Cut section / voiceover / text correction
- [ ] **Do we need to re-film?** If fundamental error, yes
- [ ] **Update protocol:** What verification step would have caught this?
- [ ] **Document lesson:** Add to this protocol as new red flag

---

## 📚 REQUIRED READING BEFORE EACH SCRIPT

Before filming any video with legal/historical claims:

1. Read this protocol
2. Identify claims requiring verification
3. Gather primary sources
4. Run NotebookLM verification
5. Correct script
6. Document verification
7. THEN film

**Time investment:** 30-60 minutes
**Value:** Prevents hours of re-filming and protects channel credibility

---

## 🎓 LESSONS LEARNED

### **Nicaragua v Colombia Error (2025-01-27)**

**What we said:** "The ICJ ruled the treaty was valid, but Colombia had violated Nicaragua's maritime rights anyway."

**What actually happened:**
- ICJ ruled "no jurisdiction" to revisit treaty (didn't rule it "valid" or "invalid")
- ICJ rejected Nicaragua's breach claim (didn't find Colombia violated rights)
- ICJ delimited new maritime boundary (treaty didn't establish one)

**Why it happened:**
- Claude worked from general knowledge of ICJ cases
- No verification step with actual ruling
- Assumed "treaty stood" = "court ruled it valid" (wrong)

**What would have prevented it:**
- Upload Nicaragua v Colombia 2012 ruling to NotebookLM
- Ask: "Did ICJ rule treaty valid or decline to rule on validity?"
- Compare answer to script claim
- Correct before filming

**Fix:**
- Cut Nicaragua section entirely (weakest precedent anyway)
- Film 10-second pickup line
- Shorter, stronger video

---

## 🛡️ CHANNEL REPUTATION PROTECTION

**Your channel's brand promise:** Evidence-based analysis with academic rigor

**This protocol protects:**
- Factual accuracy (your core value)
- Viewer trust (they rely on you to get details right)
- Channel growth (credibility drives subscriptions)
- Legal topics authority (you cite actual rulings, not summaries)

**Cost of violation:**
- Misinformation in published video
- Comments pointing out errors
- Damaged credibility
- Lost viewer trust

**Cost of compliance:**
- 30-60 min verification per video
- Worth it EVERY TIME

---

## ✅ SIGN-OFF CHECKLIST

Before marking any script "READY FOR FILMING":

- [ ] All court rulings verified with NotebookLM
- [ ] All treaty provisions verified with full text
- [ ] All legal definitions verified with authoritative sources
- [ ] All case precedents correctly characterized
- [ ] All quotes accurate with page numbers
- [ ] FACT-CHECK-VERIFICATION.md completed
- [ ] Claude has reviewed and corrected any errors
- [ ] User has spot-checked key claims

**Only then:** Mark script VERIFIED and film

---

**REMEMBER: 30 minutes of fact-checking prevents hours of re-filming.**

**Your audience trusts you to get it right. Honor that trust.**
