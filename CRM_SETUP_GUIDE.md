# CRM Setup Guide for Head-Bot

**Purpose:** Maintain organized client data, track interactions, and automate workflows for apostille service delivery and client management.

---

## 1. CHOOSING A CRM PLATFORM

### Recommended CRM Options (Ranked by Apostille/Service Business Fit):

#### **Option A: HubSpot CRM** (Recommended for Small Teams)
- **Cost:** Free up to 2 million contacts
- **Pros:** 
  - Excellent deal pipeline tracking
  - Built-in email templates and sequences
  - Mobile app for on-the-go access
  - Strong reporting and dashboards
  - Native integration with Google Workspace
- **Cons:** 
  - Limited without paid features
  - Learning curve for complex workflows
- **Best For:** Service businesses starting from scratch

---

#### **Option B: Pipedrive**
- **Cost:** $12/user/month (billed annually)
- **Pros:**
  - Designed for sales pipelines
  - Visual deal flow (easy to manage at a glance)
  - Strong mobile app
  - Good for service businesses
- **Cons:**
  - Limited contact detail fields
  - Fewer automation options
- **Best For:** Teams focused on sales pipeline velocity

---

#### **Option C: Salesforce**
- **Cost:** $75/user/month (Professional edition)
- **Pros:**
  - Highly customizable
  - Excellent for enterprise workflows
  - Strong ecosystem and integrations
- **Cons:**
  - Overkill for small service teams
  - Steep learning curve
  - High cost
- **Best For:** Growing companies with complex workflows

---

#### **Option D: Monday.com**
- **Cost:** $10/user/month (billed annually)
- **Pros:**
  - Easy to use and visually appealing
  - Flexible workflows (can model any process)
  - Great for team collaboration
- **Cons:**
  - Less sales-centric than other CRMs
  - Fewer out-of-box sales features
- **Best For:** Teams wanting flexibility and ease-of-use

---

**RECOMMENDATION FOR COMMON NOTARY:** Start with **HubSpot Free** and upgrade to Professional ($50/month) if you need advanced automation and reporting.

---

## 2. CRM DATA STRUCTURE

### CORE OBJECTS TO SET UP:

#### **A. CONTACTS** (Individual people at companies)
```
Contact Fields:
- First Name (required)
- Last Name (required)
- Email (required)
- Phone (required)
- Job Title
- Company (linked to Company object)
- Decision Maker? (yes/no)
- Contact Preference (email/phone/LinkedIn)
- Best Time to Reach (morning/afternoon/evening)
- Notes (recent conversation summary)
```

#### **B. COMPANIES** (Client organizations)
```
Company Fields:
- Company Name (required)
- Industry (legal/corporate/education/government/other)
- Company Size (1-50 / 51-250 / 251-1000 / 1000+)
- Website
- Phone
- Address
- Annual Revenue (estimate)
- Estimated Apostille Volume (documents/month)
- Geographic Presence (states they operate in)
- Source (cold outreach / referral / LinkedIn / event)
- Decision Maker (linked to Contact object)
- Account Manager (staff member assigned)
```

#### **C. DEALS** (Sales pipeline)
```
Deal Fields:
- Deal Name (e.g., "ABC Corp - Apostille Services")
- Stage (see below)
- Company (linked)
- Company Contact (linked)
- Deal Amount ($)
- Close Date (target)
- Description (key terms, special requests)
- Annual Contract Value (estimated yearly spend)
- Contract Length (months)
```

**Deal Stages Pipeline:**
1. **Prospect** — Lead identified, not yet contacted
2. **Outreach** — Initial contact made, waiting for response
3. **Qualified** — Response received, schedules meeting
4. **Discovery** — Had first conversation, assessing fit
5. **Proposal** — Sent custom proposal, awaiting decision
6. **Negotiation** — Discussing terms/pricing
7. **Closed Won** — Contract signed
8. **Closed Lost** — Prospect declined or went elsewhere

---

## 3. IMPLEMENTATION STEPS

### **STEP 1: Set Up Contact Database** (Week 1)
```
1. Create HubSpot (or chosen CRM) account
2. Set up basic contact fields (first, last, email, phone, company)
3. Create "Companies" object with fields listed above
4. Link contacts to companies
5. Create contact import template (CSV for bulk imports)
```

### **STEP 2: Build Sales Pipeline** (Week 1-2)
```
1. Create Deal object with stages (see above)
2. Set up deal fields (amount, close date, company, contact)
3. Create deal templates for common contract scenarios
4. Set contact fields that auto-populate from company data
```

### **STEP 3: Create Intake Forms** (Week 2)
```
1. Build simple "Contact Us" form on website
   - Company Name
   - Contact Name
   - Email
   - Phone
   - Brief description of need
   - Apostille volume estimate

2. Set up form to auto-create Contact + Company records
3. Auto-assign to account manager
```

