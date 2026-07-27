# Source Acquisition Queue — #55 Falklands/Malvinas

**Purpose:** Track primary/secondary-source acquisitions that would upgrade candidate quotes to verified, primary-anchored quotes.
**Generated from:** `primary-source-hunter` trace of the Jennings "strong presumption against the validity" dictum, 2026-07-27.
**Status legend:** TARGETED / ATTEMPTING / ACQUIRED / UNAVAILABLE / DEFERRED

## Queue Summary
- Total acquisitions targeted: 2
- Priority 1 (blocks on-screen primary for the Jennings/arbitration beat): 2

---

## Acquisitions

### Jennings, R. Y. *The Acquisition of Territory in International Law* (Manchester University Press, 1963)
- **Upgrades claim:** The dictum "there must be a strong presumption against the validity of such an alleged title where the claimant is not willing to have that claim properly determined in a Court of Law" — currently held at Gustafson 1988 p.33, third-hand (Jennings → Moore's AJIL letter → Gustafson). This is the most-primary possible source (Jennings's own monograph).
- **Current tier:** T3 (Gustafson's paraphrase-quote, uncorroborated at the primary)
- **Target tier:** T1 (direct from Jennings's own book, if the exact page can be located)
- **Source type:** Academic monograph (standard treatise, Melland Schill Lectures)
- **Access path checked (all FREE-only, none succeeded):**
  - archive.org item `acquisitionofter0000robe` — exists but `access-restricted-item:true` (Controlled Digital Lending); direct text download returns HTTP 401; the item's own "search inside" endpoint errors with "Item not available due to issues with the item's content." A personal archive.org account + 1-hour borrow loan MIGHT work but was not attempted (no login in this session) — free and legitimate if the user wants to try it manually.
  - HathiTrust — no catalog record found for this ISBN (9780719002274); not digitized there.
  - Google Books (`id=NhfpAAAAIAAJ`) — no preview/snippet available for search terms.
  - Google Books API — quota exhausted (HTTP 429) on this account/project.
  - manchesterhive.com (2021 reissue, Kohen intro) — chapter page 403 Forbidden (gated).
  - EJIL review "That Little Book" (Storr, 2023, open access, fully read) — does NOT quote or discuss this passage.
  - Malaya Law Review 1963 review PDF (law.nus.edu.sg) — blocked by bot-protection (Incapsula), not retrievable via automated tools.
- **Estimated effort:** Low-medium — library ILL, or a personal archive.org borrow (free), or the reissued paperback (~£20-30, Manchester UP / Amazon, ISBN 9781526117175)
- **Priority:** 1 — this is the bedrock primary for the arbitration/adjudication beat, and Jennings later became ICJ President, so his own wording carries real on-screen weight
- **Status:** UNAVAILABLE via free web access — needs manual library/ILL/borrow action
- **Notes:** Two other scholars in this project's exhibit set (Beck 1988 fn.62, Dolzer 1993 fn.379) independently cite Jennings pp.6/20-23/22 for an ADJACENT but not proven-identical doctrine (a title-holder's need to offer judicial settlement to defeat prescription) — this is the best lead for WHERE in the book to look once access is obtained, but is NOT confirmed to be the same sentence Gustafson quotes. Once obtained, raw-read pp.6, 20-23 first.

---

### Moore, John Norton. "Correspondence." *American Journal of International Law* 77, no. 3 (July 1983), pp. 610–615.
- **Upgrades claim:** Same dictum as above. This is the INTERMEDIATE rung — the letter Gustafson actually quoted from (per his footnote 101), which itself quotes Jennings and presumably cites a specific page of the 1963 book.
- **Current tier:** T3 (unread; Gustafson's citation to it is the only trace)
- **Target tier:** T2 (a scholar's letter quoting Jennings verbatim with a page cite) — reading it would likely hand us the exact Jennings page number even if the 1963 book itself remains unobtained.
- **Source type:** Journal correspondence/letter-to-editors (not a peer-reviewed article)
- **Access path checked:**
  - Confirmed via Crossref: DOI `10.1017/S0002930000763081`, pp.610-615, AJIL vol.77 no.3 (July 1983) — matches Gustafson's "p.612" exactly.
  - Unpaywall lookup on this DOI: `is_oa: false`, no OA locations anywhere. Fully closed (Cambridge Core / JSTOR only).
- **Estimated effort:** Low — single letter, ~6pp; library JSTOR/HeinOnline access or ILL photocopy request
- **Estimated cost:** Free via any university library login; otherwise a few dollars via document-delivery/ILL
- **Priority:** 1 — fastest path to the exact Jennings page number; read this FIRST if only one acquisition is pursued
- **Status:** UNAVAILABLE via free web access — gated, no OA copy exists
- **Notes:** Gustafson's own citation to this letter has a typo (AJIL "vol. 11" should be vol. 77) — worth independently confirming pp.610-615 is the right item once accessed, since Crossref's metadata for this DOI carries no title ("[no title]" = correspondence/departmental item, consistent with a letters section).

---

## Post-Acquisition Protocol

1. Acquire (ILL / library login / archive.org borrow / purchase) — Moore's AJIL letter first, since it's shorter and will likely hand us the exact Jennings page number.
2. Raw-read Moore's letter for: (a) the exact verbatim Jennings quote as Moore renders it, (b) the page of Jennings 1963 it cites, (c) whether Moore frames the quote as general doctrine or Falklands-specific.
3. Acquire Jennings 1963 (or the relevant page range) and raw-read the passage in context (a paragraph before/after) to answer the DECISIVE QUESTION: general doctrine vs. context-specific.
4. Render/photograph the exact page if acquired as a physical book or scan.
5. Update `_research/agent-outputs/jennings-dictum-trace.md` with the confirmed verbatim + page + scope finding.
6. Upsert the finding into `_research/SOURCE-GENEALOGY.md`.
7. If verified, move Gustafson's quote from "candidate/T3" to a verified T1/T2 quote in `01-VERIFIED-RESEARCH.md`, correcting Gustafson's broken AJIL volume citation in the process.

**Gate:** This beat should not go on screen as "Jennings wrote..." with a verbatim quote until at least the Moore AJIL letter (Priority 1, faster) has been raw-read to confirm Gustafson's rendering is accurate.
