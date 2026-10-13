# 🦈 GitHub Achievement Unlocker

> Koleksi script Python untuk unlock GitHub Profile Achievements secara otomatis dan efisien.

[![GitHub Stars](https://img.shields.io/github/stars/Hadi-Akram-Ramadhan/generate-git?style=social)](https://github.com/Hadi-Akram-Ramadhan/generate-git)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Table of Contents

- [Fitur](#-fitur)
- [Achievements yang Didukung](#-achievements-yang-didukung)
- [Prasyarat](#-prasyarat)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Struktur Script](#-struktur-script)
- [FAQ & Troubleshooting](#-faq--troubleshooting)
- [Kontribusi](#-kontribusi)
- [Disclaimer](#-disclaimer)
- [License](#-license)

---

## 🎯 Fitur

- **Otomatis & Cepat**: Script teroptimasi dengan pacing API yang aman dari rate-limit GitHub.
- **Realistic Commits**: Generate PR dengan commit message conventional, code TypeScript/React realistis, dan struktur folder production-ready.
- **Multi-Achievement Support**: Unlock Pull Shark, Galaxy Brain, Quickdraw, dan YOLO dalam satu repository.
- **Clean & Modular**: Setiap achievement punya script terpisah dengan docstring jelas.

---

## 🏆 Achievements yang Didukung

| Badge | Nama | Tier Maksimal | Script | Deskripsi |
|-------|------|---------------|--------|-----------|
| 🦈 | **Pull Shark** | Gold (x4) | `unlock_pull_pair_gold.py` | Unlock dengan 1,024 merged PRs |
| 🧠 | **Galaxy Brain** | Gold (x4) | `unlock_galaxy_brain.py` | Unlock dengan 32 accepted Q&A answers |
| 🤠 | **Quickdraw** | Base | Manual (close issue <5 min) | Close issue dalam 5 menit |
| 🎲 | **YOLO** | Base | Manual (merge PR tanpa review) | Merge PR tanpa code review |

---

## 🔧 Prasyarat

### Software Requirements

```bash
# Python 3.8 atau lebih tinggi
python --version

# Git CLI terinstall dan terkonfigurasi
git --version

# Requests library
pip install requests
```

### GitHub Setup

1. **Personal Access Token (PAT)**
   - Buka [GitHub Settings → Developer Settings → Tokens](https://github.com/settings/tokens)
   - Generate token dengan scope:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `write:discussion` (Read/write discussions)
     - ✅ `read:user`
   - Simpan token di Git Credential Manager (script akan auto-detect):
     ```bash
     git credential approve
     protocol=https
     host=github.com
     username=YOUR_GITHUB_USERNAME
     password=YOUR_PAT_TOKEN
     ```

2. **Repository Target**
   - Buat repository baru atau gunakan existing repo
   - **WAJIB PUBLIC** selama script berjalan (bisa di-private lagi setelah badge muncul)
   - Enable **GitHub Discussions** di Settings → Features → Discussions (untuk Galaxy Brain)
   - Tambahkan **Q&A category** di Discussions

3. **Akun Kolaborator (untuk Pair Extraordinaire & Galaxy Brain)**
   - Buat akun GitHub kedua (atau minta teman jadi collaborator)
   - Invite sebagai **Collaborator** dengan **Write access**
   - Generate PAT untuk akun helper tersebut

---

## 📦 Instalasi

### 1. Clone Repository

```bash
cd C:\laragon\www  # atau direktori pilihan lo
git clone https://github.com/Hadi-Akram-Ramadhan/generate-git.git
cd generate-git
```

### 2. Install Dependencies

```bash
pip install requests
```

### 3. Konfigurasi Script

Edit script dan sesuaikan variabel berikut:

#### `unlock_galaxy_brain.py`
```python
REPO_ID = "R_kgDOUuDulA"              # GraphQL Node ID repo lo
QA_CATEGORY_ID = "DIC_kwDOUuDulM4DHOlT"  # Q&A Category ID dari Discussions
HELPER_TOKEN = "ghp_xxxxxxxxxxxxx"    # PAT akun helper
REPO_PATH = r"C:\path\to\repo"        # Path lokal repo target
```

**Cara Dapat Repo ID & Category ID:**
```graphql
# Jalankan di https://docs.github.com/en/graphql/overview/explorer
query {
  repository(owner: "USERNAME", name: "REPO") {
    id
    discussionCategories(first: 10) {
      nodes {
        id
        name
        isAnswerable
      }
    }
  }
}
```

#### `unlock_pull_pair_gold.py`
```python
REPO_OWNER = "Hadi-Akram-Ramadhan"
REPO_NAME = "sibermu-haf"
REPO_PATH = r"C:\laragon\www\sibermu-haf"

CO_AUTHOR_NAME = "hadooyy90-afkrere"
CO_AUTHOR_EMAIL = "330958267+hadooyy90-afkrere@users.noreply.github.com"
```

---

## 🚀 Cara Penggunaan

### Script 1: Pull Shark Gold

Generate 500+ realistic Next.js/React PRs dengan struktur production-ready.

```bash
cd C:\laragon\www\YOUR_REPO
python unlock_pull_pair_gold.py
```

**Estimasi Waktu:** ~30–60 menit (tergantung jumlah PR yang dibutuhkan)

**Output:**
- ✅ 500+ merged PRs dengan commit message conventional (`feat(ui):`, `perf(gsap):`, dll)
- ✅ File tersebar di `components/`, `lib/`, `types/`, `app/` (production-realistic)

---

### Script 2: Galaxy Brain Gold

Generate 32 accepted answers di GitHub Discussions Q&A.

```bash
cd C:\laragon\www\sibermu-haf
python unlock_galaxy_brain.py
```

**Estimasi Waktu:** ~5–10 menit

**Cara Kerja:**
1. Akun helper membuat 32 pertanyaan teknis di Discussions (kategori Q&A)
2. Akun utama menjawab setiap pertanyaan
3. Akun helper meng-accept jawaban (via GraphQL `markDiscussionCommentAsAnswer`)

**Output:**
- ✅ 32 accepted answers → **Galaxy Brain Gold (x4)**

---

## 📂 Struktur Script

```
generate-git/
│
├── README.md                      # Dokumentasi lengkap (file ini)
├── unlock_pull_pair_gold.py       # Pull Shark Gold
├── unlock_galaxy_brain.py         # Galaxy Brain Gold via Discussions
├── run_clean.py                   # Helper: Sequential PR runner (opsional)
│
└── .gitignore                     # Ignore tokens dan cache
```

---

## ❓ FAQ & Troubleshooting

### Q: Badge tidak muncul setelah script selesai?

**A:** GitHub Achievement indexing berjalan secara **asynchronous** dengan delay 15 menit hingga 48 jam. Solusi:
1. Pastikan repository dalam status **PUBLIC** saat script berjalan
2. Buka **Settings → Public profile** → Centang `Include private contributions on my profile`
3. Hard refresh profil (`Ctrl + F5`) di browser
4. Tunggu maksimal 24–48 jam

---

### Q: Error `fatal: Unable to create '.git/index.lock': File exists`

**A:** Git collision dari proses concurrent. Solusi:
```bash
cd C:\laragon\www\sibermu-haf
rm -f .git/index.lock
python unlock_pull_pair_gold.py  # Run ulang
```

---

### Q: Error `GitHub API rate limit exceeded`

**A:** Lo kena rate-limit 5000 req/hour. Solusi:
- Tunggu 1 jam, atau
- Gunakan PAT dengan scope lengkap (rate-limit lebih tinggi untuk authenticated requests)

---

### Q: Co-author tidak terdeteksi di commit history?

**A:** Format trailer salah atau email tidak verified. Cek:
1. Harus ada **blank line** sebelum `Co-authored-by:`
2. Email harus match dengan verified email di GitHub Settings akun co-author
3. Format: `Co-authored-by: Name <email@domain.com>` (case-sensitive!)

---

### Q: Pair Extraordinaire masih belum unlock padahal sudah 50+ co-authored PRs?

**A:** GitHub menghitung berdasarkan **co-authored commits**, bukan jumlah PR. Solusi:
- Pastikan setiap PR menggunakan **standard merge** (bukan squash/rebase yang bisa strip trailer)
- Cek apakah repo sempat di-private saat script jalan (ubah ke public dulu!)
- Re-trigger indexing dengan merge 1 PR baru di repo public

---

### Q: Apakah bisa di-run di Linux/macOS?

**A:** **Yes!** Ubah path separator:
```python
# Windows
REPO_PATH = r"C:\laragon\www\sibermu-haf"

# Linux/macOS
REPO_PATH = "/home/user/projects/sibermu-haf"
```

---

## 🤝 Kontribusi

Contributions are welcome! Kalau lo punya ide improvement atau nemuin bug:

1. Fork repo ini
2. Buat branch fitur baru (`git checkout -b feat/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push ke branch (`git push origin feat/amazing-feature`)
5. Open Pull Request

---

## ⚠️ Disclaimer

Script ini dibuat untuk **tujuan edukasi dan eksperimen** dengan GitHub API. Penggunaan untuk spamming, abuse, atau melanggar [GitHub Terms of Service](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service) adalah **tanggung jawab pengguna**.

**Catatan Penting:**
- Jangan gunakan script ini di repository production yang aktif dipakai tim
- Gunakan repository testing/sandbox khusus
- Hargai kolaborator real dan jangan abuse co-author feature untuk manipulasi kontribusi orang lain
- GitHub berhak merevoke achievements atau suspend akun yang abuse automation

---

## 📜 License

MIT License - bebas digunakan, dimodifikasi, dan didistribusikan.

---

## 🌟 Credits

Dibuat dengan ❤️ oleh [Hadi Akram Ramadhan](https://github.com/Hadi-Akram-Ramadhan)

**Tech Stack:**
- Python 3.8+
- GitHub REST API v3
- GitHub GraphQL API v4
- Git CLI

---

## 📞 Support

Butuh bantuan? Open issue di [GitHub Issues](https://github.com/Hadi-Akram-Ramadhan/generate-git/issues) atau DM via [GitHub Profile](https://github.com/Hadi-Akram-Ramadhan).

---

**Happy Achievement Hunting! 🚀**
