# `eb2e.py` — Eventbrite to EZ Badge CSV Converter

`eb2ez.py` converts an [Eventbrite](https://www.eventbrite.com/) **Attendee Report CSV** to an [EZ Badge](https://ez-badge.com/) **upload CSV**, enabling badge printing for in-person event attendees.

---

## 🧾 Default Field Mappings

The default field mappings are tailored for the **IEEE Consultants' Network of Silicon Valley (CNSV)**, using their custom Eventbrite fields and EZ Badge upload template.

This transformation:

* Converts `Yes/No` fields into formatted values suitable for badge printing.
* Ensures EZ Badge compliance by replacing certain values and adjusting field names.

---

## 📥 Example Input Format (Eventbrite CSV)

```
Order #,Order Date,First Name,Last Name,Email,Quantity,Price Tier,Ticket Type,Attendee #,Group,Order Type,Currency,Total Paid,Fees Paid,Eventbrite Fees,Eventbrite Payment Processing,Attendee Status,Home Address 1,Home Address 2,Home City,Home State,Home Zip,Home Country,How did you hear about this event?,Are you a consultant?,Are you an IEEE member?,Are you an IEEE-CNSV Member?,Where are you located (city+state or city+country),Please tell us where you heard about this event,Of which IEEE Societies and/or Affinity Groups are you a member?,Job Title,Company
11211912243,11/29/24 22:28,John,Doe,jdoe1@test1mail.com,1,,General Admission,18441583423,,Free Order,USD,0,0,0,0,Attending,,,,,,,CNSV Email,Yes,No,No,"City1, CA",,,JobTitle1,Company1Name
11211987213,11/29/24 22:54,Jane,Doe,jdoe2@test2mail.com,1,,General Admission,18441700883,,Free Order,USD,0,0,0,0,Attending,,,,,,,CNSV Email,No,No,No,City2 CA,,,Job2Title,Company2Name
```

---

## 📤 Example Output Format (EZ Badge CSV)

```
FirstName,LastName,Email,Company or Organization,IEEE?,CNSV?,Are you a consultant?,Are you on CNSV BOD?,CB 6:1 - CNSV Email,CB 6:2 - CNSV Website,CB 6:3 - IEEE GRID,CB 6:4 - Eventbrite Browsing,CB 6:5 - Meetup,CB 6:6 - Friend,CB 6:7 - Other,
John,Doe,jdoe1@test1mail.com,Company1Name,IEEE," ",Consultant," "," "," "," "," "," "," "," ",
Jane,Doe,jdoe2@test2mail.com,Company2Name," "," "," "," "," "," "," "," "," "," "," ",
```

---

## ⚠️ Notes on EZ Badge CSV Format

* Fields with real-world null values are represented as quoted space characters (`" "`).
* Quoted values are required **only** for:

  * quotation marks (`"`),
  * commas (`,`),
  * carriage returns (`\r`), and
  * newline characters (`\n`).
* All lines in the EZ Badge output end with a **trailing comma (`,`)** — this is required by the system.

---

## 🧰 Usage

```bash
python eb2e.py <input_file.csv>
```

Or for help:

```bash
python eb2e.py --help
```

---

## 🛑 Error Handling

The script will raise errors if:

1. The input file is missing,
2. The input is not a CSV file, or
3. The expected column headers do not match the specification.

---

## 🧹 File Preprocessing Rules

The following substitutions are applied before writing the EZ Badge file:

1. `"Are you a consultant?"`

   * `"Yes"` → `Consultant`
   * `"No"`  → `" "` (space in quotes)

2. `"Are you an IEEE member?"`

   * `"Yes"` → `IEEE`
   * `"No"`  → `" "`

3. `"Are you an IEEE-CNSV Member?"`

   * `"Yes"` → `CNSV`
   * `"No"`  → `" "`

---

## 🔁 Column Headings Map

| Eventbrite Field               | EZ Badge Field            |
| ------------------------------ | ------------------------- |
| `First Name`                   | `FirstName`               |
| `Last Name`                    | `LastName`                |
| `Company`                      | `Company or Organization` |
| `Are you an IEEE member?`      | `IEEE?`                   |
| `Are you an IEEE-CNSV Member?` | `CNSV?`                   |

