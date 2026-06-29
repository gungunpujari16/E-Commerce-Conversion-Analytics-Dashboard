# 🛒 E-Commerce Conversion Analytics Dashboard

**MBA Data Analytics | SP Jain Global | Dubai Campus | Term 2**

An interactive Streamlit dashboard for descriptive and diagnostic analytics of an e-commerce customer conversion and sales pipeline dataset.

---

## 📁 File Structure

```
dashboard/
├── app.py                          # Main Streamlit application
├── utils.py                        # Data loading, filters, colour helpers
├── ecommerce_cleaned.csv           # Dataset (place in same folder as app.py)
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

---

## 🚀 Quick Start — Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-dashboard.git
cd ecommerce-dashboard
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Place the dataset
Copy `ecommerce_cleaned.csv` into the same folder as `app.py`.

### 5. Run the dashboard
```bash
streamlit run app.py
```

The dashboard opens automatically at `http://localhost:8501`

---

## ☁️ Deploy on Streamlit Community Cloud (Free)

1. Push this folder to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New App**
4. Select your repo, branch (`main`), and set **Main file path** to `app.py`
5. Click **Deploy**

> ⚠️ **Important:** The CSV file must be committed to the repo.
> Streamlit Cloud reads files relative to `app.py`.

---

## 📊 Dashboard Pages

| Tab | Contents |
|---|---|
| **Overview & KPIs** | Conversion rate, cart rate, AOV, return rate, gender/age breakdown |
| **Funnel Analysis** | Waterfall drop-off, abandonment by stage/device, traffic × abandonment heatmap |
| **Traffic & Channels** | Channel conversion rates, device performance, location analysis |
| **Products & Revenue** | Category conversion, AOV, friction index bubble chart, payment analysis |
| **Diagnostic Deep-Dive** | Skewness distributions, engagement scatter, correlation heatmap, discount impact |

---

## 🎛️ Sidebar Filters (apply to all tabs simultaneously)

- Traffic Source (multi-select)
- Device Type (multi-select)
- Product Category (multi-select)
- Location (multi-select)
- Payment Method (multi-select)
- Customer Type (All / New / Return)
- Age Range (slider)

---

## 🛠️ Tech Stack

| Library | Version | Purpose |
|---|---|---|
| Streamlit | 1.35 | Dashboard framework |
| Plotly | 5.22 | Interactive charts |
| Pandas | 2.2 | Data manipulation |
| NumPy | 1.26 | Numerical operations |
| SciPy | 1.13 | Statistical tests |

---

## 📌 Notes

- All charts respond to sidebar filters in real time
- The **Diagnostic** tab includes a raw data explorer with CSV export
- Dataset: 1,400 synthetic e-commerce customer records × 20 features
