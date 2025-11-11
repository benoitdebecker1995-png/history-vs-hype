# Voice Check Command

Analyze whether a script matches the creator's natural speaking voice from VOICE-GUIDE.md.

## Your Task

Read VOICE-GUIDE.md and analyze the script provided for voice authenticity.

## Analysis Checklist

### 1. Natural Fillers
Does the script use:
- [ ] "I think"
- [ ] "you know"
- [ ] "like"
- [ ] "kind of" / "sort of"
- [ ] "I mean"
- [ ] "basically"
- [ ] "right?"

**If missing:** Flag sections that sound too polished/formal.

### 2. Signature Phrases
Does the script use:
- [ ] "The biggest deal is..."
- [ ] "I think both of these are wrong"
- [ ] "Which, yeah, I think puts things into perspective"
- [ ] "I'm not super familiar with it, to be honest" (if appropriate)

**If missing:** Note where they should appear.

### 3. Formal Language (AVOID)
Does the script contain:
- [ ] "Furthermore," "Moreover," "Consequently"
- [ ] "In conclusion"
- [ ] "It is evident that"
- [ ] Perfect thesis statements

**If found:** Flag each occurrence with line number.

### 4. Argument Building
- [ ] Does it build incrementally? (not thesis-first)
- [ ] Does it include self-correction? ("well, not exactly, but...")
- [ ] Does it admit uncertainty where appropriate?

### 5. Source Citations
Are sources cited conversationally?
- ✅ "Samuel Moyn has this really good book called..."
- ❌ "According to historian Samuel Moyn (2015)..."

### 6. Both Extremes Pattern
- [ ] Does opening frame BOTH extreme narratives?
- [ ] Does ending return to both extremes?
- [ ] Does it explicitly say "both are wrong"?

---

## Output Format

### VOICE AUTHENTICITY SCORE: [X/10]

**Natural Fillers:** [Present/Sparse/Missing]
- Issues: [List any sections without fillers]

**Signature Phrases:** [Present/Partial/Missing]
- Issues: [List missing phrases]

**Formal Language:** [None/Some/Excessive]
- Problems found: [List with line numbers]

**Argument Structure:** [Incremental/Thesis-first/Mixed]
- Issues: [Describe problems]

**Both Extremes Pattern:** [Complete/Partial/Missing]
- Issues: [What's missing]

---

### SPECIFIC PROBLEMS FOUND

**Line [X]:**
> "[Quote from script]"

**Problem:** [Too formal / Missing fillers / Perfect thesis / etc.]

**Sounds like:** AI-generated / Documentary narration / Academic paper

**Creator would say:**
> "[Rewrite in natural voice]"

---

**Line [X]:**
> "[Quote from script]"

**Problem:** [Describe issue]

**Creator would say:**
> "[Rewrite]"

---

### SECTIONS THAT SOUND UNNATURAL

**[Timestamp or section name]:**
- Current: "[Quote]"
- Problem: [Why it doesn't match voice]
- Fix: "[Natural version]"

---

### OVERALL ASSESSMENT

This script sounds:
- [ ] Like the creator's natural voice ✅
- [ ] Partially authentic (needs work) ⚠️
- [ ] Formal/AI-generated (major revision needed) ❌

**Key issues:**
1. [Most important voice issue]
2. [Second issue]
3. [Third issue]

**Quick wins:**
- Add natural fillers in [sections]
- Replace formal language in [lines]
- Include "both extremes" framing in [section]

---

## Script to Analyze

$ARGUMENTS