### **STEP 4: Set Up Workspaces & Views** (Week 2)
```
1. Create "Sales Dashboard"
   - Pipeline by stage
   - Won vs. loss rate
   - Average deal size
   - Sales cycle length

2. Create "Account Management Dashboard"
   - Clients by status
   - Upcoming renewals
   - Customer satisfaction scores
   - Service delivery timeline

3. Create "Prospect Dashboard"
   - Outreach attempts by status
   - Response rate by campaign
   - Lead source performance
```

### **STEP 5: Integrate Email & Calendar** (Week 3)
```
1. Connect email account (Gmail/Outlook) to CRM
2. Enable email logging (auto-log outbound messages)
3. Connect calendar to see availability
4. Set up meeting templates for recurring call types
5. Enable automated call logging (if phone integrated)
```

### **STEP 6: Create Email Templates** (Week 3)
```
1. Import email templates from EMAIL_TEMPLATES.md file
2. Create CRM sequences for:
   - Cold outreach (3 email sequence)
   - Discovery follow-up (2 email sequence)
   - Proposal delivery (1 email + follow-up)
   - Post-discovery nurture (4 email sequence)

3. Set up automation to trigger sequences based on stage
```

### **STEP 7: Build Automation Workflows** (Week 4)
```
See detailed workflow examples below in Section 4
```

---

## 4. CRITICAL CRM WORKFLOWS & AUTOMATIONS

### **WORKFLOW A: New Contact Creation** 
**Trigger:** Contact added to database
**Actions:**
1. Auto-create or link to Company
2. Assign to account manager
3. Create initial task: "Research prospect" (1 day)
4. Create calendar event: "First outreach call" (5 days out)

---

### **WORKFLOW B: Prospect Cold Outreach**
**Trigger:** Contact moves to "Prospect" stage
**Actions:**
1. Send cold outreach email from EMAIL_TEMPLATES.md
2. Create task: "Follow up if no response" (3 days)
3. Log outreach attempt in Contact timeline
4. Set reminder for manager

---

### **WORKFLOW C: Qualified Lead / Discovery Meeting**
**Trigger:** Contact responds to outreach
**Actions:**
1. Update contact status to "Qualified"
2. Create task: "Schedule discovery call"
3. Move deal to "Discovery" stage
4. Send calendar invite template
5. Create pre-call research task for manager

---

### **WORKFLOW D: Post-Discovery Next Steps**
**Trigger:** Manager logs discovery call notes and moves deal to "Proposal"
**Actions:**
1. Auto-create task: "Prepare custom proposal" (1 day)
2. Create task: "Send proposal email" (2 days)
3. Create task: "Schedule proposal review call" (3 days)
4. Set deal close date based on typical sales cycle

---

### **WORKFLOW E: Proposal Sent**
**Trigger:** Proposal email sent (logged in CRM)
**Actions:**
1. Update deal stage to "Proposal"
2. Send task reminder: "Follow up on proposal" (5 days)
3. Log proposal sent date
4. Set deal close date (10 days out)
5. Alert manager if no response within 5 days

---

### **WORKFLOW F: Deal Won / Contract Signed**
**Trigger:** Contract signed and uploaded
**Actions:**
1. Update deal to "Closed Won"
2. Create recurring tasks for:
   - Monthly check-in calls (1st day of month)
   - Quarterly business reviews (every 3 months)
   - Renewal follow-up (30 days before expiration)
3. Create company record fields:
   - Contract start date
   - Contract end date
   - Monthly value
   - Account manager
   - Onboarding status
4. Generate onboarding checklist (see ONBOARDING_CHECKLIST.md)
5. Send welcome email sequence

---

### **WORKFLOW G: Inactive Client Alert**
**Trigger:** No orders or communications in 60 days
**Actions:**
1. Alert account manager
2. Create task: "Outreach to inactive client" (urgent)
3. Tag contact as "At Risk"
4. Prepare win-back email (from EMAIL_TEMPLATES.md)

---

### **WORKFLOW H: Contract Renewal Alert**
**Trigger:** 60 days before contract expiration
**Actions:**
1. Create task: "Schedule renewal business review call"
2. Create calendar event for renewal meeting
3. Prepare contract renewal proposal
4. Alert account manager with renewal details
5. Send renewal email sequence

---

## 5. REPORTING & ANALYTICS DASHBOARDS

### **Sales Performance Dashboard**
```
Key Metrics:
- Total Prospects in Pipeline: [#]
- Prospects by Stage: 
  * Prospect: [#]
  * Outreach: [#]
  * Qualified: [#]
  * Discovery: [#]
  * Proposal: [#]
  * Negotiation: [#]
  * Closed Won: [#]
  * Closed Lost: [#]

- Won Deals (This Month): [#] ($[total])
- Lost Deals (This Month): [#]
- Win Rate: [%]
- Average Deal Size: $[amount]
- Sales Cycle Length: [X] days
- Revenue Forecast (Next 30/60/90 days): $[amount]
```

