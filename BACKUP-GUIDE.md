# Backup & Disaster Recovery Guide - History vs Hype

**Purpose:** Protect your valuable content, research, and production work

**Your repository contains:**
- 275+ files
- 169 subscribers worth of channel work
- Months of research and script development
- Irreplaceable academic source compilation

**NEVER lose this work. Follow this guide.**

---

## 🚨 CRITICAL IMPORTANCE

### What You Could Lose:
- ❌ **Scripts:** Weeks of research and writing
- ❌ **Research:** Hundreds of hours of source verification
- ❌ **Channel data:** Analytics and performance insights
- ❌ **Raw footage:** Can't recreate filmed content
- ❌ **Project files:** DaVinci Resolve timelines
- ❌ **Intellectual property:** Your unique analysis and arguments

### Cost of Data Loss:
- **Time:** Months to recreate
- **Money:** Lost revenue during recovery
- **Reputation:** Delayed uploads = subscriber loss
- **Mental health:** Devastating setback to channel growth

**Solution:** Multiple backup layers. Redundancy saves channels.

---

## 🎯 BACKUP STRATEGY (3-2-1 Rule)

**3** = Three copies of data
**2** = Two different storage types
**1** = One offsite copy

### Your Implementation:
1. **Primary:** Working copy on PC (C:\Users\benoi\Documents\History vs Hype)
2. **Local Backup:** External hard drive (daily/weekly)
3. **Cloud Backup:** OneDrive/Google Drive/Dropbox (automatic)
4. **Remote Git:** GitHub private repository (version control)

---

## 📁 WHAT TO BACK UP

### Tier 1 - CRITICAL (Back up immediately after changes):
- ✅ Scripts (final and drafts)
- ✅ Research documents
- ✅ Source citations
- ✅ Fact-checking notes
- ✅ Project status files
- ✅ Channel analytics data

### Tier 2 - IMPORTANT (Back up weekly):
- ✅ Transcripts
- ✅ B-roll checklists
- ✅ Filming notes
- ✅ Video metadata
- ✅ Templates and guides
- ✅ Slash commands and agents

### Tier 3 - VALUABLE (Back up monthly):
- ✅ Archive folders
- ✅ Old script versions
- ✅ Historical channel data
- ✅ Compass artifacts

### Tier 4 - SEPARATE STORAGE (Large files):
- 📹 **Raw video footage** (external drive + cloud)
- 🎵 **Audio files** (external drive)
- 🎨 **DaVinci Resolve projects** (external drive + cloud)
- 🖼️ **Photoshop files** (external drive)

---

## 💾 METHOD 1: Git Version Control (Primary)

**Status:** ✅ Already set up!

### What Git Protects:
- All markdown files
- Scripts and research
- Documentation
- Configuration files

### Daily Git Workflow:
```bash
# At end of work session:
git add .
git commit -m "Brief description of changes"
```

### Weekly Git Review:
```bash
# View recent changes
git log --oneline -10

# Check repository status
git status
```

### What Git DOESN'T Protect:
- Large video files (*.mp4, *.mov)
- DaVinci Resolve projects (*.drp)
- Photoshop files (*.psd)
- Audio files (*.wav)

**These need separate backup!**

---

## ☁️ METHOD 2: Cloud Backup (Automatic)

### Recommended Services:

#### Option A: OneDrive (Windows Integration)
**Pros:**
- Built into Windows 11
- Automatic sync
- 5GB free (1TB with Microsoft 365)
- Version history

**Setup:**
1. Open OneDrive settings
2. Add "History vs Hype" folder to sync
3. Exclude large files (video footage)
4. Enable "Files On-Demand" to save space

**Cost:** Free (5GB) or $6.99/month (1TB with Office)

#### Option B: Google Drive
**Pros:**
- 15GB free
- Easy sharing
- Good mobile access
- Integrates with Google Docs

**Setup:**
1. Install Google Drive for Desktop
2. Select "History vs Hype" folder to sync
3. Exclude video files
4. Enable automatic backup

**Cost:** Free (15GB) or $1.99/month (100GB)

#### Option C: Dropbox
**Pros:**
- Excellent sync reliability
- Version history (30 days free, unlimited paid)
- Easy sharing

**Cost:** $11.99/month (2TB)

### Recommended Setup:
**Use OneDrive for automatic daily backup of documents**
- Scripts, research, notes automatically synced
- Set up once, forget it
- Access from any device

---

## 💽 METHOD 3: External Hard Drive (Local Backup)

### Recommended Hardware:
- **2TB external drive** ($50-70)
- USB 3.0+ for speed
- Portable (easy to store offsite)

### Backup Schedule:

#### Daily (after significant work):
- New scripts
- Research documents
- Project files

#### Weekly (end of week):
- Full repository backup
- Raw footage from week
- DaVinci Resolve projects

