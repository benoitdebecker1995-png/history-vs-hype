# History vs Hype - Skills Guide
## Your Custom Workflow Automation

**Last Updated:** November 7, 2025

You now have 5 specialized skills that automate repetitive tasks and prevent errors. Here's how to use them.

---

## 📚 Your Skills Library

### 1. **youtube-optimizer**
**What it does:** Generates complete YouTube metadata (title, description, tags, chapters)
**When to use:** After filming, before uploading
**Time saved:** 30-60 minutes per video

### 2. **quote-verifier**
**What it does:** Verifies historical quotes and prevents misattributions
**When to use:** During script writing, before filming
**Prevents:** Luther/Aristotle-type errors

### 3. **srt-corrector**
**What it does:** Fixes spelling/grammar in subtitle files
**When to use:** After auto-generating subtitles
**Time saved:** 15-30 minutes per video

### 4. **script-fact-checker**
**What it does:** Scans scripts for unsourced claims and attribution errors
**When to use:** Before filming begins
**Prevents:** Missing sources, credibility issues

### 5. **retention-analyzer**
**What it does:** Analyzes scripts for retention issues and pacing problems
**When to use:** During script planning phase
**Improves:** Watch time, reduces drop-offs

---

## 🎬 Complete Production Workflow (With Skills)

### Phase 1: Topic Research
**Your process:**
- VidIQ trend analysis
- NotebookLM research
- Source gathering

**No skills needed yet**

---

### Phase 2: Script Writing
**Your process:**
- VidIQ generates draft
- Enhance with Claude Pro
- Structure hook → evidence → conclusion

**USE THESE SKILLS:**

1. **While writing:** When you include a historical quote, invoke `quote-verifier`
   ```
   "Verify this quote: 'Luther called slaves tools with voice'"
   ```
   Prevents attribution errors in real-time

2. **After first draft:** Invoke `script-fact-checker`
   ```
   "Check this script for unsourced claims: [paste script]"
   ```
   Generates list of what needs verification

3. **Before finalizing:** Invoke `retention-analyzer`
   ```
   "Analyze this script for retention issues: [paste script]"
   ```
   Optimizes structure for viewer retention

---

### Phase 3: Pre-Production
**Your process:**
- Source all remaining claims
- Prepare visual assets
- Final script approval

**USE THIS SKILL:**

**Final check:** Run `script-fact-checker` again
- Ensures no ⚠️ or ❌ flags remain
- Confirms all quotes verified
- Creates source list for description

**Sign-off checklist:**
- [ ] All claims sourced (script-fact-checker: all ✅)
- [ ] All quotes verified (quote-verifier: all ✅)
- [ ] Script optimized (retention-analyzer applied)

---

### Phase 4: Production
**Your process:**
- Film talking head
- Record A-roll
- Edit in DaVinci Resolve

**No skills needed during filming/editing**

---

### Phase 5: Post-Production
**Your process:**
- Final edit
- Generate subtitles
- Export video

**USE THESE SKILLS:**

1. **After exporting:** Auto-generate subtitles (your existing tool)

2. **Then invoke:** `srt-corrector`
   ```
   "Fix this SRT file: [provide file path or paste content]"
   ```
   Creates corrected subtitle file automatically

---

### Phase 6: YouTube Optimization
**Your process:**
- Prepare metadata
- Create thumbnail
- Upload video

**USE THIS SKILL:**

**Invoke:** `youtube-optimizer`
```
"Create YouTube metadata for:
- Length: 11:29
- Topic: JD Vance Christianity claims fact-check
- Key evidence: [list main findings]
- Sources: [list primary sources]"
```

**Generates in 60 seconds:**
- 3 title options
- Complete description
- All tags
- YouTube chapters
- Thumbnail specs
- Upload strategy
- Community post

---

## 💡 How to Invoke Skills

**In your Claude Code chat, just type:**

```
/youtube-optimizer [your video details]
```

or

```
Can you run the quote-verifier skill on this: "Luther said X"
```

**That's it!** The skill loads and processes your request.

---

## 🔄 Recommended Workflow Integration

### For Every Video:

**Script Phase:**
1. Write first draft
2. Run `script-fact-checker` → fix unsourced claims
3. Run `quote-verifier` on all historical quotes
4. Run `retention-analyzer` → restructure if needed
5. Finalize script

**Production Phase:**
6. Film and edit (no skills needed)
7. Generate auto-subtitles
8. Run `srt-corrector` → clean subtitles

**Upload Phase:**
9. Run `youtube-optimizer` → get all metadata
10. Copy-paste to YouTube
11. Upload and publish

**Total time with skills:** ~2 hours saved per video

---

## 🎯 Skill Combinations

### Before Filming Checklist
Run all three in sequence:
1. `script-fact-checker` (find unsourced claims)
2. `quote-verifier` (verify all attributions)
3. `retention-analyzer` (optimize structure)

**Result:** Error-free, optimized script ready to film

