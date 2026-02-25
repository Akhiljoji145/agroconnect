# Expert Verification System - Admin Guide

## 🎯 Why Expert Status is Pending

When experts register in the system, they start with **"pending"** verification status by default. This is a security measure to ensure only qualified experts provide agricultural advice.

## 🔐 Admin Verification Process

### **Step 1: Access Admin Panel**
```
URL: http://127.0.0.1:8000/admin/
Login: Your superuser credentials
```

### **Step 2: Expert Verification Dashboard**
```
URL: http://127.0.0.1:8000/admin/verification_dashboard/
```
**Features:**
- 📊 Verification statistics
- ⏳ Pending experts list
- ✅ Recent verification actions
- 📈 Specialization breakdown

### **Step 3: Review Expert Applications**

#### **Option A: Individual Review**
1. Go to: `/admin/expert/expertprofile/`
2. Filter by: `Verification Status: Pending`
3. Click on expert name to review
4. Check:
   - Qualifications and experience
   - Uploaded verification documents
   - Specialization relevance
5. Change status to: `Verified` or `Rejected`

#### **Option B: Bulk Actions**
1. Select multiple pending experts
2. Choose action:
   - `Verify selected experts` - Sets status to "verified"
   - `Reject selected experts` - Sets status to "rejected"

### **Step 4: Verification Form Features**

The enhanced admin form includes:
- 📋 Expert information display
- 📄 Verification document preview
- ⚡ Quick approve/reject checkboxes
- 📊 Status indicators
- 🔄 Manual status change dropdown

## 🏆 Expert Verification Statuses

### **🟡 Pending (Default)**
- Expert just registered
- Waiting for admin review
- Cannot accept consultations
- Shown as "unverified" to farmers

### **✅ Verified**
- Admin has approved expert
- Can accept consultations
- Appears in expert browse
- Shows "verified" badge

### **❌ Rejected**
- Admin has rejected expert
- Cannot accept consultations
- Hidden from expert browse
- Can re-register with new info

## 📋 Admin Dashboard Features

### **📊 Statistics Cards**
- Total experts count
- Pending verification count
- Verified experts percentage
- Recent registrations

### **📝 Pending Experts Table**
- Expert username and email
- Specialization and experience
- Registration date
- Direct review links

### **🔄 Recent Actions**
- Last 7 days of changes
- Status updates
- Quick access to details

### **📈 Specialization Breakdown**
- Expert distribution by field
- Verification status per specialization
- Visual progress bars

## 🔗 Quick Access URLs

### **Admin Access:**
- Main Admin: `http://127.0.0.1:8000/admin/`
- Verification Dashboard: `http://127.0.0.1:8000/admin/verification_dashboard/`
- Expert Management: `http://127.0.0.1:8000/admin/expert/expertprofile/`

### **Expert Management:**
- Pending Only: `http://127.0.0.1:8000/admin/expert/expertprofile/?verification_status__exact=pending`
- Verified Only: `http://127.0.0.1:8000/admin/expert/expertprofile/?verification_status__exact=verified`
- Rejected Only: `http://127.0.0.1:8000/admin/expert/expertprofile/?verification_status__exact=rejected`

## 🎯 Best Practices

### **✅ Verification Criteria:**
1. **Check Qualifications**: Verify educational background
2. **Review Experience**: Confirm years of experience
3. **Validate Documents**: Check uploaded certificates
4. **Assess Specialization**: Ensure expertise matches field
5. **Contact Information**: Verify phone and email

### **⚠️ Quality Control:**
- Reject incomplete applications
- Verify document authenticity
- Check for duplicate profiles
- Monitor expert activity post-verification

### **📞 Communication:**
- Notify experts of verification status
- Provide reasons for rejection
- Allow re-application with corrections
- Maintain professional communication

## 🚀 Implementation Complete

The expert verification system now includes:
- ✅ Enhanced admin interface
- ✅ Verification dashboard
- ✅ Bulk approval/rejection
- ✅ Document preview
- ✅ Statistics and analytics
- ✅ Status tracking
- ✅ Professional UI

**🎉 Your expert verification system is now fully functional with comprehensive admin management!**