#### Monthly (first of month):
- Complete archive
- Verify backup integrity
- Test restore process

### Windows Backup Setup:

**Method A: Manual Copy (Simple)**
```powershell
# Create backup script
$Source = "C:\Users\benoi\Documents\History vs Hype"
$Destination = "D:\Backups\History-vs-Hype-$(Get-Date -Format 'yyyy-MM-dd')"
Copy-Item -Path $Source -Destination $Destination -Recurse
```

**Method B: Windows Backup (Automatic)**
1. Settings → Update & Security → Backup
2. Add drive → Select external drive
3. "More options" → Add "History vs Hype" folder
4. Set schedule to daily

---

## 🌐 METHOD 4: GitHub Private Repository (Version Control + Remote)

### Why GitHub:
- Free private repositories
- Complete version history
- Accessible from anywhere
- Professional backup solution
- Collaboration ready (future)

### Setup Instructions:

#### 1. Create GitHub Account (if needed)
- Go to github.com
- Sign up for free account

#### 2. Create Private Repository
```bash
# In your History vs Hype folder:
git remote add origin https://github.com/YOUR-USERNAME/history-vs-hype.git
git branch -M main
git push -u origin main
```

#### 3. Daily Push Routine
```bash
# After committing changes:
git push origin main
```

### What Goes to GitHub:
✅ All text files (.md, .txt, .json)
✅ Scripts and documentation
✅ Research notes
✅ Configuration files
✅ Small images (<1MB)

❌ Large video files
❌ Raw footage
❌ DaVinci Resolve projects
❌ Photoshop working files

---

## 📹 VIDEO FOOTAGE BACKUP STRATEGY

### Critical: Video Files Are Irreplaceable

#### Primary Storage:
- Keep on PC during editing
- Delete after video published (if space needed)

#### Backup Storage:
1. **External Drive:** Copy immediately after filming
2. **Cloud Storage:** Use Google Drive / OneDrive / Backblaze
3. **Archive Drive:** Long-term storage (2TB+ drive)

### Folder Structure:
```
External Drive/
├── Raw-Footage/
│   ├── 2025-11-10_sykes-picot/
│   ├── 2025-11-05_lagertha/
│   └── [date]_[topic]/
├── Edited-Projects/
│   ├── sykes-picot_davinci-project.drp
│   └── [topic]_davinci-project.drp
└── Published-Videos/
    ├── final-exports/
    └── thumbnails/
```

### Retention Policy:
- **Raw footage:** Keep 6 months, then archive
- **Project files:** Keep 3 months after publish
- **Final exports:** Keep permanently (small file)

---

## 🔄 BACKUP AUTOMATION

### Create Daily Backup Script:

**File:** `scripts/automation/daily-backup.ps1`

```powershell
# Daily Backup Script for History vs Hype
param(
    [string]$BackupDrive = "D:"
)

$Source = "C:\Users\benoi\Documents\History vs Hype"
$Date = Get-Date -Format "yyyy-MM-dd"
$Destination = "$BackupDrive\Backups\History-vs-Hype-$Date"

Write-Host "🔄 Starting daily backup..." -ForegroundColor Cyan

# Check if backup already exists today
if (Test-Path $Destination) {
    Write-Host "✅ Backup already exists for today" -ForegroundColor Green
    exit 0
}

# Create backup
try {
    Copy-Item -Path $Source -Destination $Destination -Recurse -Force
    Write-Host "✅ Backup complete: $Destination" -ForegroundColor Green

    # Git commit and push
    Set-Location $Source
    git add .
    git commit -m "Daily backup $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    git push origin main

    Write-Host "✅ Changes pushed to GitHub" -ForegroundColor Green
} catch {
    Write-Host "❌ Backup failed: $_" -ForegroundColor Red
    exit 1
}
```

### Schedule with Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "History vs Hype Daily Backup"
4. Trigger: Daily at 6 PM
5. Action: Run PowerShell script
6. Program: `powershell.exe`
7. Arguments: `-File "C:\Users\benoi\Documents\History vs Hype\scripts\automation\daily-backup.ps1"`

---

## ✅ BACKUP VERIFICATION CHECKLIST

### Weekly Check (Every Sunday):
- [ ] Cloud sync is active and up to date
- [ ] External drive has recent backup
- [ ] Git repository pushed to GitHub
- [ ] No backup errors in logs
- [ ] Free space available on all drives

### Monthly Check (First of Month):
- [ ] Test restore process (restore one file)
- [ ] Verify backup integrity
- [ ] Clean up old backups (keep 3 months)
- [ ] Update this checklist if workflow changed
- [ ] Check cloud storage capacity

### Quarterly Check (Every 3 Months):
- [ ] Full disaster recovery test
- [ ] Review backup strategy effectiveness
- [ ] Update backup documentation
- [ ] Verify all important files backed up
- [ ] Check external drive health