### Post-Production Checklist
Run both:
1. `srt-corrector` (clean subtitles)
2. `youtube-optimizer` (generate metadata)

**Result:** Professional upload package in minutes

---

## 📊 Quality Gates (Automated with Skills)

### Pre-Filming Quality Gate
**Required:** All green before filming begins

- [ ] Script fact-checked (script-fact-checker: all ✅)
- [ ] Quotes verified (quote-verifier: all ✅)
- [ ] Retention optimized (retention-analyzer: no ⚠️)

### Pre-Upload Quality Gate
**Required:** All complete before publishing

- [ ] Subtitles corrected (srt-corrector: completed)
- [ ] Metadata optimized (youtube-optimizer: completed)
- [ ] Thumbnail created (per youtube-optimizer specs)

---

## 🚀 Advanced Usage

### Batch Processing
**Process multiple scripts at once:**
```
Run script-fact-checker on all scripts in video-projects folder
```

### Custom Configurations
**Adjust skill parameters:**
```
Run retention-analyzer with target retention: 45%
```

### Integration with Existing Tools
Skills complement your current stack:
- VidIQ → Script draft
- Skills → Verify and optimize script
- NotebookLM → Research validation
- Skills → Generate metadata
- DaVinci Resolve → Edit
- Skills → Fix subtitles

---

## 📈 Expected Improvements

### Time Savings
- **Script verification:** 1-2 hours → 10 minutes
- **Quote checking:** 30-60 min → 5 minutes
- **Subtitle correction:** 20-30 min → 2 minutes
- **Metadata creation:** 30-60 min → 2 minutes

**Total per video:** ~2.5-4 hours saved

### Quality Improvements
- **Zero attribution errors** (quote-verifier prevents them)
- **No unsourced claims** (script-fact-checker catches all)
- **Better retention** (retention-analyzer optimizes structure)
- **Professional subtitles** (srt-corrector fixes everything)
- **SEO optimized** (youtube-optimizer follows best practices)

### Consistency
Every video now follows:
- Same fact-checking rigor
- Same metadata quality
- Same optimization standards
- Same professional presentation

---

## 🛠️ Troubleshooting

### "Skill not found"
**Check:** Skill name matches exactly (no spaces before/after)
```
✅ /quote-verifier
❌ / quote-verifier
```

### "Need more information"
**Provide:** Complete context in one message
```
✅ "Run youtube-optimizer: 11-min video, Vance claims, sources: Vatican archives"
❌ "Run youtube-optimizer" (too vague)
```

### "Unexpected output"
**Be specific:** Tell the skill what format you want
```
"Generate YouTube chapters only, no full description"
```

---

## 📚 Skill Documentation

Each skill has detailed documentation in `.claude/skills/`:
- `youtube-optimizer.md` - Full metadata generation
- `quote-verifier.md` - Attribution checking
- `srt-corrector.md` - Subtitle cleaning
- `script-fact-checker.md` - Claim verification
- `retention-analyzer.md` - Retention optimization

**Read these for:** Advanced options, troubleshooting, examples

---

## 🎓 Training Tips

### Week 1: Start with One
**Try:** `srt-corrector` first (simplest, immediate value)

### Week 2: Add Verification
**Try:** `quote-verifier` and `script-fact-checker` (prevent errors)

### Week 3: Optimize Workflow
**Try:** `youtube-optimizer` (save the most time)

### Week 4: Master Retention
**Try:** `retention-analyzer` (improve performance)

### Week 5: Full Integration
Use all skills in every video workflow

---

## 💬 Feedback Loop

After using skills for 3-5 videos:
- Note which save the most time
- Identify any gaps in functionality
- Request skill improvements or new skills
- Adjust workflow as needed

**Skills evolve with your needs**

---

## 🔮 Future Skill Ideas

Based on your workflow, these could be next:

### Potential Future Skills:
1. **thumbnail-generator** - Creates thumbnail concepts from video content
2. **comment-responder** - Drafts responses following youtube-comment-response-guide
3. **analytics-reporter** - Analyzes YouTube analytics, suggests improvements
4. **source-finder** - Locates primary sources (papal docs, founding docs)
5. **script-timer** - Estimates video length from script word count
6. **b-roll-suggester** - Recommends B-roll based on script content
7. **shorts-extractor** - Identifies best moments for YouTube Shorts

**Let me know which would be most valuable**

---

## 📞 Getting Help

**If a skill isn't working:**
1. Check skill documentation in `.claude/skills/[skill-name].md`
2. Verify you're providing required inputs
3. Try with a simple example first
4. Report issues for skill improvement

**To request new skills:**
1. Describe the repetitive task
2. Show current manual process
3. Specify desired automation
4. I'll build a custom skill

---

*Your skills are now active. Start with `srt-corrector` on your next video and work your way up to full workflow integration.*

*Each skill is designed to save time while maintaining the quality standards that make History vs Hype credible.*