### **Account Management Dashboard**
```
Key Metrics:
- Total Active Clients: [#]
- Clients by Status:
  * Onboarding: [#]
  * Active: [#]
  * At Risk (60+ days no order): [#]
  * Churned: [#]

- Contracts Expiring (Next 30 days): [#]
- Monthly Revenue: $[amount]
- Customer Satisfaction (NPS): [score]
- Service Delivery On-Time Rate: [%]
```

### **Marketing & Outreach Dashboard**
```
Key Metrics:
- Outreach Attempts (This Month): [#]
- Response Rate: [%]
- Top Source for Leads: [source]
- Cost Per Prospect: $[amount]
- Conversion by Source: [source] [%]
```

---

## 6. DATA HYGIENE BEST PRACTICES

### **Monthly CRM Maintenance:**

1. **Remove Duplicates**
   - Run duplicate detection
   - Merge duplicate contacts/companies
   - Consolidate to most recent/complete record

2. **Update Contact Info**
   - Flag contacts with old phone/email
   - Verify decision makers still at company
   - Update company size/revenue if changed

3. **Clean Up Deals**
   - Close deals stuck in same stage 30+ days
   - Update close dates if changed
   - Document loss reasons for closed deals

4. **Archive Old Contacts**
   - Move cold prospects (no response in 6+ months) to archive
   - Keep completed deals in active database
   - Maintain clean pipeline

5. **Standardize Data**
   - Ensure consistent company name formats
   - Standardize phone numbers and emails
   - Use picklist values (don't free-type industry, etc.)

---

## 7. SECURITY & COMPLIANCE

### **Access Control:**
- Limit CRM access to authorized team members
- Use role-based permissions:
  - **Admin:** Full access
  - **Account Manager:** Can view/edit own accounts
  - **Sales:** Can view all contacts, edit own prospects
  - **Support:** Read-only view of active clients

### **Data Protection:**
- Enable two-factor authentication (2FA)
- Use strong passwords (minimum 12 characters)
- Never share login credentials
- Review access logs monthly
- Back up data monthly (if self-hosted)

### **Privacy Compliance:**
- GDPR: Delete contact data if requested
- CCPA: Respect "do not contact" requests
- CAN-SPAM: Honor unsubscribe requests
- Document consent for email/phone outreach

---

## 8. TRAINING & ROLLOUT

### **User Training (2 hours total):**
```
Module 1 (30 min): CRM Overview & Navigation
- Dashboard orientation
- How to add records
- How to update stages

Module 2 (40 min): Daily Workflows
- Logging activities
- Sending templated emails
- Scheduling meetings
- Creating tasks

Module 3 (30 min): Reporting & Analytics
- Running reports
- Interpreting dashboards
- Using data for decisions
- Monthly review process
```

### **Rollout Timeline:**
- **Week 1:** Set up CRM, import contacts, basic training
- **Week 2:** Migrate one active deal through full workflow
- **Week 3:** Full team usage with manager oversight
- **Week 4:** Review adoption, troubleshoot, finalize processes

---

## 9. COMMON CRM PITFALLS TO AVOID

❌ **Not standardizing data entry** → Garbage in, garbage out
✅ Do: Create pick-lists, use templates, enforce required fields

❌ **Overcomplicating workflows** → Too much automation, hard to maintain
✅ Do: Start simple, add complexity only when needed

❌ **Ignoring data quality** → Old/wrong contact info loses deals
✅ Do: Monthly hygiene, verify phone/email before outreach

❌ **Lack of user adoption** → CRM unused, decisions made outside system
✅ Do: Train thoroughly, make CRM easy to use, tie to incentives

❌ **No regular backups** → Data loss in transition or crash
✅ Do: Monthly exports, automated backups, disaster recovery plan

---

## 10. CRM QUICK START CHECKLIST

- [ ] Choose CRM platform (HubSpot recommended)
- [ ] Set up Contact object with required fields
- [ ] Set up Company object with required fields
- [ ] Set up Deal object with pipeline stages
- [ ] Create contact import template
- [ ] Build "Contact Us" form on website
- [ ] Import existing contacts and companies
- [ ] Create sales dashboard
- [ ] Create account management dashboard
- [ ] Connect email and calendar
- [ ] Import email templates from EMAIL_TEMPLATES.md
- [ ] Build automation workflows (Sections 4)
- [ ] Set up user roles and access control
- [ ] Conduct user training
- [ ] Establish monthly maintenance schedule
- [ ] Document CRM processes in team wiki

---

*Last Updated: February 11, 2026*