---

## 🚨 DISASTER RECOVERY PLAN

### Scenario 1: PC Crash / Hard Drive Failure

**Immediate Action:**
1. Get new PC / drive
2. Install git
3. Clone from GitHub: `git clone https://github.com/YOUR-USERNAME/history-vs-hype.git`
4. Download cloud backup (OneDrive/Google Drive)
5. Verify all files present
6. Resume work

**Recovery Time:** 2-4 hours

---

### Scenario 2: Accidental File Deletion

**Immediate Action:**
1. Check git history: `git log -- [filename]`
2. Restore from git: `git checkout [commit] -- [filename]`
3. Or restore from cloud (OneDrive version history)
4. Or restore from external drive backup

**Recovery Time:** 5-15 minutes

---

### Scenario 3: Ransomware / Malware

**Immediate Action:**
1. Disconnect PC from internet
2. Do NOT pay ransom
3. Wipe PC and reinstall OS
4. Restore from external drive (offline backup)
5. Restore from GitHub
6. Verify files clean

**Recovery Time:** 4-8 hours

**Prevention:** Keep external drive disconnected when not backing up

---

### Scenario 4: Cloud Account Compromise

**Immediate Action:**
1. Change cloud passwords immediately
2. Enable 2FA if not already active
3. Restore from external drive
4. Restore from GitHub
5. Verify file integrity

**Recovery Time:** 1-2 hours

---

## 📊 BACKUP COST ANALYSIS

### Minimum Setup (Free):
- Git + GitHub: Free
- OneDrive: Free (5GB)
- Manual external drive: $60 one-time

**Total:** $60

### Recommended Setup:
- Git + GitHub: Free
- Microsoft 365 (1TB OneDrive): $6.99/month ($84/year)
- 2TB external drive: $70 one-time
- Second 2TB external drive (offsite): $70 one-time

**Total:** $224 first year, $84/year after

### Professional Setup:
- Git + GitHub: Free
- Backblaze (unlimited cloud): $7/month ($84/year)
- Two 4TB external drives: $180 one-time
- NAS drive (network storage): $300 one-time

**Total:** $564 first year, $84/year after

**Channel Revenue Potential:** $500-2000/month when monetized
**Backup Cost:** $7-25/month
**ROI:** Worth it.

---

## 🎯 QUICK START (Do This Now)

### 5-Minute Setup:
1. ✅ Git already initialized
2. [ ] Enable OneDrive sync for this folder
3. [ ] Buy external hard drive (if you don't have one)
4. [ ] Copy entire folder to external drive
5. [ ] Schedule weekly backup reminder

### 30-Minute Setup:
1. [ ] Complete 5-minute setup
2. [ ] Create GitHub account
3. [ ] Push repository to GitHub
4. [ ] Set up automatic cloud sync
5. [ ] Create backup verification checklist
6. [ ] Test restore process with one file

### Complete Setup:
1. [ ] Complete 30-minute setup
2. [ ] Create daily backup script
3. [ ] Schedule automatic backups
4. [ ] Document backup locations
5. [ ] Create disaster recovery plan
6. [ ] Set monthly backup verification reminder

---

## 📝 BACKUP LOG

### Track Your Backups:

**Last Git Commit:** [Check with `git log -1`]
**Last Cloud Sync:** [Check OneDrive/Google Drive]
**Last External Backup:** [Manual check]
**Last GitHub Push:** [Check github.com]

**Update this weekly!**

---

## 💡 PRO TIPS

1. **"3-2-1" Rule:** 3 copies, 2 different types, 1 offsite
2. **Test restores regularly:** Backups are useless if they don't work
3. **Automate everything possible:** Manual backups get forgotten
4. **Keep one backup offline:** Protection against ransomware
5. **Version history matters:** Git saves every version of your work
6. **Document your system:** Future you will thank present you

---

## 🚀 NEXT STEPS

**Today:**
- [ ] Enable cloud sync
- [ ] Make first external drive backup
- [ ] Push to GitHub (if not already done)

**This Week:**
- [ ] Buy external drive (if needed)
- [ ] Set up automatic daily backup
- [ ] Test restore process

**This Month:**
- [ ] Verify all backup methods working
- [ ] Create offsite backup copy
- [ ] Schedule regular backup checks

---

## 📞 EMERGENCY CONTACTS

**If disaster strikes:**
1. **Don't panic** - Your backups exist
2. **Follow recovery plan** - See Disaster Recovery section
3. **Document what happened** - Improve process
4. **Verify all files recovered** - Before resuming work

**Remember:** Good backups mean disasters are inconveniences, not catastrophes.

---

**Last Updated:** 2025-11-10
**Status:** Essential - Implement immediately
**Priority:** CRITICAL

**Your channel is valuable. Protect it.**
